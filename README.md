[![stablebuild](https://travis-ci.org/stashkov/Signal2RGraph.svg?branch=master)](https://travis-ci.org/stashkov/Signal2RGraph)
[![codeclimate](https://codeclimate.com/github/stashkov/Signal2RGraph/badges/gpa.svg)](https://codeclimate.com/github/stashkov/Signal2RGraph/issues)
[![codecov](https://codecov.io/gh/stashkov/Signal2RGraph/branch/master/graph/badge.svg)](https://codecov.io/gh/stashkov/Signal2RGraph)
[![DOI](https://zenodo.org/badge/99731542.svg)](https://zenodo.org/badge/latestdoi/99731542)

__Signal2RGraph__ is a biological tool, that helps to calculate all
EFM (elementary flux modes) in a given metabolic pathway.


# How does it work?
For detailed explanation please refer to the [article][Engelhardt_et_al]

In short:
1. Each activation reaction produces 3 reactions
2. Each inhibition reaction produces 2 reactions
3. Reactions are then placed into stoichiometric matrix
4. Based on the matrix calculate EFMs


# How to use it?

### Getting started ![alt text][python_versions]
```python
pip install -r requirements.txt
git clone git@github.com:stashkov/Signal2RGraph.git
cd Signal2RGraph
python main.py edge_list.csv
```
### How to create edge list?
Suppose
GRK2 is activated by cAMP and GEF1 is inhibited by GRK2.

This means we have cAMP -> GRK2 -| GEF1.
We can represent these edges as follows:
```
cAMP, GRK2, ACTIVATION
GRK2, GEF1, INHIBITION
```


Note: The use of `""` is only necessary when you have a
comma inside the name of a node (e.g. "Complex II, III, IV").

Example file can be found in `examples` folder

# Results
Results can be found in `result` folder. It contains:
- EFM in human readable format (node names from input file)
- EFM with numbers instead of node names
- Original imported graph from edge list and node names as GraphML
- Expanded graph as GraphML


[python_versions]: https://img.shields.io/pypi/pyversions/PyBEL.svg "Stable Supported Python Versions"
[Engelhardt_et_al]: https://academic.oup.com/imammb/article/doi/10.1093/imammb/dqx003/3827653/Modelling-and-mathematical-analysis-of-the-M-2 "Oxford Academic"




