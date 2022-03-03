import os
from typing import Callable, List, Optional, TypeVar


T = TypeVar('T')


def get_from_environment(name: str, cast: Callable[[str], T] = str) -> Optional[T]:
    value = os.environ.get(name)

    if value is not None:
        return cast(value)


def get_array_from_environment(name: str, cast: Callable[[str], T] = str) -> Optional[List[T]]:
    value = os.environ.get(name)

    if value is not None:
        return list(map(cast, value.split(',')))
