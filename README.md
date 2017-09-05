<a href="https://codeclimate.com/github/codeclimate/codeclimate"><img src="https://codeclimate.com/github/codeclimate/codeclimate/badges/gpa.svg" /></a>

# What is this?
Signal2RGraph is a biological tool, that helps to calculate all
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

`python main.py edge_list.csv`

### How to create edge list?
Suppose
GRK2 is activated by cAMP and GEF1 is inhibited by GRK2.

This means we have cAMP -> GRK2 -| GEF1.
We can represent these edges as follows:
```
cAMP, GRK2, ACTIVATION
GRK2, GEF1, INHIBITION
```


Note: Because the delimiter is a comma symbol `,`,
the use of `""` is only necessary when you have
comma symbol inside name of the node (e.g. "Complex II, III, IV").

Example file can be found in `examples` folder

# Results
Results can be found in `result` folder. It contains:
- EFM in human readable format (node names from input file)
- EFM with numbers instead of node names
- Original imported graph from edge list and node names as GraphML
- Expanded graph as GraphML