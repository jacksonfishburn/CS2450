from classes.signed_int import SignedInt

class Memory:
    """A class used to represent a 100-word memory
    """
    def __init__(self, load: list, size = 250):
        """Initialize an instance of Memory

        Args:
            load (list): Initial memory to be loaded
        """
        self.size = size
        self.int_size = (len(str(self.size-1))*2)
        self._lis = self._make(load)

    def at(self, address: int) -> SignedInt:
        """Return the SignedInt at a specific location

        Args:
            address (int): The address of the desired SignedInt

        Raises:
            TypeError: If given address is not an integer
            IndexError: If address is negative or greater than 100

        Returns:
            SignedInt: _description_
        """
        if not type(address) is int:
            raise TypeError(f"Invalid address: {address}")
        if 0 <= address < self.size:
            return self._lis[address]
        else:
            raise IndexError(f"{address} out of range")

    def set(self, address: int, new: SignedInt ) -> None:
        """Set SignedInt at specific location in memory

        Args:
            address (int): The address where the new SignedInt will be set
            new (SignedInt | int | str): The new SignedInt to be set

        Raises:
            TypeError: If address is not an integer
            ValueError: If new is not a valid SignedInt
            TypeError: If new is not an SignedInt
            IndexError: If the address is out of range
        """
        if not type(address) is int:
            raise TypeError(f"address ({address}) of wrong type: {type(address)}")
        if 0 <= address < self.size:
            if type(new) is SignedInt:
                self._lis[address] = new
            else:
                try:
                    self._lis[address] = SignedInt(new, size=self.int_size)
                except TypeError:
                    raise TypeError(f"{new} is of invalid type: {type(new)}")
                except ValueError as e:
                    raise e
        else:
            raise IndexError(f"{address} out of range")

    def get(self) -> list:
        """Return list of SignedInt in memory

        Returns:
            list: List of SignedInt in memory
        """
        return self._lis

    def _make(self, load: list = []) -> list[SignedInt]:
        """Private method to create a list of 100 SignedInt from an initial loaded list

        Args:
            load (list, optional): List to be loaded into memory. Defaults to [].

        Raises:
            ValueError: If loaded memory is to long
            ValueError: If any object being loaded into memory is not a valid SignedInt
            TypeError: If any object being loaded into memory is not an SignedInt

        Returns:
            list[SignedInt]: A list of 100 SignedInt from an initial loaded list
        """
        out = []
        n = 0
        if len(load) > self.size:
            raise ValueError(f"loaded memory is to long")
        else:
            for i in load:
                try:
                    new = str(i)
                except:
                    raise TypeError(f"{i} of wrong type: {type(i)}")
                if not new[0] in ('-', '+'):
                    new = '+' + new
                while len(new) < self.int_size + 1:
                    new = list(new)
                    new.insert(1,'0')
                    new.insert(4,'0')
                    new = "".join(new)
                new = int(new)
                try:
                    out.append(SignedInt(new, self.int_size))
                except:
                    raise ValueError(f"{i} invalid integer")
                n += 1
            for j in range(self.size - len(out)):
                out.append(SignedInt(size=self.int_size))
        return out
