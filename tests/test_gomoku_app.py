import pytest

from .context import settings
from .context import conftest
from .context import gomoku_app
from .context import file_utils


def test_gomoku():
    global winner
    winner = None
    def set_winner(val):
        global winner
        winner = val
    g1 = gomoku_app.Gomoku(1)
    g1.put_piece(0, 0, set_winner)
    assert winner == -1
    
    winner = None
    g2 = gomoku_app.Gomoku(5)
    for i in range(9):
        # print((i&1, i//2), g2, sep="\n")
        g2.put_piece(i&1, i//2, set_winner)
    print(g2)
    assert winner == 0
    
    winner = None
    g3 = gomoku_app.Gomoku(20)
    with pytest.raises(IndexError):
        g3.put_piece(-1, 0, set_winner)
    g3.put_piece(0, 0, set_winner)
    g3.put_piece(19, 19, set_winner)
    with pytest.raises(ValueError):
        g3.put_piece(0, 0, set_winner)
    