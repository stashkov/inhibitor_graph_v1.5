import networkx as nx


def example30():
    """Graph S1"""
    G = nx.DiGraph()

    G.add_node(1, name='Bacteria')
    G.add_node(2, name='Epithelial cells', isEssential='0')
    G.add_node(3, name='Complement', isEssential='1')
    G.add_node(4, name='Ag-Ab complex', isEssential='1')
    G.add_node(5, name='Pro-inflamatory cytokines (IL-1,6,TNF-alpha, beta)', isEssential='0')
    G.add_node(6, name='Recruited PMNs', isEssential='1')
    G.add_node(7, name='Activated Phagocytic Cells', isEssential='0')
    G.add_node(8, name='Other antibodies', isEssential='1')
    G.add_node(9, name='Complement fixing antibodies IgG, IgM', isEssential='1')
    G.add_node(10, name='Macrophages', isEssential='1')
    G.add_node(11, name='Th1 cells', isEssential='1')
    G.add_node(12, name='T0 cells', isEssential='0')
    G.add_node(13, name='Th2 cells', isEssential='0')
    G.add_node(14, name='B cells', isEssential='0')
    G.add_node(15, name='Th1 related cytokines (IFN- Gamma, TNF-beta, IL-2)', isEssential='1')
    G.add_node(16, name='Th2 related cytokines (IL-4, 10,13)', isEssential='0')
    G.add_node(17, name='Dendritic cells', isEssential='0')
    G.add_node(18, name='Phagocytosis')

    G.add_edge(1, 17, weight=0)
    G.add_edge(1, 4, weight=0)
    G.add_edge(1, 2, weight=0)
    G.add_edge(1, 3, weight=0)

    G.add_edge(2, 5, weight=0)

    G.add_edge(3, 7, weight=0)

    G.add_edge(4, 3, weight=0)
    G.add_edge(4, 7, weight=0)

    G.add_edge(5, 17, weight=0)
    G.add_edge(5, 6, weight=0)
    G.add_edge(5, 10, weight=0)

    G.add_edge(6, 7, weight=0)

    G.add_edge(7, 5, weight=0)
    G.add_edge(7, 18, weight=0)

    G.add_edge(8, 4, weight=0)
    G.add_edge(8, 8, weight=0)

    G.add_edge(9, 9, weight=0)
    G.add_edge(9, 3, weight=0)

    G.add_edge(10, 7, weight=0)

    G.add_edge(11, 15, weight=0)

    G.add_edge(12, 11, weight=0)
    G.add_edge(12, 13, weight=0)

    G.add_edge(13, 14, weight=0)
    G.add_edge(13, 16, weight=0)

    G.add_edge(14, 8, weight=0)
    G.add_edge(14, 9, weight=0)

    G.add_edge(15, 10, weight=0)
    G.add_edge(15, 17, weight=0)
    G.add_edge(15, 11, weight=0)
    G.add_edge(15, 16, weight=1)

    G.add_edge(16, 15, weight=1)
    G.add_edge(16, 5, weight=1)
    G.add_edge(16, 17, weight=0)
    G.add_edge(16, 13, weight=0)

    G.add_edge(17, 15, weight=0)
    G.add_edge(17, 16, weight=0)

    G.add_edge(18, 1, weight=1)
    return G


