import sys
sys.path.append("..")
from src.datacell import DataCell

def test_get_bit():
    datacell = DataCell()
    for i in range(16):
        assert(datacell.get_bit(i) == 0)

    datacell.set_int(-1)
    for i in range(16):
        assert(datacell.get_bit(i) == 1)

    datacell.set_int(-32768)
    for i in range(15):
        assert(datacell.get_bit(i) == 0)
    assert(datacell.get_bit(15) == 1)

    datacell.set_int(32767)
    for i in range(15):
        assert(datacell.get_bit(i) == 1)
    assert(datacell.get_bit(15) == 0)


def test_overflow():
    datacell = DataCell()
    datacell.set_int(32768)
    assert(datacell.get_int() == -32768)

    datacell.set_int(-32768)
    assert(datacell.get_int() == -32768)

    datacell.set_int(65536)
    assert(datacell.get_int() == 0)

    datacell.set_int(65535)
    assert(datacell.get_int() == -1)

    datacell.set_int(-65536)
    assert(datacell.get_int() == 0)

    datacell.set_int(-65537)
    assert(datacell.get_int() == -1)


def test_get_bin():
    datacell = DataCell()

    def bin_to_string(bin):
        return str(bin)[2:]

    datacell.set_int(0)
    assert("1" not in bin_to_string(datacell.get_bin()))

    datacell.set_int(-1)
    assert("0" not in bin_to_string(datacell.get_bin()))

    datacell.set_int(1)
    assert(bin_to_string(datacell.get_bin())[-1] == "1")

def test_size():
    datacell = DataCell()
    assert(datacell.get_size() == 16)

