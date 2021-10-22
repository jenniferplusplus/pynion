from typing import Callable, Optional

sig_eject = Callable[[object], None]
sig_handler = Callable[[object, object, Optional[sig_eject], Optional[object]], object]
sig_err = Callable[[object, object, Optional[sig_eject], Optional[object]], object]


class Middleware:
    def __init__(self, *, pre=sig_handler, post=sig_handler, err=sig_handler, name=str):
        """
        :param pre: A function to be executed before the main handler logic. This could, for example perform
        validations or enrich the event argument before it reaches the handler.
        :param post: A function to be executed after the main handler logic. It could enrich the result or trigger
        side-effects.
        :param err: A function that will have a chance to handle errors raised during processing.
        :param name: A human readable name for this middleware instance, which may be used in logs or other output.
        """
        self._pre = pre
        self._post = post
        self._err = err
        self._name = name
        return

    @property
    def name(self):
        return self._name

    @property
    def pre_handler(self) -> Callable:
        return self._pre

    @property
    def post_handler(self) -> Callable:
        return self._post

    @property
    def err_handler(self) -> Callable:
        return self._err
