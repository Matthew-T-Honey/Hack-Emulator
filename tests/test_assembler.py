import sys
sys.path.append("..")
from src.assembler import Assembler
from src.emulator import HackEmulator


def test_tmoats():

    emulator = HackEmulator()
    assembler = Assembler()

    f = open("tests/test_files/tmoats.txt","r")
    assembler.assemble(emulator, f)
    f.close()

    emulator.run_program(10000, debug = False)

    assert(emulator.get_value(2) == emulator.get_value(3))
    assert(emulator.get_value(4) == 1)