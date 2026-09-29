from signed_4_digit_int import S4DI

class Accumulator:
    """A class used to represent an Accumulator
    """
    def __init__(self):
        """Initialize an Accumulator instance
        """
        self._word = S4DI()

    def set_word(self, new:S4DI|int|str) -> None:
        """Set the word in the accumulator

        Args:
            new (S4DI | int | str): New word to be in the accumulator

        Raises:
            TypeError: If new cannot be formatted as a S4DI
        """
        if type(new) is S4DI:
            self._word = new
        elif type(new) in (str, int):
            try:
                self._word = S4DI(new)
            except:
                self._word = S4DI()
        else:
            raise TypeError(f"{new} of wrong type: {type(new)}")

    def add(self, other:S4DI|int) -> None:
        """Add other to word in accumulator, storing the result

        Args:
            other (S4DI | int): Value to be added to accumulator
        """
        self.set_word(self._word + other)
    def sub(self, other:S4DI|int) -> None:
        """Subtract other from word in accumulator, storing the result

        Args:
            other (S4DI | int): Value to be subtracted from accumulator
        """
        self.set_word(self._word - other)
    def div(self, other:S4DI|int) -> None:
        """Floor divide accumulator by other, storing the result

        Args:
            other (S4DI | int): Value to divide accumulator by
        """
        self.set_word(self._word // other)
    def mul(self, other:S4DI|int) -> None:
        """Multiply accumulator and other, storing the result

        Args:
            other (S4DI | int): Value to be multiply accumulator by
        """
        self.set_word(self._word * other)

    def get_word(self) -> S4DI:
        """Get word in accumulator

        Returns:
            S4DI: Word in accumulator
        """
        return self._word