# What is this?
It's a biological tool, that helps to calculate all
EFM (elementary flux modes) in a given metabolic pathway.


# How does it expand a metabolic pathway?
For detailed explanation please refer to the article [article_name]

In short:
1. Each activation reaction produces 3 reactions
2. Each inhibition reaction produces 2 reactions
3. Reactions are then placed into stoichiometric matrix
4. Based on the matrix calculate EFMs


# How do I use it?
#### Execute
`python main.py path_to_file_with_nodes.txt path_to_file_with_edges.txt`

#### What should be inside node file?
File with node suppose to be node names.

For example I have 3 nodes,
each of which represent an enzyme. cAMP, GRK2 and GEF1.
Therefore my file should look like this:
```
cAMP
GRK2
GEF1
```

It will assign GRK2 to node 1, and cAMP to node 2.


#### What should be inside edges file?
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

#### What is the result?
Result is reactions, that correspond to chosen EFMs.
