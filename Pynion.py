from collections import Callable
from pprint import pprint
from typing import Optional, List

from Middleware import Middleware, sig_handler


class Pynion:
    def __init__(self, handler: sig_handler):
        self._stack: List[Middleware] = []
        self._handler = handler

        return

    def __call__(self, event: dict, context: dict):
        result = event
        ejected = False

        def fn_abort(value):
            nonlocal result
            nonlocal ejected
            result = value
            ejected = True

        # err_handlers = [handler.err_handler for handler in self._stack if handler.err_handler]
        pre_handlers = [handler.pre_handler for handler in self._stack if handler.pre_handler]
        for pre in pre_handlers:
            if ejected: return result
            try:
                result = pre(result, context, fn_abort, event)
            except Exception as ex:
                pprint(ex)

        if ejected: return result
        try:
            result = self._handler(result, context, fn_abort, event)
        except Exception as ex:
            pprint(ex)

        post_handlers = [handler.post_handler for handler in self._stack if handler.post_handler][::-1]
        for post in post_handlers:
            if ejected: return result
            try:
                result = post(result, context, fn_abort, event)
            except Exception as ex:
                pprint(ex)

        return result

    def use(self, middleware: Middleware):
        """Add a middleware handler to the stack"""
        self._stack.append(middleware)
        return self

    def pre(self, fn: Callable, name: Optional[str]):
        self._stack.append(Middleware(pre=fn, name=name or fn.__name__))
        return self

    def post(self, fn: Callable, name: Optional[str]):
        self._stack.append(Middleware(post=fn, name=name or fn.__name__))
        return self

    def err(self, fn: Callable, name: Optional[str]):
        self._stack.append(Middleware(err=fn, name=name or fn.__name__))
        return self

    def instrument(self, fn: Callable):
        raise NotImplemented()
        return self

    def concatenate(self, stack: [Middleware]):
        """Append a pre-built stack of middleware functions to the Pynion middleware list"""
        self._stack.extend(stack)
        return self
