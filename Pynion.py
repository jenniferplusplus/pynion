from collections import Callable
from typing import Optional

import Middleware


class Pynion:
    def __init__(self, handler: Callable[object, object, Optional[Callable], Optional[object]]):
        self._stack = [Middleware]
        self._handler = handler

        return

    def __call__(self, *args, **kwargs):
        pass

    def use(self, middleware: Middleware):
        """:arg middleware a Middleware object"""

        self.stack.append(middleware)

    def pre(self, fn: Callable, name: Optional[str]):
        pass

    def post(self, fn: Callable, name: Optional[str]):
        pass

    def err(self, fn: Callable, name: Optional[str]):
        pass

    def instrument(self, fn: Callable):
        pass

    def append(self, stack: [Middleware]):
        pass
