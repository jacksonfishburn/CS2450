import sys
import os
import unittest
from unittest.mock import patch
import io

#Parent directory to Python's path so it can find the 'classes' folder
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from classes.signed_int import SignedInt
from classes.memory import Memory
from classes.uvsim import UVSim, NeedValue, GotValue, Halted


class Test4SignedIntAndMemory100(unittest.TestCase):
    # --- WORD VALIDATION & MEMORY LOADING ---
    def test_4SignedInt_valid_creation(self):
        word = SignedInt("+1234", size=4)
        self.assertEqual(str(word), "+1234")
        self.assertEqual(word.get_command(), 12)
        self.assertEqual(word.get_pointer(), 34)
    
    def test_4SignedInt_invalid_input(self):
        with self.assertRaises(ValueError):
            SignedInt("+ABCD", size=4)
        with self.assertRaises(ValueError):
            SignedInt("")

    def test_memory_load_too_long(self):
        with self.assertRaises(ValueError):
            Memory(["+0000"] * 101, size=100)

    def test_memory_out_of_bounds(self):
        mem = Memory([], size=100)
        with self.assertRaises(IndexError):
            mem.at(100)
        with self.assertRaises(IndexError):
            mem.set(-1, "+0000")

class Test6SignedIntAndMemory250(unittest.TestCase):
    # --- WORD VALIDATION & MEMORY LOADING ---
    def test_4SignedInt_valid_creation(self):
        word = SignedInt("+123231", size=6)
        self.assertEqual(str(word), "+123231")
        self.assertEqual(word.get_command(), 123)
        self.assertEqual(word.get_pointer(), 231)
    
    def test_4SignedInt_invalid_input(self):
        with self.assertRaises(ValueError):
            SignedInt("+ABCDEF", size=6)
        with self.assertRaises(ValueError):
            SignedInt("")

    def test_memory_load_too_long(self):
        with self.assertRaises(ValueError):
            Memory(["+0000"] * 251, size=250)

    def test_memory_out_of_bounds(self):
        mem = Memory([], size=250)
        with self.assertRaises(IndexError):
            mem.at(250)
        with self.assertRaises(IndexError):
            mem.set(-1, "+000000")


class TestArithmetic100(unittest.TestCase):
    def setUp(self):
        self.cpu = UVSim(memory_size=100)
        # Location 00: Command | Location 10: +0015 | Location 11: -0005
        self.cpu.set_memory_at(10, "+0015")
        self.cpu.set_memory_at(11, "-0005")

    # --- ADD (code 30) ---
    def test_add_success(self):
        self.cpu.set_memory_at(0, "+3010")
        self.cpu._acu.set_word("+0010")
        self.cpu.step()
        self.assertEqual(str(self.cpu.get_accumulator()), "+0025")

    def test_add_invalid_memory(self):
        with self.assertRaises(ValueError):
            self.cpu.set_memory_at(10, "+ABCD")

    # --- SUBTRACT (code 31) ---
    def test_subtract_success(self):
        self.cpu.set_memory_at(0, "+3110")
        self.cpu._acu.set_word("+0010")
        self.cpu.step()
        self.assertEqual(str(self.cpu.get_accumulator()), "-0005")

    def test_subtract_invalid_accumulator(self):
        # Accumulator raises TypeError when given an unsupported data type (e.g., list)
        with self.assertRaises(TypeError):
            self.cpu._acu.set_word(["invalid_type"])

    # --- MULTIPLY (code 33) ---
    def test_multiply_success(self):
        self.cpu.set_memory_at(0, "+3310")
        self.cpu._acu.set_word("+0010")
        self.cpu.step()
        self.assertEqual(str(self.cpu.get_accumulator()), "+0150")

    def test_multiply_overflow(self):
        self.cpu.set_memory_at(0, "+3310")
        self.cpu.set_memory_at(10, "+9999")
        self.cpu._acu.set_word("+0010")
        self.cpu.step()
        # 9999 * 10 = 99990 -> 99990 % 10000 = 9990
        self.assertEqual(str(self.cpu.get_accumulator()), "9990")

    # --- DIVIDE (code 32) ---
    def test_divide_success(self):
        self.cpu.set_memory_at(0, "+3210")
        self.cpu._acu.set_word("+0030")
        self.cpu.step()
        self.assertEqual(str(self.cpu.get_accumulator()), "+0002")

    def test_divide_by_zero(self):
        self.cpu.set_memory_at(0, "+3210")
        self.cpu.set_memory_at(10, "+0000")
        self.cpu._acu.set_word("+0030")
        with self.assertRaises(ZeroDivisionError):
            self.cpu.step()

