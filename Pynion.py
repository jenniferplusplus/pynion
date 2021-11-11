from typing import List, Callable

from Middleware import Middleware, sig_handler


class Pynion:
    def __init__(self, handler: sig_handler):
        self._stack: List[Middleware] = []
        self._handler = handler
        self._aborted: bool = False
        self._result: object = None

        return

    @property
    def aborted(self) -> bool:
        return self._aborted

    @aborted.setter
    def aborted(self, value: bool):
        self._aborted = value

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value):
        self._result = value if not self.aborted else self._result

    def __call__(self, event: dict, context: dict):
        self.result = event.copy()

        def fn_abort(value):
            """The abort callback"""
            nonlocal self
            # nonlocal aborted
            self.result = value
            self.aborted = True

        # noinspection PyShadowingNames
        def on_error(err_fns, ex, result, context) -> object:
            for fn_err in err_fns:
                value = fn_err(ex, result, context, fn_abort)
                if not isinstance(value, Exception):
                    return value
            raise ex

        err_handlers = [handler.err_handler for handler in self._stack if handler.err_handler]
        pre_handlers = [handler.pre_handler for handler in self._stack if handler.pre_handler]
        for pre in pre_handlers:
            if self.aborted: return self.result
            try:
                self.result = pre(self.result, context, fn_abort, event)
            except Exception as ex:
                self.result = on_error(err_handlers, ex, self.result, context)

        if self.aborted: return self.result
        try:
            self.result = self._handler(self.result, context, fn_abort, event)
        except Exception as ex:
            self.result = on_error(err_handlers, ex, self.result, context)

        post_handlers = [handler.post_handler for handler in self._stack if handler.post_handler][::-1]
        for post in post_handlers:
            if self.aborted: return self.result
            try:
                self.result = post(self.result, context, fn_abort, event)
            except Exception as ex:
                self.result = on_error(err_handlers, ex, self.result, context)

        return self.result

    def use(self, middleware: Middleware):
        """Add a full middleware handler to the stack"""
        assert isinstance(middleware, Middleware)
        self._stack.append(middleware)
        return self

    def pre(self, fn: Callable, name=None):
        """Add a single pre-handler function to the stack"""
        assert callable(fn)
        self._stack.append(Middleware(pre=fn, name=name or fn.__name__))
        return self

    def post(self, fn: Callable, name=None):
        """Add a single post-handler function to the stack"""
        assert callable(fn)
        self._stack.append(Middleware(post=fn, name=name or fn.__name__))
        return self

    def err(self, fn: Callable, name=None):
        """Add a single error handler function to the stack"""
        assert callable(fn)
        self._stack.append(Middleware(err=fn, name=name or fn.__name__))
        return self

    def instrument(self, fn: Callable):
        raise NotImplemented()
        return self

    def concatenate(self, stack: [Middleware]):
        """Append a pre-built stack of middleware functions to the Pynion middleware list"""
        self._stack.extend(stack)
        return self
