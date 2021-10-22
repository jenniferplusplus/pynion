from Middleware import Middleware


def _handler():
    pass


def test_middleware():
    actual = Middleware(pre=_handler, post=_handler, err=_handler, name='test middleware')

    assert actual