def example32S3():
    """Graph S3"""
    G = nx.DiGraph()
    G.add_node(1, name='CD28')
    G.add_node(2, name='CD4', isEssential='0')
    G.add_node(3, name='TCRlig')
    G.add_node(4, name='CD45', isEssential='0')
    G.add_node(5, name='TCRb', isEssential='1')
    G.add_node(6, name='SHP1', isEssential='0')
    G.add_node(7, name='Csk', isEssential='0')
    G.add_node(8, name='PAG', isEssential='0')
    G.add_node(9, name='Lckp2', isEssential='0')
    G.add_node(10, name='CbIb')
    G.add_node(11, name='Lckp1', isEssential='0')
    G.add_node(12, name='Fyn', isEssential='1')
    G.add_node(13, name='PI3K', isEssential='1')
    G.add_node(14, name='cCbIp1')
    G.add_node(15, name='SHIP-1')
    G.add_node(16, name='PIP3', isEssential='1')
    G.add_node(17, name='PDK1', isEssential='1')
    G.add_node(18, name='PTEN')
    G.add_node(19, name='PKB')
    G.add_node(20, name='TCRp', isEssential='1')
    G.add_node(21, name='SHP2')
    G.add_node(22, name='ABI', isEssential='1')
    G.add_node(23, name='Rlk', isEssential='0')
    G.add_node(24, name='cCbIp2', isEssential='0')
    G.add_node(25, name='Gab2', isEssential='0')
    G.add_node(26, name='ZAP70', isEssential='1')
    G.add_node(27, name='Ca', isEssential='1')
    G.add_node(28, name='CaM', isEssential='1')
    G.add_node(29, name='CaMK4')
    G.add_node(30, name='CaMK2', isEssential='1')
    G.add_node(31, name='cabin1')
    G.add_node(32, name='AKAP79')
    G.add_node(33, name='Calpr1')
    G.add_node(34, name='LAT', isEssential='1')
    G.add_node(35, name='SLP76', isEssential='1')
    G.add_node(36, name='Itk', isEssential='0')
    G.add_node(37, name='IP3', isEssential='1')
    G.add_node(38, name='Calcln')
    G.add_node(39, name='Vav1', isEssential='1')
    G.add_node(40, name='sh3bp2', isEssential='0')
    G.add_node(41, name='PLCgb', isEssential='1')
    G.add_node(42, name='PLCga', isEssential='1')
    G.add_node(43, name='DAG', isEssential='1')
    G.add_node(44, name='RasGRP1', isEssential='0')
    G.add_node(45, name='Vav3', isEssential='0')
    G.add_node(46, name='Grb2', isEssential='0')
    G.add_node(47, name='Sos', isEssential='0')
    G.add_node(48, name='GAPs')
    G.add_node(49, name='PKCth', isEssential='1')
    G.add_node(50, name='Rac1p1', isEssential='0')
    G.add_node(51, name='Rac1p2', isEssential='0')
    G.add_node(52, name='HPK1', isEssential='0')
    G.add_node(53, name='Cdc42', isEssential='0')
    G.add_node(54, name='Ras', isEssential='0')
    G.add_node(55, name='Ikkg', isEssential='1')
    G.add_node(56, name='MLK3', isEssential='0')
    G.add_node(57, name='MEKK1', isEssential='0')
    G.add_node(58, name='Raf', isEssential='0')
    G.add_node(59, name='CARD11')
    G.add_node(60, name='CARD11a', isEssential='1')
    G.add_node(61, name='Ikkab', isEssential='1')
    G.add_node(62, name='Gadd45')
    G.add_node(63, name='MKK4')
    G.add_node(64, name='MEK', isEssential='0')
    G.add_node(65, name='Bcl10')
    G.add_node(66, name='Malt1')
    G.add_node(67, name='IkB')
    G.add_node(68, name='p38')
    G.add_node(69, name='JNK')
    G.add_node(70, name='ERK', isEssential='0')
    G.add_node(71, name='SRE')
    G.add_node(72, name='Jun')
    G.add_node(73, name='Fos')
    G.add_node(74, name='Rsk')
    G.add_node(75, name='AP1')
    G.add_node(76, name='CREB')
    G.add_node(77, name='CRE')

    G.add_node(78, name='BAD')
    G.add_node(79, name='GSK3')
    G.add_node(80, name='NFkB')
    G.add_node(81, name='NFAT')
    G.add_node(82, name='bcat')
    G.add_node(83, name='Cyc1')
    G.add_node(84, name='p21c')
    G.add_node(85, name='p27k')
    G.add_node(86, name='FKHR')
    G.add_node(87, name='BclXL')
    G.add_node(88, name='p70S6K')
    G.add_node(132, name='Gads', isEssential='1')
    G.add_node(133, name='DGK', isEssential='0')

    G.add_edge(1, 10, weight=1)
    G.add_edge(1, 39, weight=0)
    G.add_edge(1, 13, weight=0)

    G.add_edge(2, 11, weight=0)

    G.add_edge(3, 5, weight=0)

    G.add_edge(4, 11, weight=0)
    G.add_edge(4, 12, weight=0)

    G.add_edge(5, 20, weight=0)
    G.add_edge(5, 12, weight=0)
    G.add_edge(5, 9, weight=0)
    G.add_edge(5, 133, weight=0)
    G.add_edge(5, 8, weight=1)

    G.add_edge(6, 11, weight=1)

    G.add_edge(7, 11, weight=1)

    G.add_edge(8, 7, weight=0)

    G.add_edge(9, 12, weight=0)
    G.add_edge(9, 13, weight=0)

    G.add_edge(10, 13, weight=1)

    G.add_edge(11, 6, weight=0)
    G.add_edge(11, 12, weight=0)
    G.add_edge(11, 23, weight=0)
    G.add_edge(11, 22, weight=0)

    G.add_edge(12, 8, weight=0)
    G.add_edge(12, 24, weight=0)
    G.add_edge(12, 20, weight=0)
    G.add_edge(12, 22, weight=0)

    G.add_edge(13, 16, weight=0)

    G.add_edge(14, 5, weight=1)
    G.add_edge(14, 26, weight=1)

    G.add_edge(15, 16, weight=1)

    G.add_edge(16, 17, weight=0)
    G.add_edge(16, 36, weight=0)

    G.add_edge(17, 19, weight=0)
    G.add_edge(17, 88, weight=0)
    G.add_edge(17, 49, weight=0)

    G.add_edge(18, 16, weight=1)

    G.add_edge(19, 79, weight=1)
    G.add_edge(19, 78, weight=1)
    G.add_edge(19, 84, weight=1)
    G.add_edge(19, 85, weight=1)
    G.add_edge(19, 86, weight=1)

    G.add_edge(20, 26, weight=0)

    # no outgoing edges for node 21

    G.add_edge(22, 70, weight=0)

    G.add_edge(23, 42, weight=0)

    G.add_edge(24, 42, weight=1)

    G.add_edge(25, 21, weight=0)
    G.add_edge(25, 35, weight=1)

    G.add_edge(26, 14, weight=0)
    G.add_edge(26, 25, weight=0)
    G.add_edge(26, 39, weight=0)
    G.add_edge(26, 40, weight=0)

    G.add_edge(27, 28, weight=0)

    G.add_edge(28, 29, weight=0)
    G.add_edge(28, 30, weight=0)
    G.add_edge(28, 38, weight=0)

    G.add_edge(29, 31, weight=1)

    G.add_edge(30, 61, weight=0)

    G.add_edge(31, 38, weight=1)

    G.add_edge(32, 38, weight=1)

    G.add_edge(33, 38, weight=1)

    G.add_edge(34, 25, weight=0)
    G.add_edge(34, 40, weight=0)
    G.add_edge(34, 41, weight=0)
    G.add_edge(34, 46, weight=0)
    G.add_edge(34, 52, weight=0)

    G.add_edge(35, 42, weight=0)

    G.add_edge(36, 42, weight=0)

    G.add_edge(37, 27, weight=0)

    G.add_edge(38, 81, weight=0)

    G.add_edge(39, 50, weight=0)
    G.add_edge(39, 49, weight=0)

    G.add_edge(40, 45, weight=0)

    G.add_edge(41, 42, weight=0)

    G.add_edge(42, 43, weight=0)
    G.add_edge(42, 37, weight=0)

    G.add_edge(43, 44, weight=0)
    G.add_edge(43, 49, weight=0)

    G.add_edge(44, 54, weight=0)

    G.add_edge(45, 51, weight=0)

    G.add_edge(46, 25, weight=0)
    G.add_edge(46, 47, weight=0)

    G.add_edge(47, 53, weight=0)
    G.add_edge(47, 54, weight=0)

    G.add_edge(48, 54, weight=1)

    G.add_edge(49, 55, weight=0)

    G.add_edge(50, 56, weight=0)

    G.add_edge(51, 71, weight=0)
    G.add_edge(51, 57, weight=0)

    G.add_edge(52, 56, weight=0)
    G.add_edge(52, 56, weight=0)

    G.add_edge(53, 57, weight=0)
    G.add_edge(53, 71, weight=0)

    G.add_edge(54, 58, weight=0)

    G.add_edge(55, 61, weight=0)

    G.add_edge(56, 63, weight=0)

    G.add_edge(57, 68, weight=0)
    G.add_edge(57, 69, weight=0)

    G.add_edge(58, 64, weight=0)

    G.add_edge(59, 60, weight=0)

    G.add_edge(60, 55, weight=0)

    G.add_edge(61, 67, weight=1)

    G.add_edge(62, 68, weight=1)

    G.add_edge(63, 69, weight=0)

    G.add_edge(64, 70, weight=0)

    G.add_edge(65, 60, weight=0)

    G.add_edge(66, 60, weight=0)

    G.add_edge(67, 80, weight=1)

    # 68 no outgoing edges

    G.add_edge(69, 72, weight=0)

    G.add_edge(70, 73, weight=0)
    G.add_edge(70, 74, weight=0)

    # 71 no outgoing edgse

    G.add_edge(72, 75, weight=0)

    G.add_edge(73, 75, weight=0)

    G.add_edge(74, 76, weight=0)

    # 75 no outgoing edges

    G.add_edge(76, 77, weight=0)

    # 77 no outgoing edges

    G.add_edge(78, 87, weight=1)

    G.add_edge(79, 82, weight=1)
    G.add_edge(79, 83, weight=1)

    # 80 - 88 no outgoing edges

    G.add_edge(132, 35, weight=0)
    G.add_edge(132, 25, weight=0)

    G.add_edge(133, 43, weight=1)

    return G


