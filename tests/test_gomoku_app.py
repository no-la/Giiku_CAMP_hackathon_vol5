import pytest

from .context import settings
from .context import conftest
from .context import gomoku_app
from .context import file_utils


def test_gomoku():
    global winner
    g1 = gomoku_app.Gomoku(1)
    g1.put_piece(0, 0)
    assert g1.winner == -1
    
    g2 = gomoku_app.Gomoku(5)
    for i in range(9):
        g2.put_piece(i&1, i//2)
    assert g2.winner == 0
    with pytest.raises(ValueError):
        g2.put_piece(3, 0)
    
    g3 = gomoku_app.Gomoku(20)
    with pytest.raises(IndexError):
        g3.put_piece(-1, 0)
    g3.put_piece(0, 0)
    g3.put_piece(19, 19)
    with pytest.raises(ValueError):
        g3.put_piece(0, 0)
    
    g4 = gomoku_app.Gomoku(5)
    for i in range(4):
        g4.board[i][i] = 0
    g4.put_piece(4, 4)
    assert g4.winner == 0
    
    g5 = gomoku_app.Gomoku(5)
    for i in range(4):
        g5.board[i-2][i] = 0
    # print(g5)
    g5.put_piece(2, 4)
    assert g5.winner == None