class TestArithmetic250(unittest.TestCase):
    def setUp(self):
        self.cpu = UVSim(memory_size=250)
        # Location 00: Command | Location 10: +0015 | Location 11: -0005
        self.cpu.set_memory_at(10, "+000015")
        self.cpu.set_memory_at(11, "-000005")

    # --- ADD (code 030) ---
    def test_add_success(self):
        self.cpu.set_memory_at(0, "+030010")
        self.cpu._acu.set_word("+000010")
        self.cpu.step()
        self.assertEqual(str(self.cpu.get_accumulator()), "+000025")

    def test_add_invalid_memory(self):
        with self.assertRaises(ValueError):
            self.cpu.set_memory_at(10, "+ABCDEF")

    # --- SUBTRACT (code 031) ---
    def test_subtract_success(self):
        self.cpu.set_memory_at(0, "+031010")
        self.cpu._acu.set_word("+000010")
        self.cpu.step()
        self.assertEqual(str(self.cpu.get_accumulator()), "-000005")

    def test_subtract_invalid_accumulator(self):
        # Accumulator raises TypeError when given an unsupported data type (e.g., list)
        with self.assertRaises(TypeError):
            self.cpu._acu.set_word(["invalid_type"])

    # --- MULTIPLY (code 033) ---
    def test_multiply_success(self):
        self.cpu.set_memory_at(0, "+033010")
        self.cpu._acu.set_word("+000010")
        self.cpu.step()
        self.assertEqual(str(self.cpu.get_accumulator()), "+000150")

    def test_multiply_overflow(self):
        self.cpu.set_memory_at(0, "+033010")
        self.cpu.set_memory_at(10, "+999999")
        self.cpu._acu.set_word("+000010")
        self.cpu.step()
        # 999999 * 10 = 9999990 -> 99990 % 10000 = 999990
        self.assertEqual(str(self.cpu.get_accumulator()), "999990")

    # --- DIVIDE (code 032) ---
    def test_divide_success(self):
        self.cpu.set_memory_at(0, "+032010")
        self.cpu._acu.set_word("+000030")
        self.cpu.step()
        self.assertEqual(str(self.cpu.get_accumulator()), "+000002")

    def test_divide_by_zero(self):
        self.cpu.set_memory_at(0, "+032010")
        self.cpu.set_memory_at(10, "+000000")
        self.cpu._acu.set_word("+000030")
        with self.assertRaises(ZeroDivisionError):
            self.cpu.step()


class TestControl100(unittest.TestCase):
    def setUp(self):
        self.cpu = UVSim(memory_size=100)

    # --- BRANCH (code 40) ---
    def test_branch_success_size100(self):
        self.cpu.set_memory_at(0, "+4050")
        self.cpu.step()
        # sets pointer to location - 1 (49) so the next step() increments it to 50
        self.assertEqual(self.cpu.get_pointer(), 49)

    def test_branch_out_of_bounds_size100(self):
        with self.assertRaises(IndexError):
            self.cpu._BRA(105)

    # --- BRANCHNEG (code 41) ---
    def test_branch_neg_success100(self):
        self.cpu.set_memory_at(0, "+4150")
        self.cpu._acu.set_word("-0001")
        self.cpu.step()
        self.assertEqual(self.cpu.get_pointer(), 49)

    def test_branch_neg_failure100(self):
        self.cpu.set_memory_at(0, "+4150")
        self.cpu._acu.set_word("+0001")
        self.cpu.step()
        # Does not branch; stays at instruction 0
        self.assertEqual(self.cpu.get_pointer(), 0)

    # --- BRANCHZERO (code 42) ---
    def test_branch_zero_success100(self):
        self.cpu.set_memory_at(0, "+4250")
        self.cpu._acu.set_word("+0000")
        self.cpu.step()
        self.assertEqual(self.cpu.get_pointer(), 49)

    def test_branch_zero_failure100(self):
        self.cpu.set_memory_at(0, "+4250")
        self.cpu._acu.set_word("+0001")
        self.cpu.step()
        self.assertEqual(self.cpu.get_pointer(), 0)

    # --- HALT (code 43) ---
    def test_halt100(self):
        self.cpu.set_memory_at(0, "+4300")
        with self.assertRaises(Halted):
            self.cpu.step()

class TestControl250(unittest.TestCase):
    def setUp(self):
        self.cpu = UVSim(memory_size=250)

    # --- BRANCH (code 040) ---
    def test_branch_success_size100(self):
        self.cpu.set_memory_at(0, "+040050")
        self.cpu.step()
        # sets pointer to location - 1 (49) so the next step() increments it to 50
        self.assertEqual(self.cpu.get_pointer(), 49)

    def test_branch_out_of_bounds_size100(self):
        with self.assertRaises(IndexError):
            self.cpu._BRA(255)

    # --- BRANCHNEG (code 041) ---
    def test_branch_neg_success100(self):
        self.cpu.set_memory_at(0, "+041050")
        self.cpu._acu.set_word("-000001")
        self.cpu.step()
        self.assertEqual(self.cpu.get_pointer(), 49)

    def test_branch_neg_failure100(self):
        self.cpu.set_memory_at(0, "+041050")
        self.cpu._acu.set_word("+000001")
        self.cpu.step()
        # Does not branch; stays at instruction 0
        self.assertEqual(self.cpu.get_pointer(), 0)

    # --- BRANCHZERO (code 042) ---
    def test_branch_zero_success100(self):
        self.cpu.set_memory_at(0, "+042050")
        self.cpu._acu.set_word("+000000")
        self.cpu.step()
        self.assertEqual(self.cpu.get_pointer(), 49)

    def test_branch_zero_failure100(self):
        self.cpu.set_memory_at(0, "+042050")
        self.cpu._acu.set_word("+000001")
        self.cpu.step()
        self.assertEqual(self.cpu.get_pointer(), 0)

    # --- HALT (code 043) ---
    def test_halt100(self):
        self.cpu.set_memory_at(0, "+043000")
        with self.assertRaises(Halted):
            self.cpu.step()


