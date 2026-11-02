from classes.signed_int import SignedInt

class Accumulator:
    """A class used to represent an Accumulator
    """
    def __init__(self, int_size):
        """Initialize an Accumulator instance
        """
        self._word = SignedInt(size=int_size)

    def set_word(self, new: SignedInt ) -> None:
        """Set the word in the accumulator

        Args:
            new (SignedInt | int | str): New word to be in the accumulator

        Raises:
            TypeError: If new cannot be formatted as a SignedInt
        """
        if type(new) is SignedInt:
            self._word = new
        else:
            try:
                self._word = SignedInt(new)
            except:
                raise TypeError(f"{new} of wrong type: {type(new)}")

    def add(self, other: SignedInt | int) -> None:
        """Add other to word in accumulator, storing the result

        Args:
            other (SignedInt | int): Value to be added to accumulator
        """
        self.set_word(self._word + other)
    def sub(self, other: SignedInt | int ) -> None:
        """Subtract other from word in accumulator, storing the result

        Args:
            other (SignedInt | int): Value to be subtracted from accumulator
        """
        self.set_word(self._word - other)
    def div(self, other: SignedInt | int ) -> None:
        """Floor divide accumulator by other, storing the result
        Args:
            other (SignedInt | int): Value to divide accumulator by
        """
        self.set_word(self._word // other)
    def mul(self, other: SignedInt | int ) -> None:
        """Multiply accumulator and other, storing the result

        Args:
            other (SignedInt | int): Value to be multiply accumulator by
        """
        self.set_word(self._word * other)

    def get_word(self) -> SignedInt:
        """Get word in accumulator

        Returns:
            SignedInt: Word in accumulator
        """
        return self._word