# Exceptions module
from __future__ import (
    annotations,
)
from automathon.errors.errors import (
    InputError,
    SigmaError,
)
from automathon.finiteAutomata.dfa import (
    DFA,
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


@dataclass
class NFA:
    """A Class used to represent a Non-Deterministic Finite Automaton

    Attributes
    - - - - - - - - - - - - - - - - - -
    q : set[str]
      Set of strings where each string represent the states.
      Ex:
        q = {'q0', 'q1', 'q2'}

    sigma : set[str]
      Set of strings that represents the alphabet.
      Ex:
        sigma = {'0', '1'}

    delta : dict[str, dict[str, set[str]]]
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
      String that represents the initial state from where any input is processed
      (initial_state ∈ Q / initial_state in q).
      Ex:
        initial_state = 'q0'

    f : set
      Set of strings that represent the final state/states of Q (f ⊆ Q).
      Ex:
        f = {'q0', 'q1'}


    Methods
    - - - - - - - - - - - - - - - - - -

    is_valid() -> bool
        Returns True if the NFA is a valid automata

    accept(string : str) -> bool
        Returns True if the given string is accepted by the NFA

    complement() -> NFA
        Returns the complement of the NFA

    _get_e_closure(q : str, visited : list[str] | None) -> list[str]
        Returns a list of the epsilon closures from estate q

    _get_new_delta_real_value(
        delta : dict[str, dict[str, set[str]]], real_value : dict[str, str]
    ) -> dict[str, dict[str, set[str]]]
        Returns a new delta dictionary with the real values

    contains_epsilon_transitions() -> bool
        Returns True if the NFA contains Epsilon transitions (ε)

    remove_epsilon_transitions() -> NFA
        Returns a new NFA that is equivalent to the original NFA but without
        epsilon transitions

    get_dfa() -> DFA
        Returns a DFA (Deterministic Finite Automaton) equivalent to the actual NFA

    minimize() -> NFA
        Minimize the automata and return the NFA result of the minimization

    renumber() -> None
        Change the name of the states, renumbering each of the labels

    union(m : NFA) -> NFA
        Given a NFA m returns the union automaton (NFA)

    intersection(m : NFA) -> NFA
        Given a NFA m returns the intersection automaton (NFA)

    product(m : NFA) -> NFA
        Given a NFA m returns the product automaton (NFA)

    view(
        file_name : str, node_attr : dict[str, str] | None, edge_attr : dict[str, str] | None
    ) -> None
        Using the graphviz library, it creates a visual representation of the NFA
        and saves it as a .png file with the name file_name"""

    q: set[str]
    sigma: set[str]
    delta: dict[str, dict[str, set[str]]]
    initial_state: str
    f: set[str]

    def accept(self, string: str) -> bool:
        """
        Returns True if the given string is accepted by the NFA

        The string will be accepted if ∀a · a ∈ string ⇒ a ∈ sigma, which means
        that all the characters in string must be in sigma
        (must be in the alphabet).

        Parameters
        - - - - - - - - - - - - - - - - - -
        string : str
            A string that the NFA will try to process.

        Returns
        - - - - - - - - - - - - - - - - - -
        bool
            True if the string is accepted by the NFA, False otherwise.
        """

        def _add_pairs_to_queue(q, pairs):
            for pair in pairs:
                for state in pair:
                    q.append(state)

        # Basic Idea: Search through states (delta) in the NFA, since the initial state to the final states

        # BFS states

        q = (
            deque()
        )  # queue -> states from i to last character in S | (index, state)
        q.append([0, self.initial_state])  # Starts from 0
        ans = False  # Flag

        while q and not ans:
            front_q = q.popleft()
            idx = front_q[0]
            state = front_q[1]

            if idx == len(string) and state in self.f:
                ans = True
            elif idx < len(string) and string[idx] not in self.sigma:
                raise InputError(string[idx], "Is not declared in sigma")
            elif idx < len(string) and state in self.delta:
                # Search through states
                epsilon_transitions = filter(
                    lambda x: x[0] == "", self.delta[state].items()
                )
                epsilon_pairs = map(
                    lambda transition, idx=idx: map(
                        lambda state: [idx, state], transition[1]
                    ),
                    epsilon_transitions,
                )
                # Add epsilon transitions to the queue
                _add_pairs_to_queue(q, epsilon_pairs)

                valid_transitions = filter(
                    lambda x, idx=idx: x[0] == string[idx],
                    self.delta[state].items(),
                )
                valid_pairs = map(
                    lambda transition, idx=idx: map(
                        lambda state, idx=idx: [idx + 1, state], transition[1]
                    ),
                    valid_transitions,
                )
                # Add valid transitions to the queue
                _add_pairs_to_queue(q, valid_pairs)

        if string == "":
            ans = True

        return ans

    def is_valid(self) -> bool:
        """
        Returns True if the NFA is a valid automata.

        The NFA is valid if the following conditions are met:
        1. The initial state is in the set of states Q.
        2. All the states in the transition function delta are in the set Q.
        3. All the symbols in the transition function delta are in the alphabet
        set sigma.

        Parameters
        - - - - - - - - - - - - - - - - - -
        None

        Returns
        - - - - - - - - - - - - - - - - - -
        bool
            True if the NFA is valid, Raises an exception otherwise.
        """
        undeclared_states: set[str] | list[str] = set()

        # Validate if the initial state is in the set Q
        if self.initial_state not in self.q:
            undeclared_states.add(self.initial_state)

        undeclared_origin_states = set(
            filter(lambda x: x != "" and x not in self.q, self.delta.keys())
        )

        undeclared_sigma = list(
            set(
                filter(
                    lambda s: s != "" and s not in self.sigma,
                    [s for d in self.delta for s in self.delta[d]],
                )
            )
        )

        undeclared_destination_states = set(
            filter(
                lambda q: q not in self.q,
                [
                    q
                    for d in self.delta
                    for destination_set in self.delta[d].values()
                    for q in destination_set
                ],
            )
        )

        undeclared_final_states = set(filter(lambda f: f not in self.q, self.f))

        undeclared_states = list(
            undeclared_states
            | undeclared_origin_states
            | undeclared_destination_states
            | undeclared_final_states
        )

        if undeclared_states:
            raise SigmaError(
                undeclared_states,
                f"{'are' if len(undeclared_states) > 1 else 'is'} not declared in Q",
            )

        if undeclared_sigma:
            raise SigmaError(
                undeclared_sigma,
                f"{'are' if len(undeclared_sigma) > 1 else 'is'} not declared in sigma",
            )

        return True

    def complement(self) -> "NFA":
        """
        Returns the complement of the NFA.

        The complement of an NFA is a new NFA that accepts all the strings that
        the original NFA does not accept, and rejects all the strings that the
        original NFA accepts.

        Parameters
        - - - - - - - - - - - - - - - - - -
        None

        Returns
        - - - - - - - - - - - - - - - - - -
        NFA
            The complement of the original NFA.
        """
        q = self.q
        sigma = self.sigma
        delta = self.delta
        initial_state = self.initial_state
        f = {state for state in self.q if state not in self.f}

        return NFA(q, sigma, delta, initial_state, f)

    def _get_e_closure(
        self, q: str, visited: list[str] | None = None
    ) -> list[str]:
        """
        Returns a list of the epsilon closures from estate q.

        Parameters
        - - - - - - - - - - - - - - - - - -
        q : str
            The state from which to start the search.
        visited : list[str], optional
            A list of already visited states. Defaults to None, in which case it is initialized as a list containing q.

        Returns
        - - - - - - - - - - - - - - - - - -
        list[str]
            A list of states reachable from q by following epsilon transitions.
        """
        ans = [q]
        if visited is None:
            visited = list(q)

        if q in self.delta and "" in self.delta[q]:
            for st in self.delta[q][""]:
                if st not in visited:
                    visited.append(st)
                    ans.extend(
                        [
                            k
                            for k in self._get_e_closure(st, visited)
                            if k not in ans
                        ]
                    )
        return ans

    def contains_epsilon_transitions(self) -> bool:
        """Returns True if the NFA contains Epsilon transitions.

        Parameters
        - - - - - - - - - - - - - - - - - -
        None

        Returns
        - - - - - - - - - - - - - - - - - -
        bool
            True if the NFA contains epsilon transitions, False otherwise.
        """
        for q in self.delta:
            if "" in self.delta[q]:
                return True
        return False

    def remove_epsilon_transitions(self) -> "NFA":
        """Returns a new NFA that is equivalent to the original NFA but without epsilon transitions.

        Parameters
        - - - - - - - - - - - - - - - - - -
        None

        Returns
        - - - - - - - - - - - - - - - - - -
        NFA
            The new NFA without epsilon transitions.
        """
        q_prime = self.q.copy()
        delta_prime = self.delta.copy()
        delta_init_state = self.initial_state
        delta_f = self.f.copy()

        if not self.contains_epsilon_transitions():
            return NFA(
                q_prime, self.sigma, delta_prime, delta_init_state, delta_f
            )

        delta_prime = dict()
        for q in q_prime:
            closure_states = self._get_e_closure(q)

            for sigma in self.sigma:
                new_transitions = self._ret_get_new_transitions(
                    q, sigma, closure_states, delta_f
                )
                self._ret_update_delta(delta_prime, q, sigma, new_transitions)

        return NFA(q_prime, self.sigma, delta_prime, delta_init_state, delta_f)

    def _ret_get_new_transitions(
        self, q: str, sigma: str, closure_states: list[str], delta_f: set[str]
    ):
        to_epsilon_closure: list[str] = []
        new_transitions: list[str] = []

        # Get the transitions from sigma in each epsilon closure
        for closure_state in closure_states:
            if closure_state in self.f:
                delta_f.add(q)
            if (
                closure_state in self.delta
                and sigma in self.delta[closure_state]
            ):
                to_epsilon_closure.extend(self.delta[closure_state][sigma])

        # Get the new transitions from the epsilon closure
        for epsilon_closure in to_epsilon_closure:
            new_transitions.extend(self._get_e_closure(epsilon_closure))

        return new_transitions

    def _ret_update_delta(
        self,
        delta_prime: dict[str, dict[str, set[str]]],
        q: str,
        sigma: str,
        new_transitions: list[str],
    ):
        if q not in delta_prime:
            delta_prime[q] = dict()
        if sigma != "":
            delta_prime[q][sigma] = set(new_transitions)

    def get_dfa(self) -> DFA:
        """
        Returns a DFA (Deterministic Finite Automaton) equivalent to the NFA.

        Parameters
        - - - - - - - - - - - - - - - - - -
        None

        Returns
        - - - - - - - - - - - - - - - - - -
        DFA
            The DFA equivalent to the NFA.
        """

        local_nfa = NFA(
            self.q, self.sigma, self.delta, self.initial_state, self.f
        )
        local_nfa = local_nfa.remove_epsilon_transitions()

        q_prime = []
        delta_prime: dict[str, dict[str, str]] = dict()

        queue = deque()
        visited = [[local_nfa.initial_state]]
        queue.append([local_nfa.initial_state])

        while queue:
            qs = queue.pop()  # state Q

            local_transitions: dict[str, str] | dict[str, list[str]] = (
                dict()
            )  # {str : list}

            states_in_nfa_delta = filter(lambda q: q in local_nfa.delta, qs)

            for q in states_in_nfa_delta:
                for s in local_nfa.delta[q]:
                    tmp = local_nfa.delta[q][s].copy()
                    self._extend_local_transitions(tmp, s, local_transitions)

            self._update_local_transitions(local_transitions, visited, queue)

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

        return DFA(
            q_prime,
            local_nfa.sigma,
            delta_prime,
            str([local_nfa.initial_state]),
            f_prime,
        )

    def _extend_local_transitions(
        self, tmp: set[str], s: str, local_transitions: dict[str, list[str]]
    ) -> None:
        if tmp and s in local_transitions:
            # avoid add repeated values
            local_transitions[s].extend(
                [k for k in tmp if k not in local_transitions[s]]
            )
        elif tmp:
            local_transitions[s] = list(tmp)

    def _update_local_transitions(
        self,
        local_transitions: dict[str, list[str]],
        visited: list[list[str]],
        queue: deque,
    ) -> None:
        for transition in local_transitions:
            local_transitions[transition] = sorted(
                local_transitions[transition]
            )
            tmp = local_transitions[transition].copy()
            if tmp not in visited:
                queue.append(tmp)
                visited.append(tmp)
            local_transitions[transition] = str(local_transitions[transition])

    def minimize(self) -> "NFA":
        """Minimize the automata and return the NFA result of the minimization"""
        local_dfa = self.get_dfa()
        local_nfa = local_dfa.get_nfa()
        local_nfa.renumber()
        return local_nfa

    def renumber(self) -> None:
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
                for nxt_state in self.delta[_q][s]:
                    nxt_states.append(new_tags[nxt_state])

                delta[new_tags[_q]][s] = set(nxt_states)

        self.q, self.f, self.delta, self.initial_state = (
            q,
            f,
            delta,
            initial_state,
        )

    def union(self, m: "NFA") -> "NFA":
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
        self_delta = self._get_new_delta_real_value(self.delta, real_value_self)
        m_delta = self._get_new_delta_real_value(m.delta, real_value_m)

        delta = {
            **self_delta,
            **m_delta,
            initial_state: {
                "": {
                    real_value_self[self.initial_state],
                    real_value_m[m.initial_state],
                }
            },
        }

        return NFA(q, sigma, delta, initial_state, f)

    def _get_new_delta_real_value(
        self, delta: dict[str, dict[str, set[str]]], real_value: dict[str, str]
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

    def intersection(self, m: "NFA") -> "NFA":
        """Given a NFA m returns the intersection automaton"""
        if self.sigma != m.sigma:
            raise SigmaError(
                self.sigma,
                "The alphabet of the two automata must be the same",
            )

        new_q_list: list[tuple[str, str]] = []

        initial_state = str((self.initial_state, m.initial_state))
        delta: dict[str, dict[str, set[str]]] = dict()
        f: set[str] = set()
        sigma = self.sigma.copy()

        queue = deque()
        queue.append((self.initial_state, m.initial_state))

        while queue:
            a, b = queue.popleft()

            new_q_list.append((a, b))

            if a in self.f and b in m.f:
                f.add(str((a, b)))

            common_transitions = self.delta[a].keys() & m.delta[b].keys()

            for s in common_transitions:
                a_next_states = self.delta[a][s].copy()
                b_next_states = m.delta[b][s].copy()

                next_states: set[str] = {
                    (x, y) for x in a_next_states for y in b_next_states
                }

                unexplored_states = set(
                    filter(lambda x: x not in new_q_list, next_states)
                )

                new_q_list.extend(unexplored_states)

                for x, y in unexplored_states:
                    queue.append((x, y))

                if str((a, b)) not in delta:
                    delta[str((a, b))] = dict()

                delta[str((a, b))][s] = set(map(str, next_states))

        return NFA(set(map(str, new_q_list)), sigma, delta, initial_state, f)

    def product(self, m: "NFA") -> "NFA":
        """Given a DFA M returns the product automaton"""
        # Using DFA conversion
        a = self.get_dfa()
        b = m.get_dfa()

        nfa = a.product(b).get_nfa()

        return nfa

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

        for _f in self.f:
            dot.node(_f, _f, shape="doublecircle")

        for _q in self.q:
            if _q not in self.f:
                dot.node(_q, _q, shape="circle")

        dot.edge("", self.initial_state, label="")

        for q in self.delta:
            for s in self.delta[q]:
                for t in self.delta[q][s]:
                    if s == "":
                        dot.edge(q, t, label="ε")
                    else:
                        dot.edge(q, t, label=s)

        dot.render()
