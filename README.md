# What is this?
It's a biological tool, that helps to calculate all
EFM (elementary flux modes) in a given metabolic pathway.


# How does it work?
For detailed explanation please refer to the article [article_name]

In short:
1. Each activation reaction produces 3 reactions
2. Each inhibition reaction produces 2 reactions
3. Reactions are then placed into stoichiometric matrix
4. Based on the matrix calculate EFMs


# How to use it?
### Python version
Main interpreter is python3,
but I try to keep it compatible with python 2 as well

### Getting started
`pip install -r requirements.txt`

`git clone git@github.com:stashkov/inhibitor_graph_v1.5.git`

`cd inhibitor_graph_v1.5`

`python main.py node_names.txt edge_list.txt`

### How to create node names file?
For example we have graph with 3 nodes,
each of which represent an enzyme: cAMP, GRK2 and GEF1.
Therefore the file should look like this:
```
cAMP
GRK2
GEF1
```

It will assign
- cAMP to node 1
- GRK2 to node 2
- GEF1 to node 3

Example file can be found in `examples` folder

### How to create edge list?
Suppose
GRK2 is activated by cAMP and GEF1 is inhibited by GRK2.

This means we have cAMP -> GRK2 -| GEF1.
Activation is represented by 0 and inhibition by 1.

According to the numbering of nodes from previous section
we can represent these edges as follows:
```
1 2 0
2 3 1
```
It will create
- edge 1 to 2 with weight 0
- edge 2 to 3 with weight 1

Example file can be found in `examples` folder

### What is the result?
Result is reactions, that correspond to chosen EFMs. (see below)


# Results
Results can be found in `result` folder. It contains:
- EFM in human readable format (node names from input file)
- EFM with numbers instead of node names
- Original imported graph from edge list and node names as GraphML
- Expanded graph as GraphML