def example32S4():
    """Graph S4"""
    G = nx.DiGraph()
    G.add_node(1, name='CD28')
    G.add_node(2, name='CD4', isEssential='0')
    G.add_node(3, name='TCRlig')
    G.add_node(4, name='CD45', isEssential='0')
    G.add_node(5, name='TCRb', isEssential='1')
    G.add_node(6, name='SHP1', isEssential='0')
    G.add_node(7, name='Csk', isEssential='0')
    G.add_node(8, name='PAG', isEssential='0')
    G.add_node(9, name='Lckp2', isEssential='0')
    G.add_node(10, name='CbIb')
    G.add_node(11, name='Lckp1', isEssential='0')
    G.add_node(12, name='Fyn', isEssential='1')
    G.add_node(13, name='PI3K', isEssential='1')
    G.add_node(14, name='cCbIp1', isEssential='0')
    G.add_node(15, name='SHIP-1')
    G.add_node(16, name='PIP3', isEssential='1')
    G.add_node(17, name='PDK1')
    G.add_node(18, name='PTEN')
    G.add_node(19, name='PKB')
    G.add_node(20, name='TCRp', isEssential='1')
    G.add_node(21, name='SHP2')
    G.add_node(22, name='ABI', isEssential='1')
    G.add_node(23, name='Rlk', isEssential='0')
    G.add_node(24, name='cCbIp2', isEssential='0')
    G.add_node(25, name='Gab2', isEssential='0')
    G.add_node(26, name='ZAP70', isEssential='1')
    G.add_node(27, name='Ca')
    G.add_node(28, name='CaM')
    G.add_node(29, name='CaMK4')
    G.add_node(30, name='CaMK2')
    G.add_node(31, name='cabin1')
    G.add_node(32, name='AKAP79')
    G.add_node(33, name='Calpr1')
    G.add_node(34, name='LAT', isEssential='1')
    G.add_node(35, name='SLP76', isEssential='1')
    G.add_node(36, name='Itk', isEssential='0')
    G.add_node(37, name='IP3')
    G.add_node(38, name='Calcln')
    G.add_node(39, name='Vav1', isEssential='1')
    G.add_node(40, name='sh3bp2', isEssential='0')
    G.add_node(41, name='PLCgb', isEssential='1')
    G.add_node(42, name='PLCga', isEssential='1')
    G.add_node(43, name='DAG', isEssential='1')
    G.add_node(44, name='RasGRP1', isEssential='1')
    G.add_node(45, name='Vav3', isEssential='0')
    G.add_node(46, name='Grb2', isEssential='1')
    G.add_node(47, name='Sos', isEssential='1')
    G.add_node(48, name='GAPs')
    G.add_node(49, name='PKCth')
    G.add_node(50, name='Rac1p1', isEssential='0')
    G.add_node(51, name='Rac1p2', isEssential='0')
    G.add_node(52, name='HPK1', isEssential='0')
    G.add_node(53, name='Cdc42', isEssential='0')
    G.add_node(54, name='Ras', isEssential='1')
    G.add_node(55, name='Ikkg')
    G.add_node(56, name='MLK3', isEssential='0')
    G.add_node(57, name='MEKK1', isEssential='0')
    G.add_node(58, name='Raf', isEssential='1')
    G.add_node(59, name='CARD11')
    G.add_node(60, name='CARD11a')
    G.add_node(61, name='Ikkab')
    G.add_node(62, name='Gadd45')
    G.add_node(63, name='MKK4', isEssential='0')
    G.add_node(64, name='MEK', isEssential='1')
    G.add_node(65, name='Bcl10')
    G.add_node(66, name='Malt1')
    G.add_node(67, name='IkB')
    G.add_node(68, name='p38')
    G.add_node(69, name='JNK', isEssential='1')
    G.add_node(70, name='ERK', isEssential='1')
    G.add_node(71, name='SRE')
    G.add_node(72, name='Jun', isEssential='1')
    G.add_node(73, name='Fos', isEssential='1')
    G.add_node(74, name='Rsk')
    G.add_node(75, name='AP1')
    G.add_node(76, name='CREB')
    G.add_node(77, name='CRE')

    G.add_node(78, name='BAD')
    G.add_node(79, name='GSK3')
    G.add_node(80, name='NFkB')
    G.add_node(81, name='NFAT')
    G.add_node(82, name='bcat')
    G.add_node(83, name='Cyc1')
    G.add_node(84, name='p21c')
    G.add_node(85, name='p27k')
    G.add_node(86, name='FKHR')
    G.add_node(87, name='BclXL')
    G.add_node(88, name='p70S6K')

    G.add_node(132, name='Gads', isEssential='1')
    G.add_node(133, name='DGK', isEssential='0')

    G.add_edge(1, 10, weight=1)
    G.add_edge(1, 39, weight=0)
    G.add_edge(1, 13, weight=0)

    G.add_edge(2, 11, weight=0)

    G.add_edge(3, 5, weight=0)

    G.add_edge(4, 11, weight=0)
    G.add_edge(4, 12, weight=0)

    G.add_edge(5, 20, weight=0)
    G.add_edge(5, 12, weight=0)
    G.add_edge(5, 9, weight=0)
    G.add_edge(5, 133, weight=0)
    G.add_edge(5, 8, weight=1)

    G.add_edge(6, 11, weight=1)

    G.add_edge(7, 11, weight=1)

    G.add_edge(8, 7, weight=0)

    G.add_edge(9, 12, weight=0)
    G.add_edge(9, 13, weight=0)

    G.add_edge(10, 13, weight=1)

    G.add_edge(11, 6, weight=0)
    G.add_edge(11, 12, weight=0)
    G.add_edge(11, 23, weight=0)
    G.add_edge(11, 22, weight=0)

    G.add_edge(12, 8, weight=0)
    G.add_edge(12, 24, weight=0)
    G.add_edge(12, 20, weight=0)
    G.add_edge(12, 22, weight=0)

    G.add_edge(13, 16, weight=0)

    G.add_edge(14, 5, weight=1)
    G.add_edge(14, 26, weight=1)

    G.add_edge(15, 16, weight=1)

    G.add_edge(16, 17, weight=0)
    G.add_edge(16, 36, weight=0)

    G.add_edge(17, 19, weight=0)
    G.add_edge(17, 88, weight=0)
    G.add_edge(17, 49, weight=0)

    G.add_edge(18, 16, weight=1)

    G.add_edge(19, 79, weight=1)
    G.add_edge(19, 78, weight=1)
    G.add_edge(19, 84, weight=1)
    G.add_edge(19, 85, weight=1)
    G.add_edge(19, 86, weight=1)

    G.add_edge(20, 26, weight=0)

    # no outgoing edges for node 21

    G.add_edge(22, 70, weight=0)

    G.add_edge(23, 42, weight=0)

    G.add_edge(24, 42, weight=1)

    G.add_edge(25, 21, weight=0)
    G.add_edge(25, 35, weight=1)

    G.add_edge(26, 14, weight=0)
    G.add_edge(26, 25, weight=0)
    G.add_edge(26, 39, weight=0)
    G.add_edge(26, 40, weight=0)

    G.add_edge(27, 28, weight=0)

    G.add_edge(28, 29, weight=0)
    G.add_edge(28, 30, weight=0)
    G.add_edge(28, 38, weight=0)

    G.add_edge(29, 31, weight=1)

    G.add_edge(30, 61, weight=0)

    G.add_edge(31, 38, weight=1)

    G.add_edge(32, 38, weight=1)

    G.add_edge(33, 38, weight=1)

    G.add_edge(34, 25, weight=0)
    G.add_edge(34, 40, weight=0)
    G.add_edge(34, 41, weight=0)
    G.add_edge(34, 46, weight=0)
    G.add_edge(34, 52, weight=0)

    G.add_edge(35, 42, weight=0)

    G.add_edge(36, 42, weight=0)

    G.add_edge(37, 27, weight=0)

    G.add_edge(38, 81, weight=0)

    G.add_edge(39, 50, weight=0)
    G.add_edge(39, 49, weight=0)

    G.add_edge(40, 45, weight=0)

    G.add_edge(41, 42, weight=0)

    G.add_edge(42, 43, weight=0)
    G.add_edge(42, 37, weight=0)

    G.add_edge(43, 44, weight=0)
    G.add_edge(43, 49, weight=0)

    G.add_edge(44, 54, weight=0)

    G.add_edge(45, 51, weight=0)

    G.add_edge(46, 25, weight=0)
    G.add_edge(46, 47, weight=0)

    G.add_edge(47, 53, weight=0)
    G.add_edge(47, 54, weight=0)

    G.add_edge(48, 54, weight=1)

    G.add_edge(49, 55, weight=0)

    G.add_edge(50, 56, weight=0)

    G.add_edge(51, 71, weight=0)
    G.add_edge(51, 57, weight=0)

    G.add_edge(52, 56, weight=0)
    G.add_edge(52, 56, weight=0)

    G.add_edge(53, 57, weight=0)
    G.add_edge(53, 71, weight=0)

    G.add_edge(54, 58, weight=0)

    G.add_edge(55, 61, weight=0)

    G.add_edge(56, 63, weight=0)

    G.add_edge(57, 68, weight=0)
    G.add_edge(57, 69, weight=0)

    G.add_edge(58, 64, weight=0)

    G.add_edge(59, 60, weight=0)

    G.add_edge(60, 55, weight=0)

    G.add_edge(61, 67, weight=1)

    G.add_edge(62, 68, weight=1)

    G.add_edge(63, 69, weight=0)

    G.add_edge(64, 70, weight=0)

    G.add_edge(65, 60, weight=0)

    G.add_edge(66, 60, weight=0)

    G.add_edge(67, 80, weight=1)

    # 68 no outgoing edges

    G.add_edge(69, 72, weight=0)

    G.add_edge(70, 73, weight=0)
    G.add_edge(70, 74, weight=0)

    # 71 no outgoing edgse

    G.add_edge(72, 75, weight=0)

    G.add_edge(73, 75, weight=0)

    G.add_edge(74, 76, weight=0)

    # 75 no outgoing edges

    G.add_edge(76, 77, weight=0)

    # 77 no outgoing edges

    G.add_edge(78, 87, weight=1)

    G.add_edge(79, 82, weight=1)
    G.add_edge(79, 83, weight=1)

    # 80 - 88 no outgoing edges

    G.add_edge(132, 35, weight=0)
    G.add_edge(132, 25, weight=0)

    G.add_edge(133, 43, weight=1)

    return G


