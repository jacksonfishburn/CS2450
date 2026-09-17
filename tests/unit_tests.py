import sys
import os
import unittest
from unittest.mock import patch
import io

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from classes.Operators import Arithmetic, Control, InOut, LoadStore

class TestArithmetic(unittest.TestCase):
    def setUp(self):
        self.arithmetic = Arithmetic()
        self.memory = ["+0000"] * 100
        self.memory[10] = "+0015"
        self.memory[11] = "-0005"
        self.command = "+3010" # Command targeting memory location 10

    # --- ADD ---
    def test_add_success(self):
        # Test adding a positive memory value to a positive accumulator
        result = self.arithmetic.add(self.command, self.memory, "+0010")
        self.assertEqual(result, "+0025")
        
    def test_add_invalid_memory(self):
        # Test failure when trying to add a non-integer string
        self.memory[10] = "+ABCD"
        with self.assertRaises(ValueError):
            self.arithmetic.add(self.command, self.memory, "+0010")

    # --- SUBTRACT ---
    def test_subtract_success(self):
        # Test subtracting memory from accumulator (10 - 15)
        result = self.arithmetic.subtract(self.command, self.memory, "+0010")
        self.assertEqual(result, "-0005")

    def test_subtract_invalid_accumulator(self):
        # Test failure condition with invalid accumulator data
        with self.assertRaises(ValueError):
            self.arithmetic.subtract(self.command, self.memory, "invalid_data")

    # --- MULTIPLY ---
    def test_multiply_success(self):
        # Test multiplying memory and accumulator (15 * 10)
        result = self.arithmetic.multiply(self.command, self.memory, "+0010")
        self.assertEqual(result, "+0150")

    def test_multiply_overflow(self):
        self.memory[10] = "+9999"
        result = self.arithmetic.multiply(self.command, self.memory, "+0010")


    # --- DIVIDE ---
    def test_divide_success(self):
        # Test dividing accumulator by memory (30 / 15)
        result = self.arithmetic.divide(self.command, self.memory, "+0030")
        self.assertEqual(result, "+0002")

    def test_divide_by_zero(self):
        # Test failure condition: Divide by zero
        self.memory[10] = "+0000"
        with self.assertRaises(ZeroDivisionError):
            self.arithmetic.divide(self.command, self.memory, "+0030")


class TestControl(unittest.TestCase):
    def setUp(self):
        self.control = Control()

    # --- BRANCH ---
    def test_branch_success(self):
        self.assertEqual(self.control.Branch("+4050"), 50)

    def test_branch_out_of_bounds(self):
        # Test failure: Branching to a location outside 0-99
        with self.assertRaises(IndexError):
            self.control.Branch("+40999") 

    # --- BRANCHNEG ---
    def test_branch_neg_success(self):
        # Should branch if accumulator is negative
        self.assertEqual(self.control.BranchNeg("-4150", 10), 50)
        
    def test_branch_neg_failure(self):
        # Should return 'fail' (previous memory) if accumulator is positive
        self.assertEqual(self.control.BranchNeg("+4150", 10), 10)

    # --- BRANCHZERO ---
    def test_branch_zero_success(self):
        # Should branch if accumulator is exactly zero
        self.assertEqual(self.control.BranchZero("+4250", 0, 10), 50)
        
    def test_branch_zero_failure(self):
        # Should NOT branch if accumulator is non-zero
        self.assertEqual(self.control.BranchZero("+4250", 5, 10), 10)


class TestLoadStore(unittest.TestCase):
    def setUp(self):
        self.load_store = LoadStore()
        self.memory = ["+0000"] * 100
        self.memory[25] = "+1234"

    # --- LOAD ---
    def test_load_success(self):
        command = "+2025"
        result = self.load_store.load(command, self.memory)
        self.assertEqual(result, "+1234")

    def test_load_out_of_bounds(self):
        # Test failure: trying to load from memory address > 99
        command = "+20105"
        with self.assertRaises(IndexError):
            self.load_store.load(command, self.memory)

    # --- STORE ---
    def test_store_success(self):
        command = "+2130"
        accumulator = "+9999"
        updated_memory = self.load_store.store(command, self.memory, accumulator)
        self.assertEqual(updated_memory[30], "+9999")

    def test_store_invalid_format(self):
        # Test failure: storing a value that isn't a properly formatted BasicML word
        command = "+2130"
        accumulator = "invalid_word"
        with self.assertRaises(ValueError):
            self.load_store.store(command, self.memory, accumulator)


class TestInOut(unittest.TestCase):
    def setUp(self):
        self.in_out = InOut()
        self.memory = ["+0000"] * 100
        self.memory[15] = "+5678"

    # --- READ ---
    @patch('builtins.input', return_value="+9876")
    def test_read_input_valid(self, mock_input):
        command = "+1015"
        loc, data = self.in_out.read_input(command)
        self.assertEqual(loc, 15)
        self.assertEqual(data, "+9876")

    @patch('builtins.input', side_effect=["ABCDEFG", "+9999"])
    def test_read_input_invalid_recovery(self, mock_input):
        # Tests an incorrect input followed by a correct one
        command = "+1015"
        
        loc, data = self.in_out.read_input(command)
        
        self.assertEqual(loc, 15)
        self.assertEqual(data, "+9999")
        
        # Optional: Verify that input() was actually called twice
        self.assertEqual(mock_input.call_count, 2)

    # --- WRITE ---
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_write_output_success(self, mock_stdout):
        command = "+1115"
        self.in_out.write_output(self.memory, command)
        self.assertIn("+5678", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_write_output_out_of_bounds(self, mock_stdout):
        # Test failure: attempt to write from a memory location that doesn't exist
        command = "+11150"
        with self.assertRaises(IndexError):
            self.in_out.write_output(self.memory, command)

if __name__ == '__main__':
    unittest.main()