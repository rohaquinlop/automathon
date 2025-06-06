# Exceptions module
from __future__ import (
    annotations,
)
from automathon.finite_automata.finite_automata import FA
from automathon.finite_automata.dfa import (
    DFA,
)
from automathon.utils.utils import (
    list_filter,
    list_map,
    flatten_list,
)
from collections import (
    deque,
)
from typing import (
    Literal,
    Set,
    Dict,
    List,
    Optional,
    Tuple,
)


class NFA(FA):
    """A Class used to represent a Non-Deterministic Finite Automaton

    Attributes
    ----------
    q : Set[str]
        Set of strings where each string represent the states.
        Ex:
            q = {'q0', 'q1', 'q2'}

    sigma : Set[str]
        Set of strings that represents the alphabet.
        Ex:
            sigma = {'0', '1'}

    delta : Dict[str, Dict[str, Set[str]]]
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

    f : Set[str]
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

    _get_e_closure(q : str, visited : List[str] | None) -> List[str]
        Returns a list of the epsilon closures from estate q

    _get_new_delta_real_value(
        delta : Dict[str, Dict[str, Set[str]]], real_value : Dict[str, str]
    ) -> Dict[str, Dict[str, Set[str]]]
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
        file_name : str, node_attr : Dict[str, str] | None, edge_attr : Dict[str, str] | None
    ) -> None
        Using the graphviz library, it creates a visual representation of the NFA
        and saves it as a .png file with the name file_name"""

    def __init__(
        self,
        q: Set[str],
        sigma: Set[str],
        delta: Dict[str, Dict[str, Set[str]]],
        initial_state: str,
        f: Set[str],
    ) -> None:
        """Initialize a Non-Deterministic Finite Automaton.

        Args:
            q: Set of states
            sigma: Set of input symbols (alphabet)
            delta: Transition function
            initial_state: Initial state
            f: Set of final states
        """
        super().__init__(q, sigma, delta, initial_state, f)

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

        def _add_pairs_to_queue(
            q: deque[Tuple[int, str]], pairs: List[Tuple[int, str]]
        ):
            for pair in pairs:
                q.append(pair)

        # Basic Idea: Search through states (delta) in the NFA, since the initial state to the final states

        # BFS states

        q: deque[Tuple[int, str]] = deque()
        # queue -> states from i to last character in S | (index, state)
        q.append([0, self.initial_state])  # Starts from 0
        ans = False  # Flag

        while q and not ans:
            front_q = q.popleft()
            idx = front_q[0]
            state = front_q[1]

            if idx == len(string) and state in self.f:
                ans = True
            elif idx < len(string):
                # Search through states
                epsilon_transitions = filter(
                    lambda x: x[0] == "", self.delta[state].items()
                )
                epsilon_pairs = flatten_list(
                    list_map(
                        lambda transition, idx=idx: list_map(
                            lambda state: (idx, state), transition[1]
                        ),
                        epsilon_transitions,
                    )
                )
                # Add epsilon transitions to the queue
                _add_pairs_to_queue(q, epsilon_pairs)

                valid_transitions = list_filter(
                    lambda x, idx=idx: x[0] == string[idx],
                    self.delta[state].items(),
                )
                valid_pairs = flatten_list(
                    list_map(
                        lambda transition, idx=idx: list_map(
                            lambda state, idx=idx: (idx + 1, state),
                            transition[1],
                        ),
                        valid_transitions,
                    )
                )
                # Add valid transitions to the queue
                _add_pairs_to_queue(q, valid_pairs)

        return ans

    def is_valid(self) -> bool:
        """Returns True if the NFA is a valid automata.

        The NFA is valid if the following conditions are met:
        1. The initial state is in the set of states Q.
        2. All the states in the transition function delta are in the set Q.
        3. All the symbols in the transition function delta are in the alphabet
        set sigma.

        Returns
        -------
        bool
            True if the NFA is valid, False otherwise.
        """
        return (
            self._validate_initial_state()
            and self._validate_final_states()
            and self._validate_transitions()
        )

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
        dfa = self.get_dfa()
        dfa = dfa.complement()
        nfa = dfa.get_nfa()
        nfa.renumber()
        return nfa.minimize()

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
            closure_states = self.__get_e_closure(q)

            for sigma in self.sigma:
                new_transitions = self.__ret_get_new_transitions(
                    q, sigma, closure_states, delta_f
                )
                self.__ret_update_delta(delta_prime, q, sigma, new_transitions)

        return NFA(q_prime, self.sigma, delta_prime, delta_init_state, delta_f)

    def __get_e_closure(
        self, q: str, visited: List[str] | None = None
    ) -> List[str]:
        """
        Returns a list of the epsilon closures from estate q.

        Parameters
        - - - - - - - - - - - - - - - - - -
        q : str
            The state from which to start the search.
        visited : List[str], optional
            A list of already visited states. Defaults to None, in which case it is initialized as a list containing q.

        Returns
        - - - - - - - - - - - - - - - - - -
        List[str]
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
                            for k in self.__get_e_closure(st, visited)
                            if k not in ans
                        ]
                    )
        return ans

    def __ret_get_new_transitions(
        self, q: str, sigma: str, closure_states: List[str], delta_f: Set[str]
    ):
        to_epsilon_closure: List[str] = []
        new_transitions: List[str] = []

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
            new_transitions.extend(self.__get_e_closure(epsilon_closure))

        return new_transitions

    def __ret_update_delta(
        self,
        delta_prime: Dict[str, Dict[str, Set[str]]],
        q: str,
        sigma: str,
        new_transitions: List[str],
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
        delta_prime: Dict[str, Dict[str, str]] = dict()

        queue = deque()
        visited = [[local_nfa.initial_state]]
        queue.append([local_nfa.initial_state])

        while queue:
            qs = queue.pop()  # state Q

            local_transitions: Dict[str, str] | Dict[str, List[str]] = (
                dict()
            )  # {str : list}

            states_in_nfa_delta = filter(lambda q: q in local_nfa.delta, qs)

            for q in states_in_nfa_delta:
                for s in local_nfa.delta[q]:
                    tmp = local_nfa.delta[q][s].copy()
                    self.__extend_local_transitions(tmp, s, local_transitions)

            self.__update_local_transitions(local_transitions, visited, queue)

            delta_prime[str(qs)] = local_transitions
            q_prime.append(qs)

        f_prime = set()
        aux = set()

        for qs in q_prime:
            for q in qs:
                if q in local_nfa.f:
                    f_prime.add(str(qs))
                    break

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

    def __extend_local_transitions(
        self, tmp: Set[str], s: str, local_transitions: Dict[str, List[str]]
    ) -> None:
        if tmp and s in local_transitions:
            # avoid add repeated values
            local_transitions[s].extend(
                [k for k in tmp if k not in local_transitions[s]]
            )
        elif tmp:
            local_transitions[s] = list(tmp)

    def __update_local_transitions(
        self,
        local_transitions: Dict[str, List[str]],
        visited: List[List[str]],
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
        local_dfa = self.get_dfa().minimize()
        local_nfa = local_dfa.get_nfa()
        local_nfa.renumber()
        return local_nfa

    def renumber(self, prefix="q") -> None:
        """
        Change the name of the states, renumbering each of the labels

        Parameters
        ----------
        prefix : str
            Prefix for the renumbered state names.
        """

        delta = dict()

        # Create new mappings for states
        new_tags = {state: f"{prefix}{idx}" for idx, state in enumerate(self.q)}

        # Update states
        q = {new_tags[state] for state in self.q}
        f = {new_tags[state] for state in self.f}
        initial_state = new_tags[self.initial_state]

        # Update transitions
        for _q in self.delta:
            delta[new_tags[_q]] = dict()
            for s in self.delta[_q]:
                delta[new_tags[_q]][s] = {
                    new_tags[nxt_state] for nxt_state in self.delta[_q][s]
                }

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
        self_delta = self.__get_new_delta_real_value(
            self.delta, real_value_self
        )
        m_delta = self.__get_new_delta_real_value(m.delta, real_value_m)

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

    def __get_new_delta_real_value(
        self, delta: Dict[str, Dict[str, Set[str]]], real_value: Dict[str, str]
    ) -> Dict[str, Dict[str, Set[str]]]:
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
            return NFA(
                set(), set(), dict(), "", set()
            )  # Return empty NFA for invalid intersection

        new_q_list: List[Tuple[str, str]] = []

        initial_state = str((self.initial_state, m.initial_state))
        delta: Dict[str, Dict[str, Set[str]]] = dict()
        f: Set[str] = set()
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

                next_states: Set[str] = {
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
        file_format: Literal["svg", "png"] = "png",
        node_attr: Optional[Dict[str, str]] = None,
        edge_attr: Optional[Dict[str, str]] = None,
    ) -> None:
        """Create a visual representation of the NFA.

        Args:
            file_name: Name of the output file
            file_format: Format of the output file (svg or png)
            node_attr: Attributes for nodes in the visualization
            edge_attr: Attributes for edges in the visualization
        """
        dot = self._create_base_graph(
            file_name, file_format, node_attr, edge_attr
        )

        for q in self.delta:
            for s in self.delta[q]:
                for t in self.delta[q][s]:
                    if s == "":
                        dot.edge(q, t, label="ε")
                    else:
                        dot.edge(q, t, label=s)

        dot.render()
