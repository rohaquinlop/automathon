from automathon.utils.utils import list_map
from .finite_automata import FA
from collections import deque
from typing import (
    Callable,
    Literal,
    Set,
    Dict,
    List,
    Tuple,
    Optional,
    FrozenSet,
)
import itertools


class DFA(FA):
    """A class used to represent a Deterministic Finite Automaton (DFA).

    Attributes
    ----------
    q : Set[str]
        Set of strings where each string represents a state.
        Example: q = {'q0', 'q1', 'q2'}

    sigma : Set[str]
        Set of strings that represents the alphabet.
        Example: sigma = {'0', '1'}

    delta : Dict[str, Dict[str, str]]
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

    f : Set[str]
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

    union(m: DFA) -> DFA
        Given a DFA m, returns the union automaton.

    intersection(m: DFA) -> DFA
        Given a DFA m, returns the intersection automaton.

    difference(m: DFA) -> DFA
        Given a DFA m, returns the difference automaton.

    symmetric_difference(m: DFA) -> DFA
        Given a DFA m, returns the symmetric difference automaton.

    product(m: DFA) -> DFA
        Given a DFA m, returns the product automaton.

    get_nfa() -> NFA
        Converts the actual DFA to NFA and returns its conversion.

    minimize() -> DFA
        Minimize the automata and return the minimized version.

    view(
        file_name : str, node_attr : Dict[str, str] | None, edge_attr : Dict[str, str] | None
    ) -> None
        Using the graphviz library, it creates a visual representation of the DFA
        and saves it as a .png file with the name file_name
    """

    def __init__(
        self,
        q: Set[str],
        sigma: Set[str],
        delta: Dict[str, Dict[str, str]],
        initial_state: str,
        f: Set[str],
    ) -> None:
        """Initialize a Deterministic Finite Automaton.

        Args:
            q: Set of states
            sigma: Set of input symbols (alphabet)
            delta: Transition function
            initial_state: Initial state
            f: Set of final states
        """
        super().__init__(q, sigma, delta, initial_state, f)

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
        q: deque[Tuple[int, str]] = deque()
        q.append([0, self.initial_state])

        while q and not ans:
            idx, state = q.popleft()

            if idx == len(string) and state in self.f:
                ans = True
            elif idx < len(string):
                # Search through states
                for a, state in self.delta[state].items():
                    # transition: ('1', 'q0')
                    if string[idx] == a:
                        q.append([idx + 1, state])

        return ans

    def is_valid(self) -> bool:
        """Returns True if the DFA is a valid automata"""
        return (
            self._validate_initial_state()
            and self._validate_final_states()
            and self._validate_transitions()
        )

    def complement(self) -> "DFA":
        """Returns the complement of the DFA."""
        q = self.q
        sigma = self.sigma
        delta = self.delta
        initial_state = self.initial_state
        f = {state for state in self.q if state not in self.f}

        return DFA(q, sigma, delta, initial_state, f)

    def __binary_operation(
        self,
        m: "DFA",
        operation: Callable[[str, Set[str], str, Set[str]], bool],
    ) -> "DFA":
        new_q_list: List[Tuple[str, str]] = []

        initial_state = str((self.initial_state, m.initial_state))
        delta: Dict[str, Dict[str, str]] = dict()
        sigma: Set[str] = self.sigma.copy()
        f: Set[str] = set()

        # Check if both sigmas are the same
        if self.sigma != m.sigma:
            raise Exception(
                f"{self.sigma}, Sigma from both DFAs must be the same"
            )

        queue: deque[Tuple[str, str]] = deque()
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

    def product(self, m: "DFA") -> "DFA":
        initial_state = str((self.initial_state, m.initial_state))
        cross_product_states = {
            (q_1, q_2) for q_1, q_2 in itertools.product(self.q, m.q)
        }
        q = {str(state) for state in cross_product_states}
        sigma = self.sigma & m.sigma
        f = {
            str((q_1, q_2))
            for (q_1, q_2) in cross_product_states
            if q_1 in self.f and q_2 in m.f
        }
        delta: Dict[str, Dict[str, str]] = dict()

        for q_1, q_2 in cross_product_states:
            actual_state = str((q_1, q_2))
            delta[actual_state] = dict()
            common_sigma = filter(
                lambda x: x in sigma,
                set(self.delta[q_1].keys()) | set(m.delta[q_2].keys()),
            )

            for a in common_sigma:
                delta[actual_state][a] = str(
                    (self.delta[q_1][a], m.delta[q_2][a])
                )

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
                tmp[s] = [_q]

            delta[state] = tmp

        return NFA(q, sigma, delta, initial_state, f)

    def __states_idx_table(self, p_k: Set[FrozenSet[str]]) -> Dict[str, int]:
        states_idx: Dict[str, int] = dict()

        for i in range(len(p_k)):
            for state in list(p_k)[i]:
                states_idx[state] = i

        return states_idx

    def __define_group_ith_element(
        self,
        i: int,
        new_p_k: List[Set[str]],
        p_i_sigma: Set[str],
        p_states_lst: List[str],
        states_idx: Dict[str, int],
    ) -> Tuple[List[Set[str]], bool]:
        was_added = False
        for new_p_states in new_p_k:
            new_p_states_lst = list(new_p_states)
            new_p_sigma = set(self.delta[new_p_states_lst[0]].keys())

            if p_i_sigma != new_p_sigma:
                continue

            are_equivalent = all(
                list_map(
                    lambda s,
                    p=p_states_lst[i],
                    q=new_p_states_lst[0],
                    table=states_idx,
                    delta=self.delta: table[delta[p][s]] == table[delta[q][s]],
                    p_i_sigma,
                )
            )

            if are_equivalent:
                new_p_states.add(p_states_lst[i])
                was_added = True
                break

        return new_p_k, was_added

    def minimize(self) -> "DFA":
        """Minimize the automata and return the minimized version"""
        p_k: Set[FrozenSet[str]] = set(
            [frozenset([*self.q.difference(self.f)]), frozenset([*self.f])]
        )
        p_prev: Set[FrozenSet[str]] = set()

        while p_k != p_prev:
            states_idx: Dict[str, int] = self.__states_idx_table(p_k)
            new_p_k: List[Set[str]] = []

            for p_states in p_k:
                p_states_lst = list(p_states)
                new_p_k.append({p_states_lst[0]})

                for i in range(1, len(p_states_lst)):
                    was_added = False
                    p_i_sigma = set(self.delta[p_states_lst[i]].keys())

                    new_p_k, was_added = self.__define_group_ith_element(
                        i, new_p_k, p_i_sigma, p_states_lst, states_idx
                    )

                    if not was_added:
                        new_p_k.append({p_states_lst[i]})

            p_prev, p_k = p_k, set(map(lambda s: frozenset([*s]), new_p_k))

        states_idx: Dict[str, int] = self.__states_idx_table(p_k)
        initial_state = f"q{states_idx[self.initial_state]}"
        final_states = set(list_map(lambda s: f"q{states_idx[s]}", self.f))

        delta: Dict[str, Dict[str, str]] = dict()
        states = set(list_map(lambda idx: f"q{idx}", states_idx.values()))

        for state_group in p_k:
            fst_state = list(state_group)[0]

            delta[f"q{states_idx[fst_state]}"] = dict()

            for s in self.delta[fst_state]:
                delta[f"q{states_idx[fst_state]}"][s] = (
                    f"q{states_idx[self.delta[fst_state][s]]}"
                )

        return DFA(
            states, self.sigma.copy(), delta, initial_state, final_states
        )

    def view(
        self,
        file_name: str,
        file_format: Literal["svg", "png"] = "png",
        node_attr: Optional[Dict[str, str]] = None,
        edge_attr: Optional[Dict[str, str]] = None,
    ) -> None:
        """Create a visual representation of the DFA.

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
                dot.edge(q, self.delta[q][s], label=s)

        dot.render()
