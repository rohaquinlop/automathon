from typing import (
    Callable,
    TypeVar,
    Iterable,
    List,
)

_A = TypeVar("_A")
_B = TypeVar("_B")


def list_map(function: Callable[[_A], _B], iter: Iterable[_A]) -> List[_B]:
    return list(map(function, iter))


def list_filter(function: Callable[[_A], bool], iter: Iterable[_A]) -> List[_A]:
    return list(filter(function, iter))


def flatten_list(lst: List[List[_A]]) -> List[_A]:
    return sum(lst, [])
