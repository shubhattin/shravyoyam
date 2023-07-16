from typing import TypeVar, Generic, Callable, List

T = TypeVar("T")


class State(Generic[T]):
    def __init__(self, value: T):
        self.__value: T = value
        self.__callbacks: List[Callable[[T], None]] = []

    def get(self) -> T:
        return self.__value

    def set(self, value: T):
        self.__value = value
        for callback_func in self.__callbacks:
            callback_func(value)

    def add_callback(self, callback: Callable[[T], None]) -> None:
        """Callback to run on each `state change`"""
        self.__callbacks.append(callback)