class TestLoadStore100(unittest.TestCase):
    def setUp(self):
        self.cpu = UVSim(memory_size=100)
        self.cpu.set_memory_at(25, "+1234")

    # --- LOAD (code 20) ---
    def test_load_success(self):
        self.cpu.set_memory_at(0, "+2025")
        self.cpu.step()
        self.assertEqual(str(self.cpu.get_accumulator()), "+1234")

    def test_load_out_of_bounds(self):
        with self.assertRaises(IndexError):
            self.cpu._LOD(105)

    # --- STORE (code 21) ---
    def test_store_success(self):
        self.cpu.set_memory_at(0, "+2130")
        self.cpu._acu.set_word("+9999")
        self.cpu.step()
        self.assertEqual(str(self.cpu.get_memory()[30]), "+9999")

    def test_store_invalid_format(self):
        with self.assertRaises(ValueError):
            self.cpu.set_memory_at(30, "invalid_word")

class TestLoadStore250(unittest.TestCase):
    def setUp(self):
        self.cpu = UVSim(memory_size=250)
        self.cpu.set_memory_at(25, "+123456")

    # --- LOAD (code 020) ---
    def test_load_success(self):
        self.cpu.set_memory_at(0, "+020025")
        self.cpu.step()
        self.assertEqual(str(self.cpu.get_accumulator()), "+123456")

    def test_load_out_of_bounds(self):
        with self.assertRaises(IndexError):
            self.cpu._LOD(255)

    # --- STORE (code 021) ---
    def test_store_success(self):
        self.cpu.set_memory_at(0, "+021030")
        self.cpu._acu.set_word("+999999")
        self.cpu.step()
        self.assertEqual(str(self.cpu.get_memory()[30]), "+999999")

    def test_store_invalid_format(self):
        with self.assertRaises(ValueError):
            self.cpu.set_memory_at(30, "invalid_word")


class TestInOut100(unittest.TestCase):
    def setUp(self):
        self.cpu = UVSim(memory_size=100)
        self.cpu.set_memory_at(15, "+5678")

    # --- READ (code 10) ---
    def test_read_raises_need_value(self):
        self.cpu.set_memory_at(0, "+1015")
        with self.assertRaises(NeedValue) as context:
            self.cpu.step()
        self.assertEqual(context.exception.location, 15)

    @patch('builtins.input', return_value="+9876")
    def test_read_input_console_run(self, mock_input):
        self.cpu.set_memory_at(0, "+1015")
        self.cpu.set_memory_at(1, "+4300")
        self.cpu.run()
        self.assertEqual(str(self.cpu.get_memory()[15]), "+9876")

    # --- WRITE (code 11) ---
    def test_write_raises_got_value(self):
        self.cpu.set_memory_at(0, "+1115")
        with self.assertRaises(GotValue) as context:
            self.cpu.step()
        self.assertEqual(str(context.exception.value), "+5678")

    def test_write_output_out_of_bounds(self):
        with self.assertRaises(IndexError):
            self.cpu._WRI(150)

class TestInOut250(unittest.TestCase):
    def setUp(self):
        self.cpu = UVSim(memory_size=250)
        self.cpu.set_memory_at(15, "+567890")

    # --- READ (code 010) ---
    def test_read_raises_need_value(self):
        self.cpu.set_memory_at(0, "+010015")
        with self.assertRaises(NeedValue) as context:
            self.cpu.step()
        self.assertEqual(context.exception.location, 15)

    @patch('builtins.input', return_value="+009876")
    def test_read_input_console_run(self, mock_input):
        self.cpu.set_memory_at(0, "+010015")
        self.cpu.set_memory_at(1, "+043000")
        self.cpu.run()
        self.assertEqual(str(self.cpu.get_memory()[15]), "+009876")

    # --- WRITE (code 011) ---
    def test_write_raises_got_value(self):
        self.cpu.set_memory_at(0, "+011015")
        with self.assertRaises(GotValue) as context:
            self.cpu.step()
        self.assertEqual(str(context.exception.value), "+567890")

    def test_write_output_out_of_bounds(self):
        with self.assertRaises(IndexError):
            self.cpu._WRI(300)


if __name__ == '__main__':
    unittest.main()