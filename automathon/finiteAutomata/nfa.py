# Exceptions module
from __future__ import annotations

from automathon.errors.errors import *
from collections import deque
from graphviz import Digraph
from automathon.finiteAutomata.dfa import DFA


def _get_new_delta_real_value(
        delta: dict[str, dict[str, list[str]]],
        real_value: dict[str, str]
) -> dict[str, dict[str, set[str]]]:
    new_delta = dict()
    for q, transition in delta.items():
        tmp_dict = dict()
        for s, states in transition.items():
            tmp_states = []
            for state in states:
                tmp_states.append(real_value[state])

            tmp_dict[s] = set(tmp_states.copy())
        new_delta[real_value[q]] = tmp_dict.copy()
    return new_delta


class NFA:
    """A Class used to represent a Non-Deterministic Finite Automaton

  ...

  Attributes
  - - - - - - - - - - - - - - - - - -
  q : set
    Set of strings where each string represent the states.
    Ex:
      q = {'q0', 'q1', 'q2'}

  sigma : set
    Set of strings that represents the alphabet.
    Ex:
      sigma = {'0', '1'}
  
  delta : dict
    Dictionary that represents the transition function.
    Ex:
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
  
  initial_state : str
    String that represents the initial state from where any input is processed (initial_state ∈ Q / initial_state in q).
    Ex:
      initial_state = 'q0'
  
  f : set
    Set of strings that represent the final state/states of Q (f ⊆ Q).
    Ex:
      f = {'q0', 'q1'}
  

  Methods
  - - - - - - - - - - - - - - - - - -

  is_valid() -> bool : Returns True if the NFA is a valid automata
  accept(string : str) -> bool : Returns True if the given string is accepted by the NFA
  complement() -> NFA : Returns the complement of the NFA
  """

    def __init__(self, q: set, sigma: set, delta: dict, initial_state: str, f: set):
        """
    Parameters
    - - - - - - - - - - - - - - - - - -
    
    q : set
      Set of strings where each string represent the states.
    
    sigma : set
      Set of strings that represents the alphabet.
    
    delta : dict
      Dictionary that represents the transition function.
    
    initial_state : str
      String that represents the initial state from where any input is processed
      (initial_state ∈ Q / initial_state in q).
    
    f : set
      Set of strings that represent the final state/states of Q (f ⊆ Q).
    """
        self.q = q
        self.sigma = sigma
        self.delta = delta
        self.initial_state = initial_state
        self.f = f

    def accept(self, string: str) -> bool:
        """ Returns True if the given string is accepted by the NFA

    The string will be accepted if ∀a · a ∈ string ⇒ a ∈ sigma, which means that all the characters in string must be
    in sigma (must be in the alphabet).

    Parameters
    - - - - - - - - - - - - - - - - - -
    string : str
      A string that the NFA will try to process.
    """

        # Basic Idea: Search through states (delta) in the NFA, since the initial state to the final states

        # BFS states

        q = deque()  # queue -> states from i to last character in S | (index, state)
        q.append([0, self.initial_state])  # Starts from 0
        ans = False  # Flag

        while q and not ans:
            front_q = q.popleft()
            idx = front_q[0]
            state = front_q[1]

            if idx == len(string):
                if state in self.f:
                    ans = True
            elif string[idx] not in self.sigma:
                raise InputError(string[idx], 'Is not declared in sigma')
            elif state in self.delta:
                # Search through states
                for transition in self.delta[state].items():
                    d = transition[0]
                    states = transition[1]

                    if d == "":
                        # Is epsilon
                        for state in states:
                            # Do not consume character
                            q.append([idx, state])
                    elif string[idx] == d:
                        for state in states:
                            # Consume character
                            q.append([idx + 1, state])

        if string == "":
            ans = True

        return ans

    def is_valid(self) -> bool:
        """ Returns True if the NFA is a valid automata """
        ans = True
        not_declared_state = None

        # Validate if the initial state is in the set Q
        if self.initial_state not in self.q:
            not_declared_state = self.initial_state

        # Validate if the delta transitions are in the set Q
        for d in self.delta:
            if not_declared_state is not None:
                break

            if d != "" and d not in self.q:
                not_declared_state = d

            # Validate if the d transitions are valid
            for s in self.delta[d]:
                if s != "" and s not in self.sigma:
                    not_declared_state = s
                for q in self.delta[d][s]:
                    if q not in self.q:
                        not_declared_state = self.delta[d][s]

        # Validate if the final state are in Q
        for f in self.f:
            if f not in self.q:
                not_declared_state = f

        if not_declared_state is not None:
            raise SigmaError(not_declared_state, 'Is not declared in Q')
        return ans

    def complement(self) -> 'NFA':
        """Returns the complement of the NFA."""
        q = self.q
        sigma = self.sigma
        delta = self.delta
        initial_state = self.initial_state
        f = {state for state in self.q if state not in self.f}

        return NFA(q, sigma, delta, initial_state, f)

    def get_e_closure(self, q, visited=None):
        """Returns a list of the epsilon closures from estate q"""
        ans = [q]
        if visited is None:
            visited = list(q)

        if q in self.delta:
            if '' in self.delta[q]:
                for st in self.delta[q]['']:
                    if st not in visited:
                        visited.append(st)
                        ans.extend([k for k in self.get_e_closure(st, visited) if k not in ans])
        return ans

    def contains_epsilon_transitions(self) -> bool:
        """Returns True if the NFA contains Epsilon transitions else returns False"""
        for q in self.delta:
            if '' in self.delta[q]:
                return True
        return False

    def remove_epsilon_transitions(self) -> 'NFA':
        """Returns a copy of the actual NFA that doesn't contain epsilon transitions"""
        q_prime = self.q.copy()
        delta_prime = self.delta.copy()
        delta_init_state = self.initial_state
        delta_f = self.f.copy()

        if self.contains_epsilon_transitions():
            delta_prime = dict()
            for q in q_prime:
                closure_states = self.get_e_closure(q)

                for sigma in self.sigma:
                    to_epsilon_closure = list()
                    new_transitions = list()

                    # Get the transitions from sigma in each epsilon closure
                    for closure_state in closure_states:
                        if closure_state in self.f:
                            delta_f.add(q)
                        if closure_state in self.delta and sigma in self.delta[closure_state]:
                            to_epsilon_closure.extend(self.delta[closure_state][sigma])

                    # Get the new transitions from the epsilon closure
                    for epsilon_closure in to_epsilon_closure:
                        new_transitions.extend(self.get_e_closure(epsilon_closure))

                    if q not in delta_prime:
                        delta_prime[q] = dict()

                    if sigma != '':
                        delta_prime[q][sigma] = set(new_transitions)

        return NFA(q_prime, self.sigma, delta_prime, delta_init_state, delta_f)

    def get_dfa(self) -> DFA:
        """Convert the actual NFA to DFA and return its conversion"""

        local_nfa = NFA(self.q, self.sigma, self.delta, self.initial_state, self.f)
        local_nfa = local_nfa.remove_epsilon_transitions()

        q_prime = []
        delta_prime = dict()

        queue = deque()
        visited = [[local_nfa.initial_state]]
        queue.append([local_nfa.initial_state])

        while queue:
            qs = queue.pop()  # state Q

            local_transitions = dict()  # {str : list}

            for q in qs:
                if q in local_nfa.delta:
                    for s in local_nfa.delta[q]:
                        tmp = local_nfa.delta[q][s].copy()
                        if tmp:
                            if s in local_transitions:
                                # avoid add repeated values
                                local_transitions[s].extend([k for k in tmp if k not in local_transitions[s]])
                            else:
                                local_transitions[s] = list(tmp)

            for transition in local_transitions:
                local_transitions[transition].sort()
                tmp = local_transitions[transition].copy()
                if tmp not in visited:
                    queue.append(tmp)
                    visited.append(tmp)
                local_transitions[transition] = str(local_transitions[transition])

            delta_prime[str(qs)] = local_transitions
            q_prime.append(qs)

        f_prime = set()

        for qs in q_prime:
            for q in qs:
                if q in local_nfa.f:
                    f_prime.add(str(qs))
                    break

        aux = set()

        for qs in q_prime:
            aux.add(str(qs))

        q_prime = aux

        return DFA(q_prime, local_nfa.sigma, delta_prime, str([local_nfa.initial_state]), f_prime)

    def minimize(self):
        """Minimize the automata and return the NFA result of the minimization"""
        local_dfa = self.get_dfa()
        local_nfa = local_dfa.get_nfa()
        local_nfa.renumber()
        return local_nfa

    def renumber(self):
        """Change the name of the states, renumbering each of the labels"""
        idx = 0
        new_tags = dict()

        # New values
        q = set()
        delta = dict()
        f = set()

        # Setting the new label for each state
        tmp_q = list(self.q)
        tmp_q.sort()

        for _q in tmp_q:
            new_tags[_q] = str(idx)
            q.add(str(idx))
            idx += 1

        initial_state = new_tags[self.initial_state]

        # Changing the labels for the final states
        for _f in self.f:
            f.add(new_tags[_f])

        for _q in self.delta:
            delta[new_tags[_q]] = dict()
            for s in self.delta[_q]:
                nxt_states = list()
                for nxtState in self.delta[_q][s]:
                    nxt_states.append(new_tags[nxtState])

                delta[new_tags[_q]][s] = set(nxt_states)

        self.q, self.f, self.delta, self.initial_state = q, f, delta, initial_state

    def union(self, m: 'NFA') -> 'NFA':
        """Given a NFA m returns the union automaton"""
        sigma = self.sigma.union(m.sigma)
        q = set()
        f = set()
        initial_state = "q0"
        q.add(initial_state)
        real_value_self = dict()
        real_value_m = dict()

        # Fix possible errors when using the dictionaries with the name of the states
        for i, _q in enumerate(self.q, 1):
            real_value_self[_q] = "q{}".format(i)
            q.add(real_value_self[_q])

        for i, s in enumerate(m.q):
            real_value_m[s] = "s{}".format(i)
            q.add(real_value_m[s])

        for _q in self.f:
            f.add(real_value_self[_q])

        for _q in m.f:
            f.add(real_value_m[_q])

        # Replace the values
        self_delta = _get_new_delta_real_value(self.delta, real_value_self)
        m_delta = _get_new_delta_real_value(m.delta, real_value_m)

        delta = {
                    **self_delta,
                    **m_delta,
                    initial_state: {
                        '': {
                            real_value_self[self.initial_state],
                            real_value_m[m.initial_state]
                        }
                    }
        }

        return NFA(q, sigma, delta, initial_state, f)

    def product(self, m: 'NFA') -> 'NFA':
        """Given a DFA M returns the product automaton"""
        # Using DFA conversion
        a = self.get_dfa()
        b = m.get_dfa()

        nfa = a.product(b).get_nfa()

        return nfa

    def view(self, file_name: str, node_attr: dict[str, str] | None = None, edge_attr: dict[str, str] | None = None):
        dot = Digraph(name=file_name, format='png', node_attr=node_attr, edge_attr=edge_attr)

        dot.graph_attr['rankdir'] = 'LR'

        dot.node("", "", shape='plaintext')

        for _f in self.f:
            dot.node(_f, _f, shape='doublecircle')

        for _q in self.q:
            if _q not in self.f:
                dot.node(_q, _q, shape='circle')

        dot.edge("", self.initial_state, label="")

        for q in self.delta:
            for s in self.delta[q]:
                for t in self.delta[q][s]:
                    if s == '':
                        dot.edge(q, t, label='ε')
                    else:
                        dot.edge(q, t, label=s)

        dot.render()
