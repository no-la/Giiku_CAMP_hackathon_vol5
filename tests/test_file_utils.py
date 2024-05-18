import pytest
import csv

from .context import settings
from .context import conftest
from .context import file_utils


def test_is_path(txt):
    assert file_utils.is_path(txt) == True
    assert file_utils.is_path("123") == False

# def test_join_path(tmpdir, txt):
#     assert file_utils.join_path(tmpdir, txt) == 

def test_get_extension(csv, json, txt, png, gif, wav):
    assert file_utils.get_extension(csv) == ".csv"
    assert file_utils.get_extension(json) == ".json"
    assert file_utils.get_extension(txt) == ".txt"
    assert file_utils.get_extension(png) == ".png"
    assert file_utils.get_extension(gif) == ".gif"
    assert file_utils.get_extension(wav) == ".wav"


def test_get_MIMEtype_with_csv(csv, json, txt, png, gif, wav):
    assert file_utils.get_MIMEtype(csv) == "application/vnd.ms-excel"
    assert file_utils.get_MIMEtype(json) == "application/json"
    assert file_utils.get_MIMEtype(txt) == "text/plain"
    assert file_utils.get_MIMEtype(png) == "image/png"
    assert file_utils.get_MIMEtype(gif) == "image/gif"
    assert file_utils.get_MIMEtype(wav) == "audio/wav"


def test_get_abspath_of_directory(tmpdir, txt):
    assert file_utils.get_abspath_of_directory(txt) == str(tmpdir)

def test_get_all_files_of_directory(tmpdir, csv, json,
                                    txt, png, gif, wav):
    assert set(
        file_utils.get_all_files_of_directory(str(tmpdir))
        ) == set([
        f"{str(tmpdir)}\\{conftest.CSV_NAME}",
        f"{str(tmpdir)}\\{conftest.JSON_NAME}",
        f"{str(tmpdir)}\\{conftest.TXT_NAME}",
        f"{str(tmpdir)}\\{conftest.PNG_NAME}",
        f"{str(tmpdir)}\\{conftest.GIF_NAME}",
        f"{str(tmpdir)}\\{conftest.WAV_NAME}",
    ])


def test_get_list_from_csvfile(csv, txt):
    assert file_utils.get_list_from_csvfile(csv) == conftest.CSV_CONTENT
    with pytest.raises(ValueError):
        file_utils.get_list_from_csvfile(txt)

def test_get_csvline_from_csvfile(csv, txt):
    assert file_utils.get_csvline_from_csvfile(csv, row=0) == conftest.CSV_CONTENT[0]
    assert file_utils.get_csvline_from_csvfile(csv, row=1) == conftest.CSV_CONTENT[1]
    with pytest.raises(ValueError):
        file_utils.get_csvline_from_csvfile(txt, row=0)
    with pytest.raises(IndexError):
        file_utils.get_csvline_from_csvfile(csv, row=-1)
    
    # test for by identifier
    assert file_utils.get_csvline_from_csvfile(
        csv, identifier=conftest.CSV_CONTENT[0][0]) == conftest.CSV_CONTENT[0]
    assert file_utils.get_csvline_from_csvfile(
        csv, identifier=conftest.CSV_CONTENT[1][0]) == conftest.CSV_CONTENT[1]
    with pytest.raises(IndexError):
        file_utils.get_csvline_from_csvfile(csv, identifier="aaa")

def test_read_file(txt, csv):
    assert file_utils.read_file(txt) == conftest.TXT_CONTENT
    # assert file_utils.read_file(
    #     csv) == string_utils.get_csvtext_from_list(conftest.CSV_CONTENT)

    with pytest.raises(FileNotFoundError):
        file_utils.read_file("abcdefg")

def test_count_rows_of_csvfilee(txt, csv):
    with pytest.raises(ValueError):
        file_utils.count_rows_of_csvfile(txt)
    assert file_utils.count_rows_of_csvfile(
        csv) == len(conftest.CSV_CONTENT)

def test_write_csvline(csv, tmpdir):
    file_utils.write_csvline(csv, ["7", "8", "9"])
    assert file_utils.get_list_from_csvfile(
        csv) == conftest.CSV_CONTENT + [["7", "8", "9"]]
    
    tmpfile = tmpdir.join("test_write_csvline.csv")
    file_utils.write_csvline(str(tmpfile), [1, 2, 3], "w")
    assert file_utils.get_list_from_csvfile(
        str(tmpfile)) == [["1", "2", "3"]]
    tmpfile.remove()
    
    with pytest.raises(ValueError):
        file_utils.write_csvline("aaa", ["a"])
    with pytest.raises(TypeError):
        file_utils.write_csvline(csv, "aaa")
    with pytest.raises(ValueError):
        file_utils.write_csvline(csv, [0, 1, 2], "r")


def test_identifier_exists_in_csvfile(csv, txt):
    with pytest.raises(ValueError):
        file_utils.identifier_exists_in_csvfile(txt, conftest.TXT_CONTENT)
    assert file_utils.identifier_exists_in_csvfile(csv, "1") == True
    assert file_utils.identifier_exists_in_csvfile(csv, "4") == True
    assert file_utils.identifier_exists_in_csvfile(csv, "5") == False
    assert file_utils.identifier_exists_in_csvfile(csv, "") == False


def test_get_name(txt, csv):
    assert file_utils.get_name(txt) == conftest.TXT_NAME.split(".")[0]
    assert file_utils.get_name(csv) == conftest.CSV_NAME.split(".")[0]


def test_write_csvfile(csv):
    file_utils.write_csvfile(csv, [["1", "2"], ["3", "4"]])
    assert file_utils.get_list_from_csvfile(csv) == [["1", "2"], ["3", "4"]]

def test_get_dict_from_jsonfile(txt, json):
    with pytest.raises(ValueError):
        file_utils.get_dict_from_jsonfile(txt)
    case1 = file_utils.get_dict_from_jsonfile(json)
    assert case1 == conftest.JSON_CONTENT

def test_write_jsonfile(json, txt):
    d = {
        "aaa":[1, 2, 3],
        "bbb":"0123",
        "ccc":100
    }
    file_utils.write_jsonfile(json, d)
    assert file_utils.get_dict_from_jsonfile(json) == d
    with pytest.raises(ValueError):
        file_utils.write_jsonfile(txt, d)
