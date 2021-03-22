# Automathon

Created by: Robin Hafid Quintero Lopez

[![Build Status](https://travis-ci.com/rohaquinlop/automathon.svg?branch=main)](https://travis-ci.com/rohaquinlop/automathon)

A Python library for simulating finite automata

## Links
- GitHub repository: https://github.com/rohaquinlop/automathon
- PyPI: https://pypi.org/project/automathon/
- Twitter: https://twitter.com/RobinHafid
- Contact: rohaquinlop301@gmail.com

## Installation

### PyPI
```Python
pip install automathon
```

## Basic Example

![](https://upload.wikimedia.org/wikipedia/commons/9/94/DFA_example_multiplies_of_3.svg)
Self-made, Public domain, via Wikimedia Commons

##### Representing the previous automata

```Python
from automathon import DFA
Q = {'q0', 'q1', 'q2'}
sigma = {'0', '1'}
delta = { 'q0' : {'0' : 'q0', '1' : 'q1'},
          'q1' : {'0' : 'q2', '1' : 'q0'},
          'q2' : {'0' : 'q1', '1' : 'q2'}
        }
initialState = 'q0'
F = {'q0'}

automata1 = DFA(Q, sigma, delta, initialState, F)
## This is an example about creating a DFA with the library
```

###### Verify if the automata is valid

```Python
automata1.isValid()   #True
```

###### Verify if the automata accept a string

```Python
automata1.accept("001001")   #True
automata1.accept("00100")    #False
```
