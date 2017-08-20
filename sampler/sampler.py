try:
    from math import gcd
except ImportError:
    from fractions import gcd

from functools import reduce
from random import random

import numpy as np
from numpy.linalg import matrix_rank


class Sampler(object):
    """ Implements an elementary mode sampler.
    This is a refactored and slightly modified version of https://code.google.com/archive/p/emsampler/
    Inputs:
        matrix (stoichiometric matrix),
        rev_vector (reversibility vector),
        k (tunable parameter to adjust output size).
    Note: if k is undefined it will compute all modes.
    For more information consult the respective paper (Machado et al; 2012) (submitted).
    """

    def __init__(self, matrix, rev_vector, k=None):
        self.matrix = self.sort_matrix_by_first_column(matrix)
        self.rev_vector = self.check_reversibility_vector(rev_vector)
        self.k = k
        self.result = self.sampler()

    def sampler(self):
        m, n = self.matrix.shape
        T = np.hstack((self.matrix.T, np.eye(n)))

        for i in range(m):
            T2, first_i_rows, nonzero_columns, npairs, pairs, revT2 = self.prepare_vars(T, i)

            # print 'line {} of {} - keep: {} combinations: {}'.format(i + 1, m, nonzero_columns.shape[0], npairs),

            for j, k in pairs:
                cj, ck = self.get_cj_ck(T, j, k)
                Tj, Tk = self.get_Tj_Tk(T, cj, ck, j, k)
                Tjk = Tj + Tk
                revTjk = self.get_revTjk(j, k)
                minimal = self.get_minimal(Tj, Tjk, Tk, first_i_rows, i, m)
                T2, revT2 = self.recalculate_T2_and_revT2_if_minimal_exist(T2, Tjk, minimal, revT2, revTjk)

            selection = self.filter_rows_based_on_probability(T2)
            T = self.vstack_TandT2_based_on_selection(T, T2, nonzero_columns, selection)
            self.rev_vector = self.hstack_revandrevT2_based_on_selection(nonzero_columns, revT2, selection)

            # print 'new: {} total {}'.format(T.shape[0] - nonzero_columns.shape[0], T.shape[0])

        E = self.normalize_and_make_into_list(T)
        # print 'Found {} modes.'.format(len(E))

        return E

    @staticmethod
    def recalculate_T2_and_revT2_if_minimal_exist(T2, Tjk, minimal, revT2, revTjk):
        if minimal:
            T2 = np.vstack((T2, Tjk))
            revT2 = np.hstack((revT2, revTjk))
        return T2, revT2

    def normalize_and_make_into_list(self, T):
        E = list(map(self._normalize, T))
        E = [e.tolist() for e in E]
        return E

    def hstack_revandrevT2_based_on_selection(self, nonzero_columns, revT2, selection):
        return np.hstack((self.rev_vector[nonzero_columns], revT2[selection])) \
            if selection else self.rev_vector[nonzero_columns]

    @staticmethod
    def vstack_TandT2_based_on_selection(T, T2, nonzero_columns, selection):
        T = np.vstack((T[nonzero_columns, 1:], T2[selection, :])) if selection else T[nonzero_columns, 1:]
        return T

    def filter_rows_based_on_probability(self, T2):
        p = self.probability(T2.shape[0]) if T2.shape[0] else 0
        return [i for i in range(T2.shape[0]) if random() <= p]

    def prepare_vars(self, T, i):
        assert isinstance(T, np.ndarray)
        assert isinstance(i, int)
        nonzero_columns = np.nonzero(T[:, 0] == 0)[0]
        zero_columns = np.nonzero(T[:, 0])[0]
        T2 = np.zeros((0, T.shape[1] - 1))
        revT2 = np.zeros((0,))
        nrev = self.get_nrev(zero_columns)
        irr = self.get_irr()
        npos = self.get_npos(T, irr)
        nneg = self.get_nneg(T, irr)
        npairs = self.get_npairs(nneg, npos, nrev)
        pairs = self.generate_pairs(T, zero_columns)
        first_i_rows = self.get_first_i_rows(i)
        return T2, first_i_rows, nonzero_columns, npairs, pairs, revT2

    def get_minimal(self, Tj, Tjk, Tk, first_i_rows, i, m):
        minimal = all(np.abs(Tj[(m - i - 1):]) + np.abs(Tk[(m - i - 1):]) == np.abs(Tjk[(m - i - 1):])) \
                  and self._rank_test(first_i_rows, np.nonzero(Tjk[(m - i - 1):])[0])
        assert isinstance(minimal, np.bool_)
        return minimal

    def get_revTjk(self, j, k):
        revTjk = self.rev_vector[j] and self.rev_vector[k]  # will always be 0
        return revTjk

    @staticmethod
    def get_Tj_Tk(T, cj, ck, j, k):
        Tj, Tk = cj * T[j, 1:], ck * T[k, 1:]
        assert isinstance(Tj, np.ndarray) and len(Tj.shape) == 1
        assert isinstance(Tk, np.ndarray) and len(Tk.shape) == 1
        return Tj, Tk

    def get_cj_ck(self, T, j, k):
        if self.rev_vector[j] and self.rev_vector[k]:
            cj, ck = -T[k, 0], T[j, 0]
        elif self.rev_vector[j] and not self.rev_vector[k]:
            cj, ck = -np.sign(T[j, 0]) * T[k, 0], np.sign(T[j, 0]) * T[j, 0]
        elif not self.rev_vector[j] and self.rev_vector[k]:
            cj, ck = np.sign(T[k, 0]) * T[k, 0], -np.sign(T[k, 0]) * T[j, 0]
        else:
            cj, ck = abs(T[k, 0]), abs(T[j, 0])
        return cj, ck

    def get_first_i_rows(self, i):
        first_i_rows = self.matrix[:i + 1, :]
        assert isinstance(self.matrix, np.ndarray) and len(self.matrix.shape) == 2
        return first_i_rows

    def generate_pairs(self, T, zero_columns):
        pairs = ((j, k) for j in zero_columns for k in zero_columns
                 if k > j and (self.rev_vector[j] or self.rev_vector[k] or T[j, 0] * T[k, 0] < 0))
        return pairs

    @staticmethod
    def get_npairs(nneg, npos, nrev):
        npairs = int(nrev * (nrev - 1) / 2 + nrev * (npos + nneg) + npos * nneg)
        assert isinstance(npairs, int)
        return npairs

    @staticmethod
    def get_nneg(T, irr):
        nneg = len(np.nonzero(T[irr, 0] < 0)[0])
        assert isinstance(nneg, int)
        return nneg

    @staticmethod
    def get_npos(T, irr):
        npos = len(np.nonzero(T[irr, 0] > 0)[0])
        assert isinstance(npos, int)
        return npos

    def get_irr(self):
        irr = np.nonzero(self.rev_vector == 0)[0]  # shrinking on each iteration but an entire vector
        assert isinstance(irr, np.ndarray) and len(irr.shape) == 1
        return irr

    def get_nrev(self, zero_columns):
        nrev = len(np.nonzero(self.rev_vector[zero_columns])[0])
        assert isinstance(nrev, int)
        return nrev

    @staticmethod
    def check_reversibility_vector(reversibility_vector):
        reversibility_vector = np.array(reversibility_vector)
        assert isinstance(reversibility_vector, np.ndarray) and len(reversibility_vector.shape) == 1
        return reversibility_vector

    def sort_matrix_by_first_column(self, matrix):
        self.matrix = np.array(matrix)
        order = np.argsort(np.sum(np.abs(np.sign(self.matrix)), 1))
        return self.matrix[order, :]

    def probability(self, x):
        p = (lambda x: self.k / (self.k + float(x))) if self.k else 1
        try:
            p = int(p)
        except ValueError:
            print("Could not convert {} to int".format(p))
            raise
        return p

    @staticmethod
    def _rank_test(S, Sjk):
        if len(Sjk) > S.shape[0] + 1:
            return False
        else:
            return len(Sjk) - matrix_rank(S[:, Sjk]) == 1

    @staticmethod
    def _normalize(e):
        support = abs(e[np.nonzero(e)[0]])
        try:
            support = support.astype(int)
        except ValueError:
            print("Could not convert {} to array of int".format(support))
            raise
        n1 = reduce(gcd, support)  # greatest common denominator

        n2 = (min(support) * max(support)) ** 0.5  # geometric mean
        n = n1 if (1e-6 < n1 < 1e6) and (1e-6 < n2 < 1e6) else n2
        return e / n
