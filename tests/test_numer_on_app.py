import pytest
import logging

from .context import settings
from .context import conftest
from .context import numer_on_app
from .context import file_utils


def test_hoge1():
    app = numer_on_app.NumerOnApp("123")
    assert app.judge_count == 0
    app.judge("111")
    assert app.judge_count == 1
    app.judge("122")
    assert app.judge_count == 2
    

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

def test_judge3():
    app = numer_on_app.NumerOnApp("123")
    with pytest.raises(ValueError) as e:
        app.judge("222222")
    assert e.type == ValueError 
    