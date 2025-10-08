### Prerequisites:
```
pip install ply matplotlib networkx pygraphviz pydot
```
### Usage:
Run maincli.py for the intended command line usage.

Commands:
/show variable\_name : plots the tree pair associated with the variable\_name 
/make\_revealing() : shockingly not yet implemented (will fix this)

We allow definition of group elements using explicit antichains and from dfs bitstrings.

/def\_from\_achains(antichain1,antichain2, permutation) : where antichains are given as comma separated square bracketed lists of binary words enclosed in '' or "". Examples ["0", "1"] or ['1','0']. And the permutation is given as a square bracket comma separated list of numbers. Examples [0,1,2,3]
/def\_from\_dfs(antichain1, antichain2, dfs_bitstring) : TODO explain dfsbitstring

The regular group operations are given by:
a\*b : compose
\!a : invert
a^b : conjugation

We define a new variable by ':='
```
var_name := expression
``` 

Where the var\_name is a string of characters not starting with a number and the expression is any combination of brackettings with '()' and our group operations done on existing variables.

We may also see the action of a tree pair on a finite bitstring by:
```
bitstring | var_name 
Examples: 
`0101`|f, for f being previously defined with := .
```

#### Known bugs/(features?):
1. Variables are case-sensitive (feature)
2. /show expression doesnt work, but d := expression, then /show d works. (bug)
3. Defined variables are deleted on output (feature: but I plan to implement a saved state, to fix this.)

