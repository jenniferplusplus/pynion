from typing import Callable, Optional, Union

sig_eject = Callable[[object], None]

sig_handler = Callable[[object, object, Optional[sig_eject], Optional[object]], object]
"""
:arg: the triggering event, possibly transformed by previous middleware
:arg: the environmental context
:arg: the abort function
:arg: the unmodified triggering event
:returns: the value to proceed with
"""
sig_err = Callable[[Exception, object, object, sig_eject], Union[object, Exception]]
"""
:arg: The Exception
:arg: event
:arg: context
:arg: the abort function
:returns: an exception or—if the exception is resolved—the value to proceed with 
"""


class Middleware:
    def __init__(self, *, pre=None, post=None, err=None, name=str):
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
