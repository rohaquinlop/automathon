from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Literal,
    Set,
    Dict,
    Any,
    Optional,
    Union,
)
from graphviz import Digraph


class FA(ABC):
    """Abstract base class for Finite Automata.

    This class defines the common interface and attributes for all types of finite automata.
    """

    def __init__(
        self,
        q: Set[str],
        sigma: Set[str],
        delta: Dict[str, Dict[str, Any]],
        initial_state: str,
        f: Set[str],
    ) -> None:
        """Initialize a Finite Automaton.

        Args:
            q: Set of states
            sigma: Set of input symbols (alphabet)
            delta: Transition function
            initial_state: Initial state
            f: Set of final states
        """
        self.q = q
        self.sigma = sigma
        self.delta = delta
        self.initial_state = initial_state
        self.f = f

    @abstractmethod
    def accept(self, string: str) -> bool:
        """Check if the automaton accepts a given string.

        Args:
            string: Input string to check

        Returns:
            True if the string is accepted, False otherwise
        """
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        """Validate the automaton's configuration.

        Returns:
            True if the automaton is valid, raises exception otherwise
        """
        pass

    @abstractmethod
    def complement(self) -> "FA":
        """Create the complement of this automaton.

        Returns:
            A new automaton that accepts all strings not accepted by this one
        """
        pass

    @abstractmethod
    def union(self, fa: "FA") -> "FA":
        """Create the union of this automaton with another.

        Args:
            fa: Another finite automaton

        Returns:
            A new automaton that accepts strings accepted by either automaton
        """
        pass

    @abstractmethod
    def intersection(self, fa: "FA") -> "FA":
        """Create the intersection of this automaton with another.

        Args:
            fa: Another finite automaton

        Returns:
            A new automaton that accepts strings accepted by both automata
        """
        pass

    @abstractmethod
    def product(self, fa: "FA") -> "FA":
        """Create the product of this automaton with another.

        Args:
            fa: Another finite automaton

        Returns:
            A new automaton representing the product of both automata
        """
        pass

    def _validate_initial_state(self) -> bool:
        """Validate that the initial state is in the set of states.

        Returns:
            True if the initial state is valid, False otherwise
        """
        return self.initial_state in self.q

    def _validate_final_states(self) -> bool:
        """Validate that all final states are in the set of states.

        Returns:
            True if all final states are valid, False otherwise
        """
        return all(f in self.q for f in self.f)

    def _validate_transition(
        self, q: Set[str], next_state: Union[str, Set[str]]
    ) -> bool:
        if isinstance(next_state, str):
            return next_state in q
        elif isinstance(next_state, set):
            return all(ns in q for ns in next_state)

    def _validate_transitions(self) -> bool:
        """Validate that all transitions are valid.

        Returns:
            True if all transitions are valid, False otherwise
        """
        for state in self.delta:
            if state not in self.q:
                return False

            for symbol, next_state in self.delta[state].items():
                if symbol and symbol not in self.sigma:
                    return False

                if not self._validate_transition(self.q, next_state):
                    return False

        return True

    def _create_base_graph(
        self,
        file_name: str,
        file_format: Literal["svg", "png"] = "png",
        node_attr: Optional[Dict[str, str]] = None,
        edge_attr: Optional[Dict[str, str]] = None,
    ) -> Digraph:
        """Create a base graph for visualization.

        Args:
            file_name: Name of the output file
            file_format: Format of the output file (svg or png)
            node_attr: Attributes for nodes in the visualization
            edge_attr: Attributes for edges in the visualization

        Returns:
            A configured Digraph object
        """
        dot = Digraph(
            name=file_name,
            format=file_format,
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
        return dot

    @abstractmethod
    def view(
        self,
        file_name: str,
        file_format: Literal["svg", "png"] = "png",
        node_attr: Optional[Dict[str, str]] = None,
        edge_attr: Optional[Dict[str, str]] = None,
    ) -> None:
        """Create a visual representation of the automaton.

        Args:
            file_name: Name of the output file
            file_format: Format of the output file (svg or png)
            node_attr: Attributes for nodes in the visualization
            edge_attr: Attributes for edges in the visualization
        """
        pass
