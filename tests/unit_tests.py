import sys
import os
import unittest
from unittest.mock import patch
import io

#Parent directory to Python's path so it can find the 'classes' folder
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from classes.signed_4_digit_int import S4DI
from classes.memory import Memory
from classes.uvsim import UVSim, NeedValue, GotValue, Halted


class TestS4DIAndMemory(unittest.TestCase):
    # --- WORD VALIDATION & MEMORY LOADING ---
    def test_s4di_valid_creation(self):
        word = S4DI("+1234")
        self.assertEqual(str(word), "+1234")
        self.assertEqual(word.get_command(), 12)
        self.assertEqual(word.get_pointer(), 34)

    def test_s4di_invalid_input(self):
        with self.assertRaises(ValueError):
            S4DI("+ABCD")
        with self.assertRaises(ValueError):
            S4DI("")

    def test_memory_load_too_long(self):
        with self.assertRaises(ValueError):
            Memory(["+0000"] * 101)

    def test_memory_out_of_bounds(self):
        mem = Memory([])
        with self.assertRaises(IndexError):
            mem.at(100)
        with self.assertRaises(IndexError):
            mem.set(-1, "+0000")


class TestArithmetic(unittest.TestCase):
    def setUp(self):
        self.cpu = UVSim()
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


class TestControl(unittest.TestCase):
    def setUp(self):
        self.cpu = UVSim()

    # --- BRANCH (code 40) ---
    def test_branch_success(self):
        self.cpu.set_memory_at(0, "+4050")
        self.cpu.step()
        # sets pointer to location - 1 (49) so the next step() increments it to 50
        self.assertEqual(self.cpu.get_pointer(), 49)

    def test_branch_out_of_bounds(self):
        self.cpu._BRA(105)
        with self.assertRaises(IndexError):
            self.cpu.step()

    # --- BRANCHNEG (code 41) ---
    def test_branch_neg_success(self):
        self.cpu.set_memory_at(0, "+4150")
        self.cpu._acu.set_word("-0001")
        self.cpu.step()
        self.assertEqual(self.cpu.get_pointer(), 49)

    def test_branch_neg_failure(self):
        self.cpu.set_memory_at(0, "+4150")
        self.cpu._acu.set_word("+0001")
        self.cpu.step()
        # Does not branch; stays at instruction 0
        self.assertEqual(self.cpu.get_pointer(), 0)

    # --- BRANCHZERO (code 42) ---
    def test_branch_zero_success(self):
        self.cpu.set_memory_at(0, "+4250")
        self.cpu._acu.set_word("+0000")
        self.cpu.step()
        self.assertEqual(self.cpu.get_pointer(), 49)

    def test_branch_zero_failure(self):
        self.cpu.set_memory_at(0, "+4250")
        self.cpu._acu.set_word("+0001")
        self.cpu.step()
        self.assertEqual(self.cpu.get_pointer(), 0)

    # --- HALT (code 43) ---
    def test_halt(self):
        self.cpu.set_memory_at(0, "+4300")
        with self.assertRaises(Halted):
            self.cpu.step()


class TestLoadStore(unittest.TestCase):
    def setUp(self):
        self.cpu = UVSim()
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


class TestInOut(unittest.TestCase):
    def setUp(self):
        self.cpu = UVSim()
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


if __name__ == '__main__':
    unittest.main()