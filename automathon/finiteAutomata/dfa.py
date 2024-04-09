# Exceptions module
from __future__ import (
    annotations,
)
from automathon.errors.errors import (
    SigmaError,
)
from collections import (
    deque,
)
from dataclasses import (
    dataclass,
)
from graphviz import (
    Digraph,
)
from typing import (
    Callable,
)


@dataclass
class DFA:
    """A class used to represent a Deterministic Finite Automaton (DFA).

    Attributes
    ----------
    q : set[str]
        Set of strings where each string represents a state.
        Example: q = {'q0', 'q1', 'q2'}

    sigma : set[str]
        Set of strings that represents the alphabet.
        Example: sigma = {'0', '1'}

    delta : dict[str, dict[str, str]]
        Dictionary that represents the transition function.
        Example: delta = {
                      'q0' : {'0' : 'q0', '1' : 'q1'},
                      'q1' : {'0' : 'q2', '1' : 'q0'},
                      'q2' : {'0' : 'q1', '1' : 'q2'},
                    }

    initial_state : str
        String that represents the initial state from where any input is
        processed (initial_state ∈ q / initial_state in q).
        Example: initial_state = 'q0'

    f : set[str]
        Set of strings that represent the final state/states of Q (f ⊆ Q).
        Example: f = {'q0'}

    Methods
    -------
    is_valid() -> bool
        Returns True if the DFA is a valid automata.

    accept(S : str) -> bool
        Returns True if the given string S is accepted by the DFA.

    complement() -> DFA
        Returns the complement of the DFA.

    get_nfa() -> NFA
        Converts the actual DFA to NFA and returns its conversion.

    product(m: DFA) -> DFA
        Given a DFA m, returns the product automaton.

    union(m: DFA) -> DFA
        Given a DFA m, returns the union automaton.

    intersection(m: DFA) -> DFA
        Given a DFA m, returns the intersection automaton.

    difference(m: DFA) -> DFA
        Given a DFA m, returns the difference automaton.

    symmetric_difference(m: DFA) -> DFA
        Given a DFA m, returns the symmetric difference automaton.

    view(
        file_name : str, node_attr : dict[str, str] | None, edge_attr : dict[str, str] | None
    ) -> None
        Using the graphviz library, it creates a visual representation of the DFA
        and saves it as a .png file with the name file_name"""

    q: set[str]
    sigma: set[str]
    delta: dict[str, dict[str, str]]
    initial_state: str
    f: set[str]

    def accept(self, string: str) -> bool:
        """Returns True if the given string is accepted by the DFA

        The string will be accepted if ∀a · a ∈ string ⇒ a ∈ sigma, which means
        that all the characters in string must be in sigma
        (must be in the alphabet).

        Parameters
        - - - - - - - - - - - - - - - - - -
        S : str
          A string that the DFA will try to process.
        """

        # Basic Idea: Search through states (delta) in the DFA, since the initial state to the final states

        if string == "":
            return True

        q = (
            deque()
        )  # queue -> states from i to last character in S | (index, state)
        q.append([0, self.initial_state])  # Starts from 0

        while q:
            idx, state = q.popleft()

            if idx == len(string) and state in self.f:
                return True
            if idx < len(string) and state in self.delta:
                # Search through states
                for transition in self.delta[state].items():
                    # transition: ('1', 'q0')
                    if string[idx] == transition[0]:
                        q.append([idx + 1, transition[1]])

        return False

    def is_valid(self) -> bool:
        """Returns True if the DFA is a valid automata"""
        sigma_error_msg_not_q = "Is not declared in Q"
        sigma_error_msg_not_sigma = "Is not declared in sigma"

        # Validate if the initial state is in the set Q
        if self.initial_state not in self.q:
            raise SigmaError(self.initial_state, sigma_error_msg_not_q)

        # Validate if the delta transitions are in the set Q
        for d in self.delta:
            if d not in self.q:
                raise SigmaError(d, sigma_error_msg_not_q)

            # Validate if the d transitions are valid
            for s in self.delta[d]:
                if s not in self.sigma:
                    raise SigmaError(s, sigma_error_msg_not_sigma)
                elif self.delta[d][s] not in self.q:
                    raise SigmaError(self.delta[d][s], sigma_error_msg_not_q)

        # Validate if the final state are in Q
        for f in self.f:
            if f not in self.q:
                raise SigmaError(f, sigma_error_msg_not_q)

        # None of the above cases failed then this DFA is valid
        return True

    def complement(self) -> "DFA":
        """Returns the complement of the DFA."""
        q = self.q
        sigma = self.sigma
        delta = self.delta
        initial_state = self.initial_state
        f = {state for state in self.q if state not in self.f}

        return DFA(q, sigma, delta, initial_state, f)

    def get_nfa(self):
        from automathon.finiteAutomata.nfa import NFA

        """Convert the actual DFA to NFA class and return it's conversion"""
        q = self.q.copy()
        delta = dict()
        initial_state = self.initial_state
        f = self.f.copy()
        sigma = self.sigma

        for state, transition in self.delta.items():
            # state : str, transition : dict(sigma, Q)
            tmp = dict()
            for s, _q in transition.items():
                # s : sigma
                tmp[s] = ["".join(_q)]

            delta[state] = tmp

        return NFA(q, sigma, delta, initial_state, f)

    def product(self, m: "DFA") -> "DFA":
        """Given a DFA m returns the product automaton"""
        delta = dict()
        q = set()
        f = set()
        sigma = self.sigma.intersection(m.sigma)

        for state, transition in self.delta.items():
            # i : str, j : dict(sigma, Q)
            for state_m, transition_m in m.delta.items():
                # stateM : str, transitionM : dict(sigma, Q)
                sigma, q, f, delta = self._process_states(
                    state,
                    state_m,
                    transition,
                    transition_m,
                    sigma,
                    q,
                    f,
                    m.f,
                    delta,
                )

        return DFA(
            q, sigma, delta, str([self.initial_state, m.initial_state]), f
        )

    def _process_states(
        self,
        state: str,
        state_m: str,
        transition: dict[str, str],
        transition_m: dict[str, str],
        sigma: set[str],
        q: set[str],
        f: set[str],
        f_m: set[str],
        delta: dict[str, dict[str, str]],
    ) -> tuple[set[str], set[str], set[str], dict[str, dict[str, str]]]:
        for s in transition:
            if s in transition_m:
                sigma, q, f, delta = self._process_transitions(
                    state,
                    state_m,
                    s,
                    transition,
                    transition_m,
                    sigma,
                    q,
                    f,
                    f_m,
                    delta,
                )
        return sigma, q, f, delta

    def _process_transitions(
        self,
        state: str,
        state_m: str,
        s: str,
        transition: dict[str, str],
        transition_m: dict[str, str],
        sigma: set[str],
        q: set[str],
        f: set[str],
        f_m: set[str],
        delta: dict[str, dict[str, str]],
    ) -> tuple[set[str], set[str], set[str], dict[str, dict[str, str]]]:
        # sigma value in common
        sigma.add(s)

        tmp = str([state, state_m])
        tmp1 = str([transition[s], transition_m[s]])
        aux = dict()
        aux[s] = tmp1

        q.add(tmp)
        q.add(tmp1)

        if state in self.f and state_m in f_m:
            f.add(tmp)

        if transition[s] in self.f and transition_m[s] in f_m:
            f.add(tmp1)

        if tmp in delta:
            delta[tmp].update(aux)
        else:
            delta[tmp] = aux

        return sigma, q, f, delta

    def _binary_operation(
        self, m: "DFA", operation: Callable[..., bool]
    ) -> "DFA":
        new_q_list: list[tuple[str, str]] = []

        initial_state = str((self.initial_state, m.initial_state))
        delta: dict[str, dict[str, str]] = dict()
        sigma: set[str] = self.sigma.copy()
        f: set[str] = set()

        # Check if both sigmas are the same
        if self.sigma != m.sigma:
            raise SigmaError(
                self.sigma, "Sigma from both DFAs must be the same"
            )

        queue = deque()
        queue.append((self.initial_state, m.initial_state))

        while queue:
            a, b = queue.popleft()

            new_q_list.append((a, b))

            if operation(a, self.f, b, m.f):
                f.add(str((a, b)))

            common_transitions = self.delta[a].keys() & m.delta[b].keys()

            for s in common_transitions:
                new_q = (self.delta[a][s], m.delta[b][s])

                if new_q not in new_q_list:
                    queue.append(new_q)
                    new_q_list.append(new_q)

                if str((a, b)) in delta:
                    delta[str((a, b))][s] = str(new_q)
                else:
                    delta[str((a, b))] = {s: str(new_q)}

        return DFA(set(map(str, new_q_list)), sigma, delta, initial_state, f)

    def union(self, m: "DFA") -> "DFA":
        """Given a DFA  returns the union automaton"""
        return self._binary_operation(
            m, lambda a, f, b, f_m: a in f or b in f_m
        )

    def intersection(self, m: "DFA") -> "DFA":
        """Given a DFA  returns the intersection automaton"""
        return self._binary_operation(
            m, lambda a, f, b, f_m: a in f and b in f_m
        )

    def difference(self, m: "DFA") -> "DFA":
        """Given a DFA  returns the difference automaton"""
        return self._binary_operation(
            m, lambda a, f, b, f_m: a in f and b not in f_m
        )

    def symmetric_difference(self, m: "DFA") -> "DFA":
        """Given a DFA  returns the symmetric difference automaton"""
        return self._binary_operation(
            m,
            lambda a, f, b, f_m: (a in f and b not in f_m)
            or (a not in f and b in f_m),
        )

    def view(
        self,
        file_name: str,
        node_attr: dict[str, str] | None = None,
        edge_attr: dict[str, str] | None = None,
    ) -> None:
        dot = Digraph(
            name=file_name,
            format="png",
            node_attr=node_attr,
            edge_attr=edge_attr,
        )

        dot.graph_attr["rankdir"] = "LR"

        dot.node("", "", shape="plaintext")

        for f in self.f:
            dot.node(f, f, shape="doublecircle")

        for q in self.q:
            if q not in self.f:
                dot.node(q, q, shape="circle")

        dot.edge("", self.initial_state, label="")

        for q in self.delta:
            for s in self.delta[q]:
                dot.edge(q, self.delta[q][s], label=s)

        dot.render()
