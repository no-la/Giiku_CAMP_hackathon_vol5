"""pathの操作やfileの読み取り、書き込みなど"""
from pathlib import Path
import glob
import mimetypes
import csv
import json

import settings

# ---------------------------------------------
# ファイル全般の操作
# ---------------------------------------------
def is_path(file_path: str) -> bool:
    """file_pathが存在するファイルか調べる"""
    if not isinstance(file_path, str):
        return False
    return Path(file_path).exists()

def get_extension(file_path: str) -> str:
    """ファイルの拡張子を返す"""
    return Path(file_path).suffix

def get_name(file_path: str) -> str:
    """ファイルの名前(拡張子を除いた部分)を返す"""
    return Path(file_path).stem

def get_MIMEtype(file_path: str) -> str:
    """ファイルのMIMEタイプを返す"""
    return mimetypes.guess_type(file_path)[0]

def get_abspath_of_directory(file_path: str) -> str:
    """ファイルが属するディレクトリの絶対パスを返す
    
    Args:
        file_path: 対象ファイルのパス
        
    Examples:
        >>> get_abs_path_of_parent_directory(__file__)
        'この関数を呼び出したpythonファイルが属するディレクトリのパス'
    """
    return str(Path(file_path).resolve().parent)


def get_all_files_of_directory(dir_path: str) -> list[str]:
    """dir_path内の全てのファイルのパスのlistを返す
    
    Args:
        dir_path: 対象のディレクトリの絶対パス
    
    Examples:
        >>> get_all_files_of_directory('')
    """
    if dir_path[-2:]!="\\":
        dir_path += "\\"
    return glob.glob(f"{dir_path}*")

def read_file(file_path: str):
    """open(file_path, "r")の代わりに呼ぶ"""
    with open(file_path, "r", encoding=settings.ENCODING) as f:
        return f.read()

def write_file(file_path: str, content: str, mode: str = "w"):
    """file_pathにcontentを書き込む
    
    Parameters
    ----------
    file_path : str
        書き込みたいファイルの絶対パス
    content : str
        書き込みたい内容
    mode : str, default "a"
        openのoption
        w - 上書き
        a - 追加書き込み
    """
    if not mode in ("w", "a"):
        raise ValueError(f"対応しているmodeは'w'と'a'のみです mode={mode}")

    with open(file_path, mode, encoding=settings.ENCODING,
              newline="") as f:
        f.write(content)


# ---------------------------------------------
# csvファイルの操作
# ---------------------------------------------
def count_rows_of_csvfile(file_path: str):
    if get_extension(file_path)!=".csv":
        raise ValueError("csvファイルのパスを渡してください")
    c = 0
    with open(file_path, "r", encoding=settings.ENCODING) as f:
        r = csv.reader(f)
        for _ in r:
            c += 1
    return c

def identifier_exists_in_csvfile(file_path: str, identifier: str):
    """identifierがcsvファイルの0行目に存在するか調べる"""
    if get_extension(file_path)!=".csv":
        raise ValueError(f"csvファイルを渡してください file_path={file_path}")
    with open(file_path, "r", encoding=settings.ENCODING) as f:
        r = csv.reader(f)
        for l in r:
            if l[0]==identifier:
                return True
    return False
    

def get_csvline_from_csvfile(file_path: str, *,
                             row: int|None = None,
                             identifier: str|None = None):
    """csvファイルの指定した行をlistにして返す
    
    file_pathのrow行目 or 一列目がidentifierに一致する行をlistにして返す
    
    Parameters
    ----------
    file_path : str
        csvファイルのパス
    row : int or None, default None
        取得したい行(0-indexed)
    identifier : str or None, default None
        取得したい行の識別子(第0列の要素)
    Returns
    -------
    csvline : list[str]
        file_pathのrow行目をlistに変換したもの
    """
    if get_extension(file_path)!=".csv":
        raise ValueError("csvファイルのパスを渡してください")
    c = 0
    with open(file_path, "r", encoding=settings.ENCODING) as f:
        r = csv.reader(f)
        for l in r:
            if c==row or l[0]==identifier:
                return l
            c += 1
    raise IndexError("該当する行がありません file_path={0} row={1} identifier={2}".format(
        file_path, row, identifier
    ))

def get_list_from_csvfile(file_path: str) -> list[str]:
    """csvファイルをlistにして返す"""
    if get_extension(file_path)!=".csv":
        raise ValueError(f"csvファイルを渡してください file_path = {file_path}")
    ans = []
    with open(file_path, encoding=settings.ENCODING) as f:
        for l in csv.reader(f):
            ans.append(l)
    return ans


