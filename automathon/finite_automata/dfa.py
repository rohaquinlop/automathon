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

        # Basic Idea: Search through states (delta) in the DFA, from the initial state to the final states

        ans = False

        # queue -> states from i to last character in S | (index, state)
        q: deque[tuple[int, str]] = deque()
        q.append([0, self.initial_state])

        while q and not ans:
            idx, state = q.popleft()

            if idx == len(string) and state in self.f:
                ans = True
            elif idx < len(string) and state in self.delta:
                # Search through states
                for transition in self.delta[state].items():
                    # transition: ('1', 'q0')
                    if string[idx] == transition[0]:
                        q.append([idx + 1, transition[1]])

        return ans

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
        from automathon.finite_automata.nfa import NFA

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
        delta: dict[str, dict[str, str]] = dict()
        q: set[str] = set()
        f: set[str] = set()
        sigma: set[str] = self.sigma.intersection(m.sigma)

        for state, transition in self.delta.items():
            # i : str, j : dict(sigma, Q)
            for state_m, transition_m in m.delta.items():
                # stateM : str, transitionM : dict(sigma, Q)
                sigma, q, f, delta = self.__process_states(
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

    def __process_states(
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
                sigma, q, f, delta = self.__process_transitions(
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

    def __process_transitions(
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

    def union(self, m: "DFA") -> "DFA":
        """Given a DFA  returns the union automaton"""
        return self.__binary_operation(
            m, lambda a, f, b, f_m: a in f or b in f_m
        )

    def intersection(self, m: "DFA") -> "DFA":
        """Given a DFA  returns the intersection automaton"""
        return self.__binary_operation(
            m, lambda a, f, b, f_m: a in f and b in f_m
        )

    def difference(self, m: "DFA") -> "DFA":
        """Given a DFA  returns the difference automaton"""
        return self.__binary_operation(
            m, lambda a, f, b, f_m: a in f and b not in f_m
        )

    def symmetric_difference(self, m: "DFA") -> "DFA":
        """Given a DFA  returns the symmetric difference automaton"""
        return self.__binary_operation(
            m,
            lambda a, f, b, f_m: (a in f and b not in f_m)
            or (a not in f and b in f_m),
        )

    def __binary_operation(
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

    def minimize(self) -> "DFA":
        """Minimize the automata and return the minimized version"""
        visited: dict[tuple[str, str], bool] = dict()
        table, q = self.__initialize_table_and_queue()

        while q:
            q_a, q_b = q.popleft()
            if visited.get((q_a, q_b), False):
                break

            visited[(q_a, q_b)] = True

            common_sigma = filter(
                lambda s, q_a=q_a, q_b=q_b: s in self.delta[q_a]
                and s in self.delta[q_b],
                self.sigma,
            )

            reachable_pairs = map(
                lambda s, q_a=q_a, q_b=q_b: (
                    self.delta[q_a][s],
                    self.delta[q_b][s],
                ),
                common_sigma,
            )

            it_is_marked = any(
                map(lambda p: table.get(p, False), reachable_pairs)
            )

            if it_is_marked:
                table[(q_a, q_b)] = True
                visited = dict()
            else:
                q.append((q_a, q_b))

        # combine pending_states
        unmarked_pairs: list[tuple[str, str]] = []
        unmarked_states: set[str] = set()

        while q:
            q_a, q_b = q.popleft()
            unmarked_pairs.append((q_a, q_b))
            unmarked_states.add(q_a)
            unmarked_states.add(q_b)

        remaining_states = self.q.copy() - unmarked_states
        new_final_states: set[str] = set()
        groups: dict[str, list[str]] = dict()

        for pair in unmarked_pairs:
            groups[pair[0]] = groups.get(pair[0], []) + [pair[1]]
            groups[pair[1]] = groups.get(pair[1], []) + [pair[0]]

        # group states from groups (dfs)
        grouped_states: dict[int, list[str]] = dict()
        states_group: dict[str, int] = dict()
        final_groups: list[int] = []

        groups_count = self.__group_unmarked_states(
            unmarked_states,
            groups,
            grouped_states,
            final_groups,
            states_group,
        )

        for state in remaining_states:
            states_group[state] = groups_count
            grouped_states[groups_count] = [state]

            if state in self.f:
                final_groups.append(groups_count)

            groups_count += 1

        new_delta, new_initial_state = self.__build_new_delta(
            groups_count, grouped_states, states_group
        )

        for i in final_groups:
            new_final_states.add(f"q{i}")

        return DFA(
            set(new_delta.keys()),
            self.sigma.copy(),
            new_delta,
            new_initial_state,
            new_final_states,
        )

    def __initialize_table_and_queue(
        self,
    ) -> tuple[dict[tuple[str, str], bool], deque[tuple[str, str]]]:
        table: dict[tuple[str, str], bool] = dict()
        states = list(self.q.copy())
        q: deque[tuple[str, str]] = deque()

        for i in range(1, len(states)):
            for j in range(0, i):
                if states[i] in self.f and states[j] not in self.f:
                    table[(states[i], states[j])] = True
                else:
                    q.append((states[i], states[j]))

        return table, q

    def __group_unmarked_states(
        self,
        unmarked_states: set[str],
        groups: dict[str, list[str]],
        grouped_states: dict[int, list[str]],
        final_groups: list[int],
        states_group: dict[str, int],
    ) -> int:
        visited: dict[str, bool] = dict()
        groups_count = 0

        for state in unmarked_states:
            if visited.get(state, False):
                continue

            final_states, non_final_states = (
                self.__get_final_and_non_final_states(state, visited, groups)
            )

            if final_states:
                grouped_states[groups_count] = final_states
                final_groups.append(groups_count)

                for f_state in final_states:
                    states_group[f_state] = groups_count

                groups_count += 1

            if non_final_states:
                grouped_states[groups_count] = non_final_states

                for nf_state in non_final_states:
                    states_group[nf_state] = groups_count

                groups_count += 1

        return groups_count

    def __get_final_and_non_final_states(
        self, state: str, visited: dict[str, bool], groups: dict[str, list[str]]
    ) -> tuple[list[str], list[str]]:
        stack: deque[str] = deque()
        stack.append(state)
        visited[state] = True
        final_states = []
        non_final_states = []

        while stack:
            current_state = stack.pop()

            if current_state in self.f:
                final_states.append(current_state)
            else:
                non_final_states.append(current_state)

            for next_state in groups[current_state]:
                if not visited.get(next_state, False):
                    stack.append(next_state)
                    visited[next_state] = True

        return final_states, non_final_states

    def __build_new_delta(
        self,
        groups_count: int,
        grouped_states: dict[int, list[str]],
        states_group: dict[str, int],
    ) -> tuple[dict[str, dict[str, str]], str]:
        new_delta: dict[str, dict[str, str]] = dict()
        new_initial_state: str = ""

        for i in range(groups_count):
            new_delta[f"q{i}"] = dict()

            for state in grouped_states[i]:
                if state == self.initial_state:
                    new_initial_state = f"q{i}"

                for s in self.delta[state].keys():
                    new_delta[f"q{i}"][s] = (
                        f"q{states_group[self.delta[state][s]]}"
                    )

        return new_delta, new_initial_state

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