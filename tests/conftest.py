import json as json_

import pytest

from config import settings


CSV_NAME = "test.csv"
CSV_CONTENT = [["1", "2", "3"],
               ["4", "5", "6"],
               ["7", "8", "9"],
               ]
JSON_NAME = "test.json"
JSON_CONTENT = {"a":0, "b":1, "c":2}
TXT_NAME = "test.txt"
TXT_CONTENT = "abcdefg012345"
PNG_NAME = "test.png"
PNG_CONTENT = "0"
GIF_NAME = "test.gif"
GIF_CONTENT = "0"
WAV_NAME = "test.wav"
WAV_CONTENT = "0"
@pytest.fixture
def csv(tmpdir):
    tmpfile = tmpdir.join(CSV_NAME)
    with tmpfile.open("w") as f:
        f.write("\n".join([",".join(map(str, l)) 
                         for l in CSV_CONTENT]))    
    yield str(tmpfile)
    tmpfile.remove()


@pytest.fixture
def json(tmpdir):
    tmpfile = tmpdir.join(JSON_NAME)
    with tmpfile.open("w") as f:
        json_.dump(JSON_CONTENT, f)
    yield str(tmpfile)
    tmpfile.remove()


@pytest.fixture
def txt(tmpdir):
    tmpfile = tmpdir.join(TXT_NAME)
    with tmpfile.open("w") as f:
        f.write(TXT_CONTENT)    
    yield str(tmpfile)
    tmpfile.remove()

@pytest.fixture
def png(tmpdir):
    tmpfile = tmpdir.join(PNG_NAME)
    with tmpfile.open("w") as f:
        f.write(PNG_CONTENT)    
    yield str(tmpfile)
    tmpfile.remove()
@pytest.fixture
def gif(tmpdir):
    tmpfile = tmpdir.join(GIF_NAME)
    with tmpfile.open("w") as f:
        f.write(GIF_CONTENT)
    yield str(tmpfile)
    tmpfile.remove()
    
@pytest.fixture
def wav(tmpdir):
    tmpfile = tmpdir.join(WAV_NAME)
    with tmpfile.open("w") as f:
        f.write(WAV_CONTENT)    
    yield str(tmpfile)
    tmpfile.remove()


