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

## Upgrade

### PyPI
```Python
pip install automathon --upgrade
```

## Basic Example

## Deterministic Finite Automata

![](https://upload.wikimedia.org/wikipedia/commons/9/94/DFA_example_multiplies_of_3.svg)

Self-made, Public domain, via Wikimedia Commons

### Representing the previous automata

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

### Verify if the automata is valid

```Python
automata1.isValid()   #True
```

### Verify if the automata accept a string

```Python
automata1.accept("001001")   #True
automata1.accept("00100")    #False
```

### Get the automata's complement

```Python
notautomata1 = automata1.complement()
notautomata1.accept("00100")    #True
```


## Non-Deterministic Finite Automata
![](http://www.r9paul.org/wp-content/uploads/2008/12/nfa_example.jpg)

Image taken from: http://www.r9paul.org/blog/2008/nondeterministic-finite-state-machine/

### Representing the previous automata

```Python
from automathon import NFA

## Epsilon Transition is denoted by '' -> Empty string
Q = {'q1', 'q2', 'q3', 'q4'}
sigma = {'0', '1'}
delta = {
          'q1' : {
                  '0' : ['q1'],
                  '1' : ['q1', 'q2']
                  },
          'q2' : {
                  '0' : ['q3'],
                  '' : ['q3']
                  },
          'q3' : {
                  '1' : ['q4'],
                  },
          'q4' : {
                  '0' : ['q4'],
                  '1' : ['q4'],
                  },
        }
initialState = 'q1'
F = {'q4'}

automata2 = NFA(Q, sigma, delta, initialState, F)
## This is an example about creating a NFA with the library
```

### Verify if the automata is valid

```Python
automata2.isValid()   #True
```

### Verify if the automata accept a string

```Python
automata2.accept("0000011")   #True
automata2.accept("000001")    #False
```

### Get the automata's complement

```Python
notautomata2 = automata1.complement()
notautomata2.accept("000001")    #True
```

### Visualize the automata

For both, DFA and NFA, the view method enables to visualize the automaton, recives as parameter a String as the file name for the png and svg files.

```Python
automata1.view("DFA Visualization")
automata2.view("NFA Visualization")
```

## Remove Epsilon transitions from NFA

```
automata3 = automata2.removeEpsilonTransitions()
automata3.view("NFA without EpsilonTransitions")
```

## Convert NFA to DFA

```
automata4 = automata3.getDFA()
automata4.view("NFA to DFA")
```

### Errors

Errors that can be returned during the execution and the cases that can appear.

- **SigmaError**:
  - The automata contains a initial state or a final state that's not defined on Q.
  - The automata contains a delta transition that's not defined on Q or in Sigma.

- **InputError**:
  - The automata is trying to consume an letter that's not defined in sigma.
