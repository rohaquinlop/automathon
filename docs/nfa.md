# Non-Deterministic Finite Automata - NFA

`NFA` is the class used in automathon to represent a Non-Deterministic Finite
Automata.

## Attributes

Here are the attributes of the `NFA` class:

- `q` (`set[str]`): Set of strings where each string is a state of the automata.
- `sigma` (`set[str]`): Set of strings where each string is a symbol of the
    alphabet, the length of each string must be 1. The empty string is allowed in
    the `NFA` implementation as the epsilon transition.
- `delta` (`dict[str, dict[str, set[str]]]`): Dictionary that represents the
    transition function of the automata. The key of the dictionary is a state of
    the automata and the value is another dictionary that represents the
    transition function of the automata. The key of the inner dictionary is a
    symbol of the alphabet and the value is a set of states that the automata
    will go if it consumes the symbol.
    - Example:
    ```python
    delta = {
        'q0' : {
                '0' : {'q0', 'q2'},
                '1' : {'q1', 'q2', 'q3'}
                },
        'q1' : {
                '0' : {'q2'},
                '1' : {'q0', 'q1'}
                },
        'q2' : {
                '0' : {'q1', 'q2'},
                '' : {'q2'}
                },
    }
    ```
- `initial_state` (`str`): String that represents the initial state of the
    automata. initial_state must be in q.
- `f` (`set[str]`): Set of strings where each string is a final state of the
    automata. f must be a subset of q.

### Example

Here is an example of how to create a `NFA`:

```python
from automathon import NFA

## Epsilon Transition is denoted by '' -> Empty string
q = {'q1', 'q2', 'q3', 'q4'}
sigma = {'0', '1'}
delta = {
    'q1' : {
            '0' : {'q1'},
            '1' : {'q1', 'q2'}
            },
    'q2' : {
            '0' : {'q3'},
            '' : {'q3'}
            },
    'q3' : {
            '1' : {'q4'},
            },
    'q4' : {
            '0' : {'q4'},
            '1' : {'q4'},
            },
}
initial_state = 'q1'
f = {'q4'}

automata = NFA(q, sigma, delta, initial_state, f)
```

## Functions and Methods

The `NFA` class has multiple functions and methods that you can use to interact
with the automata. Here are the methods:

### is_valid

This function checks if the automata is valid. The automata is valid if the
initial state and the final states are in q, if the transitions are in q and
sigma. If the automata is not valid, the function will raise an exception with
the error message.

Example:

```python
automata.is_valid()    # True
```

### accept

This function receives a string and returns `True` if the automata accepts the
string, otherwise it returns `False`.

Example:

```python
automata.accept("0000011")   # True
automata.accept("000001")    # False
```

### view

This method receives a string as the file name for the png and svg files. It
enables to visualize the automaton. You can also add custom styling to the
automata.

```python
automata.view("NFA Visualization")

# Add custom styling

automata.view(
    file_name="NFA Custom Styling",
    node_attr={'fontsize': '20'},
    edge_attr={'fontsize': '20pt'}
)
```

Here is the result of the visualization:

![NFA Visualization](https://github.com/rohaquinlop/automathon/assets/50106623/966f4389-7862-4e5f-a5f4-c007c3a836b4)

### contains_epsilon_transitions

This function returns `True` if the automata contains epsilon transitions,
otherwise it returns `False`.

Example:

```python
automata.contains_epsilon_transitions()    # True
```

### remove_epsilon_transitions

This function returns a new `NFA` that represents the same language as the
original `NFA` but without epsilon transitions.

Example:

```python
automata_1 = automata.remove_epsilon_transitions()

automata_1.accept("0000011")   # True
automata_1.accept("000001")    # False
```

### minimize

This function returns a new `NFA` that represents the same language as the
original `NFA` but minimized.

Example:

```python
automata_2 = automata.minimize()

automata_2.accept("0000011")   # True
automata_2.accept("000001")    # False
```

### renumber

This method modifies the automata by renumbering the states. The new states will
be named as `q0`, `q1`, `q2`, and so on.

Example:

```python
automata.renumber()

automata.accept("0000011")   # True
automata.accept("000001")    # False
```

### get_dfa

This function returns a new DFA that represents the same language as the
original NFA.

Example:

```python
automata_3 = automata.get_dfa()

automata_3.accept("0000011")   # True
automata_3.accept("000001")    # False
```

### complement

This function returns the complement of the automata. The complement of the
automata is another automata that accepts the strings that the original automata
doesn't accept and vice versa. This function returns a new automata, it doesn't
modify the original one.

Example:

```python
not_automata = automata.complement()

not_automata.accept("000001")    # True
not_automata.accept("0000011")   # False
```

### union

This function receives another automata and returns a new automata that
represents the union of the languages of the original automata and the automata
received as a parameter.

Example:

```python
from automathon import NFA

nfa = NFA(
    q={"A"},
    sigma={"a"},
    delta={"A": {"a": {"A"}}},
    initial_state="A",
    f={"A"}
)

nfa_1 = NFA(
    q={"C", "D", "E"},
    sigma={"a", "b"},
    delta={
        "C": {
            "b": {"D"},
        },
        "D": {"a": {"E"}, "b": {"D"}},
    },
    initial_state="C",
    f={"E"},
)

union_result = nfa.union(nfa_1)

union_result.is_valid()             # True
union_result.accept("aaaaaa")       # True
union_result.accept("aaaabbbbaaa")  # False
```

### intersection

This function receives another automata and returns a new automata that
represents the intersection of the languages of the original automata and the
automata received as a parameter.

Example:

```python
nfa = NFA(
    q={"q1", "q2", "q3", "q4", "q5"},
    sigma={"a", "b"},
    delta={
        "q1": {
            "a": {"q2", "q1"},
            "b": {"q1"},
        },
        "q2": {"a": {"q3"}},
        "q3": {
            "a": {"q3", "q4"},
            "b": {"q3"},
        },
        "q4": {"a": {"q5"}},
        "q5": {
            "a": {"q5"},
            "b": {"q5"},
        },
    },
    initial_state="q1",
    f={"q5"},
)

nfa_1 = NFA(
    q={"q1", "q2", "q3"},
    sigma={"a", "b"},
    delta={
        "q1": {
            "a": {"q2", "q1"},
            "b": {"q1"},
        },
        "q2": {"a": {"q3"}},
        "q3": {
            "a": {"q3"},
            "b": {"q3"},
        },
    },
    initial_state="q1",
    f={"q3"},
)

intersection_result = nfa.intersection(nfa_1)

intersection_result.is_valid()                  # True
intersection_result.accept("aaaaaaaa")          # True
intersection_result.accept("aaaaaaaabbbbb")     # True
intersection_result.accept("a")                 # False
intersection_result.accept("bbbbbbbb")          # False
```

### product

This function receives another automata and returns a new automata that
represents the product of the languages of the original automata and the automata
received as a parameter.

Example:

```python
from automathon import NFA

nfa = NFA(
    q={"A", "B"},
    sigma={"a", "b"},
    delta={"A": {"a": {"B"}, "b": {"A"}}, "B": {"a": {"A"}, "b": {"B"}}},
    initial_state="A",
    f={"A"},
)

nfa_1 = NFA(
    q={"C", "D"},
    sigma={"a", "b"},
    delta={"C": {"a": {"C"}, "b": {"D"}}, "D": {"a": {"D"}, "b": {"C"}}},
    initial_state="C",
    f={"C"},
)

product_result = nfa.product(nfa_1)

product_result.is_valid()           # True
product_result.accept("")           # True
product_result.accept("bb")         # True
product_result.accept("bbaaa")      # False
```
