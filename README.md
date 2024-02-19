# automathon

<p align="center">
    <a href="https://rohaquinlop.github.io/automathon/"><img src="docs/img/logo-vector.svg" alt="automathon"></a>
</p>

<p align="center">
    <em>A Python library for simulating and visualizing finite automata.</em>
</p>

<p align="center">
    <a href="https://github.com/rohaquinlop/automathon" target="_blank">
        <img src="https://github.com/rohaquinlop/automathon/actions/workflows/main.yml/badge.svg?branch=main" alt="Test">
    </a>
    <a href="https://sonarcloud.io/summary/new_code?id=rohaquinlop_automathon" target="_blank">
        <img src="https://sonarcloud.io/api/project_badges/measure?project=rohaquinlop_automathon&metric=alert_status" alt="Quality Gate">
    </a>
    <a href="https://pypi.org/project/automathon" target="_blank">
    <img src="https://img.shields.io/pypi/v/automathon?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
</p>

---

**Documentation**: <a href="https://rohaquinlop.github.io/automathon/" target="_blank">https://rohaquinlop.github.io/automathon/</a>

**Source Code**: <a href="https://github.com/rohaquinlop/automathon" target="_blank">https://github.com/rohaquinlop/automathon</a>

**PyPI**: <a href="https://pypi.org/project/automathon/" target="_blank">https://pypi.org/project/automathon/</a>

---

## Requirements

- Python >= 3.10
- You also need to install Graphviz on your computer ([download page](https://www.graphviz.org/download/), [installation procedure for Windows](https://forum.graphviz.org/t/new-simplified-installation-procedure-on-windows/224), [archived versions](https://www2.graphviz.org/Archive/stable/)).Make sure that the directory containing the **dot** executable is on your systems’ path.

## Installation

```bash
pip install automathon
```

### Upgrade

```bash
pip install automathon --upgrade
```

## Example

Here is are some examples about what you can do with **automathon**, you can
check the documentation about [Deterministic Finite Automata](dfa.md) and
[Non-Deterministic Finite Automata](nfa.md) to know more about the functions and
methods that are available.

### DFA - Deterministic Finite Automata

![DFA Visualization](https://github.com/rohaquinlop/automathon/assets/50106623/81efada9-3c68-4611-bb5c-53dcaf7987f1)

This image was created using **automathon**.

Let's create the previous automata using the library:

```python
from automathon import DFA
q = {'q0', 'q1', 'q2'}
sigma = {'0', '1'}
delta = { 'q0' : {'0' : 'q0', '1' : 'q1'},
          'q1' : {'0' : 'q2', '1' : 'q0'},
          'q2' : {'0' : 'q1', '1' : 'q2'}
        }
initial_state = 'q0'
f = {'q0'}

automata = DFA(q, sigma, delta, initial_state, f)
```

#### Verify if the automata is valid

```python
automata.is_valid()    # True
```

In this case, the automata is valid but if it wasn't, the library would raise an
exception with the error message.

#### Errors

Errors that the library can raise are:

- **SigmaError**:
  - The automata contain an initial state, or a final state that's not defined on Q.
  - The automata contain a delta transition that's not defined on Q or in Sigma.

- **InputError**:
  - The automata is trying to consume a letter that's not defined in sigma.

#### Verify if the automata accept a given string

```python
automata.accept("001001")  # True
automata.accept("00100")   # False
```

#### Get the automata's complement

```python
not_automata = automata.complement()
not_automata.accept("00100")    #True
```

Note that this function returns a new automata, it doesn't modify the original
one.

#### Visualize the automata

For both, [DFA](dfa.md) and [NFA](nfa.md), the view method enables to visualize the automaton, receives as parameter a String as the file name for the png and svg files.

More information about the graphviz attributes [here](https://www.graphviz.org/doc/info/attrs.html).

![DFA Visualization](https://github.com/rohaquinlop/automathon/assets/50106623/81efada9-3c68-4611-bb5c-53dcaf7987f1)
```python
# Default styling
automata.view("DFA Visualization")

# If you want to add custom styling, you can use the following

automata.view(
    file_name="DFA Custom Styling",
    node_attr={'fontsize': '20'},
    edge_attr={'fontsize': '20pt'}
)
```

If you want to explore more about the functions and methods of the DFA class,
you can check the [DFA documentation](dfa.md). And if you want to know more about
the NFA class, you can check the [NFA documentation](nfa.md).

### NFA - Non-Deterministic Finite Automata

![](http://www.r9paul.org/wp-content/uploads/2008/12/nfa_example.jpg)

Image taken from: [r9paul.org](http://www.r9paul.org/blog/2008/nondeterministic-finite-state-machine/)

#### Representing the previous automata

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

#### Verify if the automata is valid

```python
automata.is_valid()  # True
```

#### Verify if the automata accept a string

```python
automata.accept("0000011")   #True
automata.accept("000001")    #False
```

#### Get the automata's complement

```python
not_automata = automata.complement()
not_automata.accept("000001")    #True
```

#### Visualize the automata

![NFA Visualization](https://github.com/rohaquinlop/automathon/assets/50106623/966f4389-7862-4e5f-a5f4-c007c3a836b4)
```python
# Default styling
automata.view("NFA Visualization")

# If you want to add custom styling, you can use the following

automata.view(
    file_name="NFA Custom Styling",
    node_attr={'fontsize': '20'},
    edge_attr={'fontsize': '20pt'}
)
```

## License

This project is licensed under the terms of the MIT license.
