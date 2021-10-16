from collections import Callable
from typing import Optional

import Middleware


class Pynion:
    def __init__(self, handler: Callable[object, object, Optional[Callable], Optional[object]]):
        self._stack = [Middleware]
        self._handler = handler

        pass

    def __call__(self, *args, **kwargs):
        return self._handler

    def use(self, middleware: Middleware):
        """:arg middleware a Middleware object"""

        self.stack.append(middleware)

