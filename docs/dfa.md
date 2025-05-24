# Deterministic Finite Automata - DFA

`DFA` is the class used in automathon to represent a Deterministic Finite Automata.

## Attributes

Here are the attributes of the `DFA` class:

- `q` (`Set[str]`): Set of strings where each string is a state of the automata.
- `sigma` (`Set[str]`): Set of strings where each string is a symbol of the
    alphabet, the length of each string must be 1. The empty string is not
    allowed in the `DFA` implementation if you need to use them then checkout
    [Non-Deterministic Finite Automata](nfa.md).
- `delta` (`Dict[str, Dict[str, str]]`): Dictionary that represents the transition
    function of the automata. The key of the dictionary is a state of the
    automata and the value is another dictionary that represents the transition
    function of the automata. The key of the inner dictionary is a symbol of the
    alphabet and the value is the state that the automata will go if it consumes
    the symbol.
    - Example:
    ```python
    delta = {
        'q0' : {'0' : 'q0', '1' : 'q1'},
        'q1' : {'0' : 'q2', '1' : 'q0'},
        'q2' : {'0' : 'q1', '1' : 'q2'},
    }
    ```
- `initial_state` (`str`): String that represents the initial state of the automata. initial_state must be in q.
- `f` (`Set[str]`): Set of strings where each string is a final state of the automata. f must be a subset of q.

### Example

Here is an example of how to create a `DFA`:

```python
from automathon import DFA

q = {'q0', 'q1', 'q2'}
sigma = {'0', '1'}
delta = {
    'q0' : {'0' : 'q0', '1' : 'q1'},
    'q1' : {'0' : 'q2', '1' : 'q0'},
    'q2' : {'0' : 'q1', '1' : 'q2'},
}
initial_state = 'q0'
f = {'q0'}

automata = DFA(q, sigma, delta, initial_state, f)
```

## Functions and Methods

The `DFA` class has multiple functions and methods that you can use to interact
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
automata.accept("001001")  # True
automata.accept("00100")   # False
```

### view

This method receives a string as the file name for the png and svg files. It
enables to visualize the automaton. You can also add custom styling to the
automata.

Example:

```python
automata.view("DFA Visualization")

# Add custom styling or change the file format

automata.view(file_name="DFA Custom Styling",
              file_format="png" or "svg",
              node_attr={'fontsize': '20'},
              edge_attr={'fontsize': '20pt'})
```

### get_nfa

This function returns a new NFA that represents the same language as the
original DFA.

Example:

```python
automata_nfa = automata.get_nfa()
automata_nfa.accept("001001")  # True
```

### complement

This function returns the complement of the automata. The complement of the
automata is another automata that accepts the strings that the original
automata doesn't accept and vice versa. This function returns a new automata,
it doesn't modify the original one.

Example:

```python
not_automata = automata.complement()
not_automata.accept("00100")    # True
not_automata.accept("001001")   # False
```

### union

This function receives another automata and returns a new automata that
represents the union of the languages of the original automata and the
automata received as a parameter.

Example:

```python
dfa = DFA(
    q={"A", "B"},
    sigma={"0", "1"},
    delta={"A": {"0": "A", "1": "B"}, "B": {"0": "B", "1": "A"}},
    initial_state="A",
    f={"B"},
)

dfa_1 = DFA(
    q={"R", "S", "T", "U"},
    sigma={"0", "1"},
    delta={
        "R": {"0": "S", "1": "R"},
        "S": {"0": "T", "1": "R"},
        "T": {"0": "U", "1": "R"},
        "U": {"0": "U", "1": "U"},
    },
    initial_state="R",
    f={"U"},
)

union_result = dfa.union(dfa_1)

union_result.is_valid()             # True
union_result.accept("00010010")     # True
union_result.accept("0011000")      # True
```

### intersection

This function receives another automata and returns a new automata that
represents the intersection of the languages of the original automata and the
automata received as a parameter.

Example:

```python
dfa = DFA(
    q={"A", "B"},
    sigma={"0", "1"},
    delta={"A": {"0": "A", "1": "B"}, "B": {"0": "B", "1": "A"}},
    initial_state="A",
    f={"B"},
)

dfa_1 = DFA(
    q={"R", "S", "T", "U"},
    sigma={"0", "1"},
    delta={
        "R": {"0": "S", "1": "R"},
        "S": {"0": "T", "1": "R"},
        "T": {"0": "U", "1": "R"},
        "U": {"0": "U", "1": "U"},
    },
    initial_state="R",
    f={"U"},
)

intersection_result = dfa.intersection(dfa_1)

intersection_result.is_valid()          # True
intersection_result.accept("0001")      # True
intersection_result.accept("00010010")  # False
```

### difference

This function receives another automata and returns a new automata that
represents the difference of the languages of the original automata and the
automata received as a parameter.

Example:

```python
dfa = DFA(
    q={"1", "2"},
    sigma={"a", "b"},
    delta={"1": {"a": "2", "b": "1"}, "2": {"a": "1", "b": "2"}},
    initial_state="1",
    f={"1"},
)

dfa_1 = DFA(
    q={"3", "4"},
    sigma={"a", "b"},
    delta={"3": {"a": "3", "b": "4"}, "4": {"a": "4", "b": "3"}},
    initial_state="3",
    f={"3"},
)

difference_result = dfa.difference(dfa_1)

difference_result.is_valid()        # True
difference_result.accept("b")       # True
difference_result.accept("aba")     # True
difference_result.accept("aa")      # True
```

### symmetric_difference

This function receives another automata and returns a new automata that
represents the symmetric difference of the languages of the original automata
and the automata received as a parameter.

Example:

```python
dfa = DFA(
    q={"1", "2"},
    sigma={"a", "b"},
    delta={"1": {"a": "2", "b": "1"}, "2": {"a": "1", "b": "2"}},
    initial_state="1",
    f={"1"},
)

dfa_1 = DFA(
    q={"3", "4"},
    sigma={"a", "b"},
    delta={"3": {"a": "3", "b": "4"}, "4": {"a": "4", "b": "3"}},
    initial_state="3",
    f={"3"},
)

symmetric_difference_result = dfa.symmetric_difference(dfa_1)

symmetric_difference_result.is_valid()      # True
difference_result.accept("b")               # True
difference_result.accept("a")               # True
difference_result.accept("abbabb")          # False
```

### product

This function receives another automata and returns a new automata that
represents the product of the languages of the original automata and the
automata received as a parameter.

Example:

```python
dfa = DFA(
    q={"A", "B"},
    sigma={"a", "b"},
    delta={"A": {"a": "B", "b": "A"}, "B": {"a": "A", "b": "B"}},
    initial_state="A",
    f={"A"},
)

dfa_1 = DFA(
    q={"C", "D"},
    sigma={"a", "b"},
    delta={"C": {"a": "C", "b": "D"}, "D": {"a": "D", "b": "C"}},
    initial_state="C",
    f={"C"},
)

product_result = dfa.product(dfa_1)

product_result.is_valid()       # True
product_result.accept("bb")     # True
product_result.accept("b")      # False
```