def write_csvline(file_path: str, csvline: list, mode="a"):
    """file_pathにcontentを書き込む
    
    Parameters
    ----------
    file_path : str
        書き込みたいファイルの絶対パス
    content : str
        書き込みたい内容
    mode : str, default "a"
        openのoption
        w - 上書き
        a - 追加書き込み
    """
    if get_extension(file_path) != ".csv":
        raise ValueError(f"csvファイルのパスを渡してください file_path={file_path}")
    elif not isinstance(csvline, list):
        raise TypeError(f"csvlineにはlistを渡してください csvline={csvline}")
    elif not mode in ("w", "a"):
        raise ValueError(f"対応しているmodeは'w'と'a'のみです mode={mode}")

    with open(file_path, mode, encoding=settings.ENCODING,
              newline="") as f:
        w = csv.writer(f)
        if mode=="a": # 1回改行する
            w.writerow([])
        w.writerow(csvline)


def write_csvfile(file_path: str, csvlines: list):
    """file_pathにcsvlinesを書き込む
    
    Parameters
    ----------
    file_path : str
        書き込みたいファイルの絶対パス
    csvlines : list of list of str
        書き込みたい内容
    """
    if get_extension(file_path) != ".csv":
        raise ValueError(f"csvファイルのパスを渡してください file_path={file_path}")
    elif not isinstance(csvlines, list):
        raise TypeError(f"csvlineにはlistを渡してください csvline={csvlines}")

    with open(file_path, "w", encoding=settings.ENCODING,
              newline="") as f:
        w = csv.writer(f)
        w.writerows(csvlines)



# ---------------------------------------------
# jsonファイルの操作
# ---------------------------------------------
def get_dict_from_jsonfile(file_path: str) -> dict:
    """jsonファイルからdictを得る
    
    Parameters
    ----------
    file_path : str
        dictを取得したいjsonファイルのパス
    """
    if get_extension(file_path)!=".json":
        raise ValueError(f"jsonファイルのパスを渡してください file_path={file_path}")

    with open(file_path, mode="r", encoding=settings.ENCODING) as f:
        return json.load(f)

def write_jsonfile(file_path: str, json_dict: dict):
    """file_pathにjson_dictを書き込む
    
    Parameters
    ----------
    file_path : str
        書き込みたいjsonファイルのパス
    json_dict : dict
        書き込みたいdict
    """
    if get_extension(file_path)!=".json":
        raise ValueError(f"jsonファイルのパスを渡してください file_path={file_path}")
    
    with open(file_path, mode="w", encoding=settings.ENCODING) as f:
        json.dump(json_dict, f, indent=4, ensure_ascii=False)



# ---------------------------------------------
# tempディレクトリの操作
# ---------------------------------------------
def get_new_tempfile_num(extension: str):
    if extension[0]!=".":
        raise ValueError(f"extentionは'.'から始めてください extension={extension}")
    return sorted([
        p for p in list(set([i for i in range(settings.TEMP_POOL_LIMIT)])
             - set(map(lambda x: int(get_name(x)) if get_extension(x)==extension else None,
                       get_all_files_of_directory(settings.TEMP_DIR_PATH)))
             )
        ])[0]

def get_tempfile_path(num: int|str, extension: str):
    """tempファイルのパスを返す
    
    Parameters
    ----------
    num : int or str
        作るファイルの名前
    extension : str
        作るファイルの拡張子
    """
    if extension[0]!=".":
        raise ValueError(f"extentionは'.'から始めてください extension={extension}")
    return f"{settings.TEMP_DIR_PATH}{num}{extension}"

def write_temp_csvfile(csvlines: list) -> str:
    """一時csvファイルに書き込む
    
    Parameters
    ----------
    csvlines : list of list of str
        書き込む内容
        
    Returns
    -------
    file_path : str
        書き込んだファイルのパス
    """
    n = get_new_tempfile_num(".csv")
    file_path = get_tempfile_path(n, ".csv")
    write_csvfile(file_path=file_path,
                  csvlines=csvlines)
    delete_tempfile(get_tempfile_path((n+1)%settings.TEMP_POOL_LIMIT, ".csv"))
    return file_path

def delete_oldest_tempfile(extension: str):
    delete_tempfile(get_tempfile_path(
        (get_new_tempfile_num(extension)+1)%settings.TEMP_POOL_LIMIT,
        extension))

def delete_tempfile(file_path: str):
    """file_pathを削除する"""
    if get_abspath_of_directory(file_path)!=settings.TEMP_DIR_PATH[:-1]:
        raise ValueError("tempディレクトリ以外のファイルが渡されました")
    
    Path(file_path).unlink(missing_ok=True)

