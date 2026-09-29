from signed_4_digit_int import S4DI

class Memory:
    """A class used to represent a 100-word memory
    """
    def __init__(self, load: list):
        """Initialize an instance of Memory

        Args:
            load (list): Initial memory to be loaded
        """
        self._lis = self._make(load)

    def at(self, address: int) -> S4DI:
        """Return the S4DI at a specific location

        Args:
            address (int): The address of the desired S4DI

        Raises:
            TypeError: If given address is not an integer
            IndexError: If address is negative or greater than 100

        Returns:
            S4DI: _description_
        """
        if not type(address) is int:
            raise TypeError(f"Invalid address: {address}")
        if 0 <= address < 100:
            return self._lis[address]
        else:
            raise IndexError(f"{address} out of range")

    def set(self, address: int, new: S4DI | int | str) -> None:
        """Set S4DI at specific location in memory

        Args:
            address (int): The address where the new S4DI will be set
            new (S4DI | int | str): The new S4DI to be set

        Raises:
            TypeError: If address is not an integer
            ValueError: If new is not a valid S4DI
            TypeError: If new is not an S4DI
            IndexError: If the address is out of range
        """
        if not type(address) is int:
            raise TypeError(f"Invalid address: {address}")
        if 0 <= address < 100:
            if type(new) is S4DI:
                self._lis[address] = new
            elif type(new) in (int, str):
                try:
                    self._lis[address] = S4DI(new)
                except ValueError:
                    raise ValueError(f"{new} is not a valid signed 4 digit integer")
            else:
                raise TypeError(f"{new} is not a signed 4 digit integer")
        else:
            raise IndexError(f"{address} out of range")

    def get(self) -> list:
        """Return list of S4DI in memory

        Returns:
            list: List of S4DI in memory
        """
        return self._lis

    def _make(self, load: list = []) -> list[S4DI]:
        """Private method to create a list of 100 S4DI from an initial loaded list

        Args:
            load (list, optional): List to be loaded into memory. Defaults to [].

        Raises:
            ValueError: If loaded memory is to long
            ValueError: If any object being loaded into memory is not a valid S4DI
            TypeError: If any object being loaded into memory is not an S4DI

        Returns:
            list[S4DI]: A list of 100 S4DI from an initial loaded list
        """
        out = []
        n = 0
        if len(load) > 100:
            raise ValueError(f"loaded memory is to long")
        else:
            for i in load:
                if type(i) is str:
                    try:
                        out.append(S4DI(i))
                    except ValueError:
                        raise ValueError(f"{i} at {n:02d} is an invalid signed 4 digit integer")
                elif type(i) is S4DI:
                    out.append(i)
                elif type(i) is int:
                    out.append(S4DI(i))
                else:
                    raise TypeError(f"{i} of wrong type: {type(i)}")
                n += 1
            for j in range(100 - len(out)):
                out.append(S4DI())
        return out
