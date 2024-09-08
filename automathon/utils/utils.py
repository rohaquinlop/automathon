from typing import (
    Callable,
    TypeVar,
    Iterable,
)

_A = TypeVar("_A")
_B = TypeVar("_B")


def list_map(function: Callable[[_A], _B], iter: Iterable[_A]) -> list[_B]:
    return list(map(function, iter))


def list_filter(function: Callable[[_A], bool], iter: Iterable[_A]) -> list[_A]:
    return list(filter(function, iter))


def flatten_list(lst: list[list[_A]]) -> list[_A]:
    return sum(lst, [])
