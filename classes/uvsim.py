from classes.signed_4_digit_int import S4DI
from classes.memory import Memory
from classes.accumulator import Accumulator

class NeedValue(Exception):
    """A solution for requesting a value from the GUI using exceptions. (Probably a bastard use case)
    """
    def __init__(self, message: str, location: int):
        """Initialize instance of NeedValue exception

        Args:
            message (str): Exception Message
            location (int): Location where value is needed
        """
        super().__init__(message)
        self.location = location

class GotValue(Exception):
    """A solution for delivering a value to the GUI using exceptions. (Probably a bastard use case)
    """
    def __init__(self, message: str, value: S4DI):
        """Initialize instance of GotValue exception

        Args:
            message (str): Exception Message
            value (S4DI): Value being delivered
        """
        super().__init__(message)
        self.value = value

class Halted(Exception):
    """A solution for halting the program and informing the GUI. (Probably a bastard use case)
    """
    pass

class UVSim:
    """A class to represent simulate the UVSim CPU

    Attributes:
        _mem: An instance of the Memory class
        _acu: An instance of the Accumulator class
        _pointer: Points to the location in memory currently being processed
    """
    def __init__(self):
        """Initialize an instance of UVSim
        """
        self.load_memory()

    def load_memory(self, load: list = []) -> None:
        """Loads memory

        Args:
            load (list, optional): List of S4DI to be loaded. Defaults to [].
        """
        self._mem = Memory(load)
        self._acu = Accumulator()
        self._pointer = -1

    def set_memory_at(self, location: int, new: S4DI | int | str) -> None:
        """Set the value at a specified location in memory

        Args:
            location (int): The location where the new value is to be set
            new (S4DI | int | str): The new value being set
        """
        self._mem.set(location, new)

    def get_memory(self) -> list[S4DI]:
        """Get the memory as a list

        Returns:
            list[S4DI]: List of S4DI in memory
        """
        return self._mem.get()

    def get_accumulator(self) -> S4DI:
        """Get word in accumulator

        Returns:
            S4DI: Word in accumulator
        """
        return self._acu.get_word()

    def get_pointer(self) -> int:
        """Get the value of the pointer

        Returns:
            int: Pointer
        """
        return self._pointer

    def step(self, debug = False):
        """Step through the memory and execute a single line of code
        """
        self._pointer += 1
        current = self._mem.at(self._pointer)
        match current.get_command():
            case 10:
                self._RED(current.get_pointer())
            case 11:
                self._WRI(current.get_pointer())
            case 20:
                self._LOD(current.get_pointer())
            case 21:
                self._STO(current.get_pointer())
            case 30:
                self._ADD(current.get_pointer())
            case 31:
                self._SUB(current.get_pointer())
            case 32:
                self._DIV(current.get_pointer())
            case 33:
                self._MUL(current.get_pointer())
            case 40:
                self._BRA(current.get_pointer())
            case 41:
                self._BRN(current.get_pointer())
            case 42:
                self._BRZ(current.get_pointer())
            case 43:
                self._HLT()

    def reset(self):
        """"""
        self._pointer = -1
        self._acu = Accumulator()

    def _RED(self, location: int):
        """Read a value from the user into a specified location in memory

        Args:
            location (int): Location in memory to store the value

        Raises:
            NeedValue: Requests value up the call stack
        """
        raise NeedValue("This is the best I could come up with", location)
    def _WRI(self, location: int):
        """Write the value from a specified location in memory to the console

        Args:
            location (int): Location in memory to write to console

        Raises:
            GotValue: Sends the value up the call stack
        """
        raise GotValue("This is the best I could come up with", self._mem.at(location))
    def _LOD(self, location: int):
        """Load a specified word from memory into the accumulator

        Args:
            location (int): The location of the word in memory to load into the accumulator
        """
        self._acu.set_word(self._mem.at(location))
    def _STO(self, location: int):
        """Stores the word in the accumulator to a specified location in memory

        Args:
            location (int): Location in memory to store the word in the accumulator
        """
        self._mem.set(location, self._acu.get_word())
    def _ADD(self, location: int):
        """Adds a specified word in memory to the word in the accumulator. Result stays in the accumulator.

        Args:
            location (int): Location in memory of word to be added to the word in the accumulator
        """
        self._acu.add(self._mem.at(location))
    def _SUB(self, location: int):
        """Subtract a specified word in memory from the word in the accumulator. Result stays in the accumulator.

        Args:
            location (int): Location in memory of word to be subtracted from the word in the accumulator
        """
        self._acu.sub(self._mem.at(location))
    def _DIV(self, location: int):
        """Divide the word in the accumulator by a specified word in memory. Result stays in the accumulator.

        Args:
            location (int): Location of word in memory to divide word in accumulator by.
        """
        self._acu.div(self._mem.at(location))
    def _MUL(self, location: int):
        """Multiply the word in the accumulator by a specified word in memory. Result stays in the accumulator.

        Args:
            location (int): Location of word in memory to multiply word in accumulator by.
        """
        self._acu.mul(self._mem.at(location))
    def _BRA(self, location: int):
        """Move pointer to specified location in memory

        Args:
            location (int): Location in memory to move pointer to.
        """
        self._pointer = location - 1 # because pointer will be incremented before the next command executes
    def _BRN(self, location: int):
        """Move pointer to specified location in memory only if the word in the accumulator is negative

        Args:
            location (int): Location in memory to move pointer to.
        """
        if not self._acu.get_word():
            self._pointer = location - 1 # because pointer will be incremented before the next command executes
    def _BRZ(self, location: int):
        """Move pointer to specified location in memory only if the word in the accumulator is equal to 0

        Args:
            location (int): Location in memory to move pointer to.
        """
        if self._acu.get_word() == 0:
            self._pointer = location - 1
    def _HLT(self):
        """Halt program execution

        Raises:
            Halted: Informs the GUI that the program has been halted
        """
        raise Halted("Program reached HALT command")

    def go_back(self, amount: int = 1):
        """Go back one line. To be used if a line needs to be re-executed due to error. Does NOT restore memory or accumulator.

        Args:
            amount (int, optional): Number of lines to go back. Defaults to 1.
        """
        self._pointer -= amount

    def run(self):
        """Run UVSim in console.
        """
        while True:
            try:
                self.step()
            except NeedValue as e:
                self._mem.set(e.location, input("Please give a valid signed 4-digit integer: "))
            except GotValue as e:
                print(f"Output value: {e.value}")
            except Halted:
                break
