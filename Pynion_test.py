from collections import Callable

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


def _err_aborts(ex, ev, ct, abort):
    return abort('aborted')


def _aborts(ev, ct, abort, o_ev):
    return abort('aborted')



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


def test_handles_errors_from_pre(mocker: MockFixture):
    err_handler = mocker.stub()
    ex = Exception()

    def throws(ev, ct, abort, o_ev):
        raise ex

    pyn = Pynion(_handler).pre(throws).err(err_handler)

    pyn({}, {})

    err_handler.assert_called_once()


def test_handles_errors_from_handler(mocker: MockFixture):
    err_handler = mocker.stub()
    ex = Exception()

    def throws(ev, ct, abort, o_ev):
        raise ex

    pyn = Pynion(throws).err(err_handler)

    pyn({}, {})

    err_handler.assert_called_once()


def test_handles_errors_from_post(mocker: MockFixture):
    err_handler = mocker.stub()
    ex = Exception()

    def throws(ev, ct, abort, o_ev):
        raise ex

    pyn = Pynion(_handler).post(throws).err(err_handler)

    pyn({}, {})

    err_handler.assert_called_once()


def test_can_abort_from_pre(mocker: MockFixture):
    handler = mocker.stub()
    post = mocker.stub()
    err = mocker.stub()

    pyn = Pynion(handler).use(Middleware(pre=_aborts, post=post, err=err))

    result = pyn({}, {})

    handler.assert_not_called()
    post.assert_not_called()
    err.assert_not_called()
    assert result == 'aborted'


def test_can_abort_from_handler(mocker: MockFixture):
    pre = mocker.stub()
    post = mocker.stub()
    err = mocker.stub()

    pyn = Pynion(_aborts).use(Middleware(pre=pre, post=post, err=err))

    result = pyn({}, {})

    pre.assert_called_once()
    post.assert_not_called()
    err.assert_not_called()
    assert result == 'aborted'


def test_can_abort_from_post(mocker: MockFixture):
    pre = mocker.stub()
    post = _aborts
    err = mocker.stub()
    handler = mocker.stub()

    pyn = Pynion(handler).use(Middleware(pre=pre, post=post, err=err))

    result = pyn({}, {})

    pre.assert_called_once()
    handler.assert_called_once()
    err.assert_not_called()
    assert result == 'aborted'


def test_can_abort_from_err(mocker: MockFixture):
    ex = Exception()

    def throws(ev, ct, abort, o_ev):
        raise ex

    pre = mocker.stub()
    post = mocker.stub()
    err = _err_aborts
    handler = throws

    pyn = Pynion(handler).use(Middleware(pre=pre, post=post, err=err))

    result = pyn({}, {})

    pre.assert_called_once()
    post.assert_not_called()
    assert result == 'aborted'