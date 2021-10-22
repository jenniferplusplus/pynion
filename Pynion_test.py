from pytest_mock import MockFixture
from Middleware import Middleware
from Pynion import Pynion


def _handler(event, context, abort, result):
    return


def _pre(event, context, abort, result):
    return


def _post(event, context, abort, result):
    return


def _err(event, context, abort, result):
    return


middleware = Middleware(pre=_pre, post=_post, err=_err, name='test middleware')


def test_pynion():
    actual = Pynion(_handler)

    assert actual


def test_use_should_add_to_stack():
    pyn = Pynion(_handler)
    pyn.use(middleware)

    assert len(pyn._stack) == 1


def test_pre_should_add_to_stack():
    pyn = Pynion(_handler)
    pyn.pre(_pre)

    assert len(pyn._stack) == 1


def test_post_should_add_to_stack():
    pyn = Pynion(_handler)
    pyn.post(_post)

    assert len(pyn._stack) == 1


def test_err_should_add_to_stack():
    pyn = Pynion(_handler)
    pyn.err(_err)

    assert len(pyn._stack) == 1


def test_can_add_multiple():
    pyn = Pynion(_handler)
    pyn.use(middleware).use(middleware)
    pyn.err(_err)

    assert len(pyn._stack) == 3


def test_can_execute_handler(mocker: MockFixture):
    handler = mocker.stub()
    pyn = Pynion(handler)

    pyn({}, {})

    assert handler.call_count == 1


def test_can_execute_pre_handlers(mocker: MockFixture):
    pre = mocker.stub()
    pyn = Pynion(_handler).pre(pre)

    pyn({}, {})

    assert pre.call_count == 1


def test_can_execute_post_handlers(mocker: MockFixture):
    post = mocker.stub()
    pyn = Pynion(_handler).post(post)

    pyn({}, {})

    assert post.call_count == 1
