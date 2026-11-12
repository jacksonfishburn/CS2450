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
            list[SignedInt]: A list of SignedInt from an initial loaded list
        """
        if len(load) > self.size:
            raise ValueError(f"Loaded memory is too long (max {self.size})")
        out = []
        valid_opcodes = {10, 11, 20, 21, 30, 31, 32, 33, 40, 41, 42, 43}
        detected_len = None
        
        for idx, i in enumerate(load):
            new = str(i).strip()
            if not new:
                continue
            if new[0] not in ('-', '+'):
                new = '+' + new
            word_len = len(new) - 1
            if word_len not in (4, 6):
                raise ValueError(f"Line {idx}: must be 4 or 6 digits")
                
            # Do not allow mixing 4-digit and 6-digit words in the same file
            if detected_len is None:
                detected_len = word_len
            elif detected_len != word_len:
                raise ValueError(f"Line {idx}: Cannot mix 4-digit and 6-digit words in the same file")
                
            # Smart Conversion Rule: 4-digits to 6-digits
            if self.int_size == 6 and word_len == 4:
                sign = new[0]
                first_two = int(new[1:3])
                                 
                if sign == '+' and first_two in valid_opcodes:
                    # Treat as instruction -> +0XX0YY
                    new = f"+0{new[1:3]}0{new[3:5]}"
                else:
                    # Treat as raw number -> +/-00XXXX
                    new = f"{sign}00{new[1:5]}"
            try:
                word_obj = SignedInt(int(new), self.int_size)
                                 
                # Reject commands targeting addresses >= 250
                if word_obj.get_sign() == '+' and word_obj.get_command() in valid_opcodes:
                    if word_obj.get_command() != 43 and not (0 <= word_obj.get_pointer() < self.size):
                        raise ValueError(f"Line {idx}: target address {word_obj.get_pointer():03d} out of bounds")
                                         
                out.append(word_obj)
            except Exception:
                raise ValueError(f"{i} invalid integer")
                
        # Pads rest of memory slots with 0s
        for j in range(self.size - len(out)):
            out.append(SignedInt(size=self.int_size))
            
        return out
