### Prerequisites:

Graphviz required:
https://pygraphviz.github.io/documentation/stable/install.html
```
pip install ply matplotlib networkx pygraphviz pydot tkinter
```
### Usage:
Run ui.py for the GUI. (intended)

#### Slash commands:
```
/show variable_name : plots the tree pair associated with the variable_name 
/print variable_name : Writes the antichains to the log.
/help : Displays the available commands.
/clear : Clears the drawns tree pairs
/var : Shows the currently available variables.
```

#### Inline commands: 

We allow definition of group elements using explicit antichains and from dfs bitstrings, using inline commands.

```
def_from_achains(antichain1,antichain2, permutation)
```
where antichains are given as comma separated square bracketed lists of binary words enclosed in '' or "". Examples ["0", "1"] or ['1','0']. And the permutation is given as a square bracket comma separated list of numbers. Examples [0,1,2,3]
```
def_from_dfs(dfs_bitstring1, dfs_bitstring2, permutation)
```
TODO explain dfsbitstring
```
b := def_from_achains(...)
```

#### Other inline commands:
```
revealing(varname) : returns a revealing pair for the given tree pair. 
```

#### Algebraic operations:
```
a*b : compose
!a : invert
a^b : conjugation (b^-1 * a * b)
a#b : commutators (a^-1 * b^-1 * a * b)
```

We define a new variable by ':='
```
var_name := expression
``` 

Where the var\_name is a string of alpha-numeric characters not starting with a number and the expression is any combination of brackettings with '()' and our group operations done on existing variables.

We may also see the action of a tree pair on a finite bitstring by:
```
bitstring | var_name 
Examples: 
`0101`|f, for f being previously defined with := .
```

#### Known bugs/(features?):
1. Variables are case-sensitive (feature)
2. /show expression doesnt work, but d := expression, then /show d works. (bug)
3. Variables are not saved on stopping the script.(feature: but I plan to implement a saved state, to fix this.)
4. The current restrictions on what is a variable or an expression and the restrictions on what characters are allowed are a bit inconsistent. (bug: This requires messing with the parser's grammar but I will change this to be more consistent.)
5. The labelling of leaves in the tree pair drawing is incorrect! (bug: major)
6. /show command does not work on certain terminals. (bug: working on a fix)

