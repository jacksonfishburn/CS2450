
class S4DI:
    """A class used to represent a Signed 4-Digit Integer
    """
    def __init__(self, word: str | int = 0):
        """Initialize signed 4 digit integer

        Args:
            word (str | int, optional): Value of signed 4 digit integer. Defaults to 0.
        """
        # try:
        #     self._word = self._validate(word)
        # except ValueError as e:
        #     print(f'{e}\nDefaulting value to +0000')
        #     self._word = "+0000"

        self._word = self._validate(word) ##was causing issues with the GUI.

    def _validate(self, word: str | int) -> str:
        """Validate word as a Signed 4-Digit Integer

        Args:
            word (str | int): Word to be validated

        Raises:
            ValueError: If word cannot be formatted
            TypeError: If word cannot be formatted

        Returns:
            str: Formatted word
        """
        if type(word) is str:
            word = word.strip()
            if not word:
                raise ValueError("Input cannot be empty.")
            try:
                word = int(word)
            except:
                raise ValueError(f"Invalid word: {word}")
        if type(word) is int:
            if (word < -9999) or (word > 9999):
                return f'{(word % 10000):04d}'
            elif word < 0:
                return f'-{abs(word):04d}'
            else:
                return f'+{word:04d}'
        else:
            raise TypeError(f"{word} of wrong type: {type(word)}")

    def get_word(self) -> str:
        """Returns word

        Returns:
            str: Properly formatted string of the signed 4-digit integer
        """
        return self._word

    def get_sign(self) -> str:
        """Returns the sign of the word

        Returns:
            str:  Either '-' or '+'
        """
        return int(self._word[0])

    def get_command(self) -> int:
        """Returns the first two digits of the word

        Returns:
            int: First two digits describing a command to execute as an integer
        """
        return int(self._word[1:3])

    def get_pointer(self) -> int:
        """Returns the last two digits of the word

        Returns:
            int: Last two digits describing a location in memory as an integer
        """
        return int(self._word[3:])

    def __str__(self) -> str:
        """Returns a string representation of self

        Returns:
            str: Properly formatted string of the signed 4-digit integer
        """
        return self._word
    def __int__(self) -> int:
        """Returns an integer representation of self

        Returns:
            int: Signed 4-Digit Integer as a Python int
        """
        return int(self._word)
    def __bool__(self) -> bool:
        """Returns a boolean representation of self

        Returns:
            bool: True if self is positive, false if negative
        Note:
            Zero defaults to positive
        """
        return self._word[0] == '+'

    def __add__(self, other) -> int:
        """Gives addition functionality

        Args:
            other (can be int): The right-hand-operand of the addition operation

        Returns:
            int: The sum of self and other
        """
        return int(self) + int(other)
    def __sub__(self, other) -> int:
        """Gives subtraction functionality

        Args:
            other (can be int): The right-hand-operand of the subtraction operation

        Returns:
            int: self subtract other
        """
        return int(self) - int(other)
    def __floordiv__(self, other) -> int:
        """Gives floor division functionality

        Args:
            other (can be int): The right-hand-operand of the floor division operation

        Returns:
            int: self floor divide other
        """
        return int(self) // int(other)
    def __mul__(self, other) -> int:
        """Gives multiplication functionality

        Args:
            other (can be int): The right-hand-operand of the multiplication operation

        Returns:
            int: The product of self and other 
        """
        return int(self) * int(other)

    def __eq__(self, value) -> bool:
        """Gives comparison functionality

        Args:
            value (can be int): The value being compared

        Returns:
            bool: True if self is equivalent to other, else False
        """
        return int(self) == int(value)
    def __le__(self, other) -> bool:
        """Gives comparison functionality

        Args:
            other (can be int): The right-hand-operand of the less than or equal to operation

        Returns:
            bool: True if self is less than or equal to other, else False
        """
        return int(self) <= int(other)
    def __ge__(self, other) -> bool:
        """Gives comparison functionality

        Args:
            other (Can be int): The right-hand-operand of the greater than or equal to operation

        Returns:
            bool: True if self is greater than or equal to other, else False
        """
        return int(self) >= int(other)
    def __lt__(self, other) -> bool:
        """Gives comparison functionality

        Args:
            other (can be int): The right-hand-operand of the less than operation

        Returns:
            bool: True if self is strictly less than other, else False
        """
        return int(self) < int(other)
    def __gt__(self, other) -> bool:
        """Gives comparison functionality

        Args:
            other (can be int): The right-hand-operand if the greater than operation

        Returns:
            bool: True if self is strictly greater than other, else False
        """
        return int(self) > int(other)