def example31S2():
    """Graph S2"""
    G = nx.DiGraph()
    G.add_node(1, name='ABA')
    G.add_node(2, name='PEPC')

    G.add_node(3, name='RCN1', isEssential='0')

    G.add_node(4, name='NOS', isEssential='0')
    G.add_node(5, name='Arg')
    G.add_node(6, name='NIA12', isEssential='0')
    G.add_node(7, name='Nitrite')
    G.add_node(8, name='NADPH')

    G.add_node(9, name='Sph')
    G.add_node(10, name='SphK', isEssential='1')
    G.add_node(11, name='Malate')
    G.add_node(12, name='NO', isEssential='0')
    G.add_node(13, name='S1P', isEssential='1')
    G.add_node(14, name='OST1', isEssential='1')
    G.add_node(15, name='GCR1')
    G.add_node(16, name='GPA1', isEssential='1')
    G.add_node(17, name='AGB1', isEssential='1')

    G.add_node(18, name='PLC', isEssential='0')
    G.add_node(19, name='PIP2')
    G.add_node(20, name='NAD+')
    G.add_node(21, name='ADPRc', isEssential='0')
    G.add_node(22, name='GTP')
    G.add_node(23, name='GC', isEssential='0')
    G.add_node(24, name='InsPK', isEssential='0')

    G.add_node(25, name='PLD', isEssential='1')
    G.add_node(26, name='PC')
    G.add_node(27, name='NADPH')
    G.add_node(28, name='Atrboh', isEssential='1')
    G.add_node(29, name='DAG')
    G.add_node(30, name='InsP3', isEssential='0')
    G.add_node(31, name='cADPR', isEssential='0')
    G.add_node(32, name='cGMP', isEssential='0')
    G.add_node(33, name='InsP6', isEssential='0')
    G.add_node(34, name='RAC1')
    G.add_node(35, name='PA', isEssential='1')
    G.add_node(36, name='ROS', isEssential='1')
    G.add_node(37, name='CIS', isEssential='0')
    G.add_node(38, name='ABH1', isEssential='0')
    G.add_node(39, name='ROP2', isEssential='1')
    G.add_node(40, name='Actin', isEssential='1')
    G.add_node(41, name='ABI1', isEssential='0')
    G.add_node(42, name='pHc', isEssential='1')
    G.add_node(43, name='ROP10')
    G.add_node(44, name='ERA1', isEssential='0')
    G.add_node(45, name='CaIM', isEssential='0')
    G.add_node(46, name='H+ATPase', isEssential='0')

    G.add_node(47, name='Ca2+ATPase', isEssential='0')
    G.add_node(48, name='Ca2+', isEssential='1')
    G.add_node(49, name='KEV', isEssential='0')
    G.add_node(50, name='Depolar', isEssential='1')
    G.add_node(51, name='AnionEM', isEssential='1')
    G.add_node(52, name='KAP', isEssential='0')
    G.add_node(53, name='KOUT', isEssential='1')
    G.add_node(54, name='AtPP2C')
    G.add_node(55, name='Closure')

    G.add_edge(1, 18, weight=0)
    G.add_edge(1, 3, weight=0)
    G.add_edge(1, 24, weight=0)
    G.add_edge(1, 34, weight=1)
    G.add_edge(1, 10, weight=0)
    G.add_edge(1, 14, weight=0)
    G.add_edge(1, 42, weight=0)
    G.add_edge(1, 11, weight=1)
    G.add_edge(1, 2, weight=1)

    G.add_edge(2, 11, weight=0)

    G.add_edge(3, 6, weight=0)

    G.add_edge(4, 12, weight=0)
    G.add_edge(5, 12, weight=0)
    G.add_edge(6, 12, weight=0)
    G.add_edge(7, 12, weight=0)
    G.add_edge(8, 12, weight=0)

    G.add_edge(9, 13, weight=0)
    G.add_edge(10, 13, weight=0)

    G.add_edge(11, 55, weight=1)

    G.add_edge(12, 21, weight=0)
    G.add_edge(13, 16, weight=0)

    G.add_edge(14, 28, weight=0)

    G.add_edge(15, 16, weight=1)

    G.add_edge(16, 25, weight=0)

    G.add_edge(17, 16, weight=0)

    G.add_edge(18, 29, weight=0)
    G.add_edge(18, 30, weight=0)

    G.add_edge(19, 29, weight=0)
    G.add_edge(19, 30, weight=0)

    G.add_edge(20, 31, weight=0)

    G.add_edge(21, 31, weight=0)

    G.add_edge(22, 32, weight=0)

    G.add_edge(23, 32, weight=0)

    G.add_edge(24, 33, weight=0)

    G.add_edge(25, 35, weight=0)

    G.add_edge(26, 35, weight=0)

    G.add_edge(27, 36, weight=0)

    G.add_edge(28, 36, weight=0)

    # node 29 has no out edges

    G.add_edge(30, 37, weight=0)

    G.add_edge(31, 37, weight=0)

    G.add_edge(32, 37, weight=0)

    G.add_edge(33, 37, weight=0)

    G.add_edge(34, 40, weight=1)

    G.add_edge(35, 39, weight=0)
    G.add_edge(35, 41, weight=1)

    G.add_edge(36, 45, weight=0)
    G.add_edge(36, 46, weight=1)
    G.add_edge(36, 41, weight=1)
    G.add_edge(36, 53, weight=1)

    G.add_edge(37, 48, weight=0)

    G.add_edge(38, 45, weight=1)

    G.add_edge(39, 28, weight=0)

    G.add_edge(40, 55, weight=0)

    G.add_edge(41, 34, weight=0)
    G.add_edge(41, 28, weight=1)
    G.add_edge(41, 51, weight=1)

    G.add_edge(42, 28, weight=0)
    G.add_edge(42, 41, weight=0)
    G.add_edge(42, 46, weight=1)
    G.add_edge(42, 53, weight=0)
    G.add_edge(42, 52, weight=1)
    G.add_edge(42, 51, weight=0)

    # node 43 has not out edges

    G.add_edge(44, 43, weight=0)
    G.add_edge(44, 45, weight=1)

    G.add_edge(45, 48, weight=0)

    G.add_edge(46, 50, weight=1)

    G.add_edge(47, 48, weight=1)

    G.add_edge(48, 47, weight=0)
    G.add_edge(48, 18, weight=0)
    G.add_edge(48, 4, weight=0)
    G.add_edge(48, 52, weight=1)
    G.add_edge(48, 50, weight=0)
    G.add_edge(48, 49, weight=0)
    G.add_edge(48, 51, weight=0)
    G.add_edge(48, 46, weight=1)
    G.add_edge(48, 40, weight=0)

    G.add_edge(49, 50, weight=0)

    G.add_edge(50, 45, weight=1)
    G.add_edge(50, 52, weight=0)
    G.add_edge(50, 53, weight=0)

    G.add_edge(51, 50, weight=0)
    G.add_edge(51, 11, weight=1)
    G.add_edge(51, 55, weight=0)

    G.add_edge(52, 50, weight=1)
    G.add_edge(52, 55, weight=0)

    G.add_edge(53, 50, weight=1)
    G.add_edge(53, 55, weight=0)

    G.add_edge(54, 55, weight=1)

    # node 55 has no out edges

    return G

