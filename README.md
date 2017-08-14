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
### Execute
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


# Example output
```
Total number of EFMs 28
EFM #1
First Reaction: PKA (cAMP dependent) + not GRK 2 <-> PKA (cAMP dependent) : GRK 2
Second Reaction: PKA (cAMP dependent) : GRK 2 -> PKA (cAMP dependent) + GRK 2
Third Reaction: GRK 2 -> not GRK 2

EFM #2
First Reaction: cAMP + not PKA (cAMP dependent) <-> cAMP : PKA (cAMP dependent)
Second Reaction: cAMP : PKA (cAMP dependent) -> cAMP + PKA (cAMP dependent)
Third Reaction: PKA (cAMP dependent) -> not PKA (cAMP dependent)

EFM #3
First Reaction: PKA (cAMP dependent) + not GRK 6 <-> PKA (cAMP dependent) : GRK 6
Second Reaction: PKA (cAMP dependent) : GRK 6 -> PKA (cAMP dependent) + GRK 6
Third Reaction: GRK 6 -> not GRK 6

EFM #4
First Reaction: ACM2 + not G-Protein alpha-s <-> ACM2 : G-Protein alpha-s
Second Reaction: ACM2 : G-Protein alpha-s -> ACM2 + G-Protein alpha-s
Third Reaction: G-Protein alpha-s -> not G-Protein alpha-s

EFM #5
First Reaction: ACM2 + not G-Protein beta/gamma <-> ACM2 : G-Protein beta/gamma
Second Reaction: ACM2 : G-Protein beta/gamma -> ACM2 + G-Protein beta/gamma
Third Reaction: G-Protein beta/gamma -> not G-Protein beta/gamma

EFM #6
First Reaction: cAMP-GEF1 + not RGS 14 <-> cAMP-GEF1 : RGS 14
Second Reaction: cAMP-GEF1 : RGS 14 -> cAMP-GEF1 + RGS 14
Third Reaction: RGS 14 -> not RGS 14

EFM #7
Third Reaction: RGS 14 -> not RGS 14
First Reaction: PKA (cAMP dependent) + not RGS 14 <-> PKA (cAMP dependent) : RGS 14
Second Reaction: PKA (cAMP dependent) : RGS 14 -> PKA (cAMP dependent) + RGS 14

EFM #8
Third Reaction: AMP -> not AMP
First Reaction: cAMP + not AMP <-> cAMP : AMP
Second Reaction: cAMP : AMP -> cAMP + AMP

EFM #9
First Reaction: PKA (cAMP dependent) + not AMP <-> PKA (cAMP dependent) : AMP
Second Reaction: PKA (cAMP dependent) : AMP -> PKA (cAMP dependent) + AMP
Third Reaction: AMP -> not AMP

EFM #10
First Reaction: Adenylate cyclase subtypes II/IV/VII + not cAMP <-> Adenylate cyclase subtypes II/IV/VII : cAMP
Second Reaction: Adenylate cyclase subtypes II/IV/VII : cAMP -> Adenylate cyclase subtypes II/IV/VII + cAMP
Third Reaction: cAMP -> not cAMP

EFM #11
Third Reaction: cAMP -> not cAMP
First Reaction: Adenylate cyclase subtypes V/VI + not cAMP <-> Adenylate cyclase subtypes V/VI : cAMP
Second Reaction: Adenylate cyclase subtypes V/VI : cAMP -> Adenylate cyclase subtypes V/VI + cAMP

EFM #12
First Reaction: ACM2 + not G-Protein alpha -o <-> ACM2 : G-Protein alpha -o
Second Reaction: ACM2 : G-Protein alpha -o -> ACM2 + G-Protein alpha -o
Third Reaction: G-Protein alpha -o -> not G-Protein alpha -o

EFM #13
First Reaction: ACM2 + not G-Protein alpha -o <-> ACM2 : G-Protein alpha -o
Second Reaction: ACM2 : G-Protein alpha -o -> ACM2 + G-Protein alpha -o
First Reaction: RGS 14 + G-Protein alpha -o <-> RGS 14 : not G-Protein alpha -o
Second Reaction: RGS 14 : not G-Protein alpha -o -> RGS 14 + not G-Protein alpha -o

EFM #14
First Reaction: ACM2 + not G-Protein alpha -i <-> ACM2 : G-Protein alpha -i
Second Reaction: ACM2 : G-Protein alpha -i -> ACM2 + G-Protein alpha -i
Third Reaction: G-Protein alpha -i -> not G-Protein alpha -i

EFM #15
First Reaction: ACM2 + not G-Protein alpha -i <-> ACM2 : G-Protein alpha -i
Second Reaction: ACM2 : G-Protein alpha -i -> ACM2 + G-Protein alpha -i
First Reaction: RGS 14 + G-Protein alpha -i <-> RGS 14 : not G-Protein alpha -i
Second Reaction: RGS 14 : not G-Protein alpha -i -> RGS 14 + not G-Protein alpha -i

EFM #16
First Reaction: cAMP + not cAMP-GEF1 <-> cAMP : cAMP-GEF1
Second Reaction: cAMP : cAMP-GEF1 -> cAMP + cAMP-GEF1
Third Reaction: cAMP-GEF1 -> not cAMP-GEF1

EFM #17
First Reaction: GRK 2 + cAMP-GEF1 <-> GRK 2 : not cAMP-GEF1
Second Reaction: GRK 2 : not cAMP-GEF1 -> GRK 2 + not cAMP-GEF1
First Reaction: cAMP + not cAMP-GEF1 <-> cAMP : cAMP-GEF1
Second Reaction: cAMP : cAMP-GEF1 -> cAMP + cAMP-GEF1

EFM #18
First Reaction: G-Protein beta/gamma + not Adenylate cyclase subtypes II/IV/VII <-> G-Protein beta/gamma : Adenylate cyclase subtypes II/IV/VII
Second Reaction: G-Protein beta/gamma : Adenylate cyclase subtypes II/IV/VII -> G-Protein beta/gamma + Adenylate cyclase subtypes II/IV/VII
Third Reaction: Adenylate cyclase subtypes II/IV/VII -> not Adenylate cyclase subtypes II/IV/VII

EFM #19
Third Reaction: Adenylate cyclase subtypes II/IV/VII -> not Adenylate cyclase subtypes II/IV/VII
First Reaction: G-Protein alpha-s + not Adenylate cyclase subtypes II/IV/VII <-> G-Protein alpha-s : Adenylate cyclase subtypes II/IV/VII
Second Reaction: G-Protein alpha-s : Adenylate cyclase subtypes II/IV/VII -> G-Protein alpha-s + Adenylate cyclase subtypes II/IV/VII

EFM #20
First Reaction: G-Protein alpha-s + not Adenylate cyclase subtypes V/VI <-> G-Protein alpha-s : Adenylate cyclase subtypes V/VI
Second Reaction: G-Protein alpha-s : Adenylate cyclase subtypes V/VI -> G-Protein alpha-s + Adenylate cyclase subtypes V/VI
Third Reaction: Adenylate cyclase subtypes V/VI -> not Adenylate cyclase subtypes V/VI

EFM #21
First Reaction: G-Protein beta/gamma + Adenylate cyclase subtypes V/VI <-> G-Protein beta/gamma : not Adenylate cyclase subtypes V/VI
Second Reaction: G-Protein beta/gamma : not Adenylate cyclase subtypes V/VI -> G-Protein beta/gamma + not Adenylate cyclase subtypes V/VI
First Reaction: G-Protein alpha-s + not Adenylate cyclase subtypes V/VI <-> G-Protein alpha-s : Adenylate cyclase subtypes V/VI
Second Reaction: G-Protein alpha-s : Adenylate cyclase subtypes V/VI -> G-Protein alpha-s + Adenylate cyclase subtypes V/VI

EFM #22
First Reaction: G-Protein alpha-s + not Adenylate cyclase subtypes V/VI <-> G-Protein alpha-s : Adenylate cyclase subtypes V/VI
Second Reaction: G-Protein alpha-s : Adenylate cyclase subtypes V/VI -> G-Protein alpha-s + Adenylate cyclase subtypes V/VI
First Reaction: G-Protein alpha -i + Adenylate cyclase subtypes V/VI <-> G-Protein alpha -i : not Adenylate cyclase subtypes V/VI
Second Reaction: G-Protein alpha -i : not Adenylate cyclase subtypes V/VI -> G-Protein alpha -i + not Adenylate cyclase subtypes V/VI

EFM #23
First Reaction: G-Protein alpha-s + not Adenylate cyclase subtypes V/VI <-> G-Protein alpha-s : Adenylate cyclase subtypes V/VI
Second Reaction: G-Protein alpha-s : Adenylate cyclase subtypes V/VI -> G-Protein alpha-s + Adenylate cyclase subtypes V/VI
First Reaction: PKA (cAMP dependent) + Adenylate cyclase subtypes V/VI <-> PKA (cAMP dependent) : not Adenylate cyclase subtypes V/VI
Second Reaction: PKA (cAMP dependent) : not Adenylate cyclase subtypes V/VI -> PKA (cAMP dependent) + not Adenylate cyclase subtypes V/VI

EFM #24
Third Reaction: Tubulin, Actin -> not Tubulin, Actin
First Reaction: AMP + not Tubulin, Actin <-> AMP : Tubulin, Actin
Second Reaction: AMP : Tubulin, Actin -> AMP + Tubulin, Actin

EFM #25
First Reaction: G-Protein alpha -o + not Tubulin, Actin <-> G-Protein alpha -o : Tubulin, Actin
Second Reaction: G-Protein alpha -o : Tubulin, Actin -> G-Protein alpha -o + Tubulin, Actin
Third Reaction: Tubulin, Actin -> not Tubulin, Actin

EFM #26
Third Reaction: Tubulin, Actin -> not Tubulin, Actin
First Reaction: cAMP-GEF1 + not Tubulin, Actin <-> cAMP-GEF1 : Tubulin, Actin
Second Reaction: cAMP-GEF1 : Tubulin, Actin -> cAMP-GEF1 + Tubulin, Actin

EFM #27
Third Reaction: Tubulin, Actin -> not Tubulin, Actin
First Reaction: GRK 2 + not Tubulin, Actin <-> GRK 2 : Tubulin, Actin
Second Reaction: GRK 2 : Tubulin, Actin -> GRK 2 + Tubulin, Actin

EFM #28
Third Reaction: Tubulin, Actin -> not Tubulin, Actin
First Reaction: PKA (cAMP dependent) + not Tubulin, Actin <-> PKA (cAMP dependent) : Tubulin, Actin
Second Reaction: PKA (cAMP dependent) : Tubulin, Actin -> PKA (cAMP dependent) + Tubulin, Actin
```