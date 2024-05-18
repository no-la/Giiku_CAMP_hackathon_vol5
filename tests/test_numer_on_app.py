import pytest
import logging

from .context import settings
from .context import conftest
from .context import numer_on_app
from .context import file_utils


def test_hoge1():
    app = numer_on_app.NumerOnApp("123")
    assert app.n == 0
    app.increment()
    assert app.n == 1
    app.increment()
    assert app.n == 2
    

def test_judge1():
    app = numer_on_app.NumerOnApp("123")
    eat, bite = app.judge("123")
    assert eat == 3
    assert bite == 3

def test_judge2():
    app = numer_on_app.NumerOnApp("123")
    eat, bite = app.judge("322")
    assert eat == 1
    assert bite == 2
