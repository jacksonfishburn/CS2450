class Control:
    def __init__(self):
        pass

    def Branch(self,command):

        loc = int(command[3:])

        if loc > 99 or loc < 0: ## checks to make sure a valid location was given
            raise IndexError("Memory address out of bounds")
        return loc

    def BranchNeg(self, command, accum, fail):
        if accum[0] == "-":
            loc = command[3] + command[4]
            return int(loc)
        else:
            return fail


    def BranchZero(self, command, accum, fail):
        if accum[1:] == "0000":
            loc = command[3] + command[4]
            return int(loc)
        else:
            return fail
"""
    def Halt(self):
        pass
"""




class InOut:
    def __init__(self):
        pass

    def read_input(self,originalCmd, data):
        """READ 10 Read a word from the keyboard into a specific location in memory"""

        loc = originalCmd[3] + originalCmd[4]

        data = data.strip() ##remove whitespace

        # Automatically format and pad numbers
        if data.isdigit():
            data = f"+{data.zfill(4)}"
        elif data.startswith("-") and data[1:].isdigit():
            data = f"-{data[1:].zfill(4)}"
        
        ##checks if 
        ##1: the starting character is + or -
        ##2: the rest of the input is a number
        ##3: the length of the input is 5 characters total
        if (len(data) != 5 or not data[1:].isdigit() or data[0] not in ['+', '-']):
            raise ValueError("Invalid input. Please enter a valid number")

        
        return int(loc), data
    
    def write_output(self, memory, command): ##this method may not be needed anymore with the new gui
        """WRITE = 11 Write a word from a specific location in memory to screen"""
        
        location = int(command[3:])
        
        if location > 99 or location < 0:
            raise IndexError("Memory address out of bounds")


        message = memory[location]

        print(message)





class LoadStore:

    def __init__(self):
        pass

    def load(self, command, memory):
        # 20 load from memory into accumulator

        location = int(command[3:])
    
        if location > 99 or location < 0:
            raise IndexError("Memory address out of bounds")

        return memory[location]

    def store(self, command, memory, accumulator):
        # 21 load from accumulator into memory

        location = int(command[3:])
    
        if location > 99 or location < 0:
            raise IndexError("Memory address out of bounds")

        int(accumulator)  ##this is to check if the accumulator is a valid number. If not, it will throw an error.

        memory[location] = accumulator
        return memory




class Arithmetic:
    def __init__(self):
        pass


    def format_word(self, value):
        # Helper method to format any integer into a valid BasicML word and truncate overflows
        value = int(value)
        if value >= 0:
            ## zfill(4) pads small numbers, [-4:] slices off the front of large numbers
            return f"+{str(value).zfill(4)[-4:]}"
        else:
            return f"-{str(abs(value)).zfill(4)[-4:]}"

    def add(self, command, memory, accumulator):
        #result stays in accumulator
        location = command[3] + command[4]
        location = int(location)
        num1 = memory[location]
        if num1[0] == "+":
            num1 = int(num1[1:])
        else:
            num1 = -1 * int(num1[1:])

        num2 = accumulator
        if num2[0] == "+":
                num2 = int(num2[1:])
        else:
            num2 = -1 * int(num2[1:])

        result = num1 + num2

        result = self.format_word(result)  # Ensure the result is formatted correctly
        return result


    def subtract(self, command, memory, accumulator):
        #result stays in accumulator
        location = command[3] + command[4]
        location = int(location)
        num1 = memory[location]
        if num1[0] == "+":
            num1 = int(num1[1:])
        else:
            num1 = -1 * int(num1[1:])

        num2 = accumulator
        if num2[0] == "+":
                num2 = int(num2[1:])
        else:
            num2 = -1 * int(num2[1:])

        result = num2 - num1

        result = self.format_word(result)  # Ensure the result is formatted correctly
        return result


    def divide(self, command, memory, accumulator):
        #result stays in accumulator
        location = command[3] + command[4]
        location = int(location)
        num1 = memory[location]
        if num1[0] == "+":
            num1 = int(num1[1:])
        else:
            num1 = -1 * int(num1[1:])

        num2 = accumulator
        if num2[0] == "+":
                num2 = int(num2[1:])
        else:
            num2 = -1 * int(num2[1:])

        result = num2//num1 ##takes off any decimal places.

        result = self.format_word(result)  # Ensure the result is formatted correctly
        return result


    def multiply(self, command, memory, accumulator):
        #result stays in accumulator
        location = command[3] + command[4]
        location = int(location)
        num1 = memory[location]
        if num1[0] == "+":
            num1 = int(num1[1:])
        else:
            num1 = -1 * int(num1[1:])

        num2 = accumulator
        if num2[0] == "+":
                num2 = int(num2[1:])
        else:
            num2 = -1 * int(num2[1:])

        result = num2 * num1

        result = self.format_word(result)  # Ensure the result is formatted correctly
        return result