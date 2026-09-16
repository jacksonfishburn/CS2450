class Control:
    def __init__(self):
        pass

    def Branch(self,command):
        loc = command[3] + command[4]
        loc = int(loc)
        return loc

    def BranchNeg(self, command, fail):
        if command[0] == "-":
            loc = command[3] + command[4]
            return loc
        else:
            return fail


    def BranchZero(self, command, accum, fail):
        if accum == 0:
            loc = command[3] + command[4]
            return loc
        else:
            return fail
"""
    def Halt(self):
        pass
"""




class InOut:
    def __init__(self):
        pass

    def read_input(self,originalCmd):
        """READ 10 Read a word from the keyboard into a specific location in memory"""
        data = input("Enter valid input ex.(+1234, -1234): ")

        loc = originalCmd[3] + originalCmd[4]
        
        ##checks if 
        ##1: the starting character is + or -
        ##2: the rest of the input is a number
        ##3: the length of the input is 5 characters total
        if (data[0] not in ['+', '-']) or (not data[1:].isdigit() or len(data) != 5):
            print("Invalid input. Please enter a valid signed integer.")
            return self.read_input(originalCmd)  # Recursively call read_input until valid input is provided

        
        return int(loc), data
    
    def write_output(self, memory, command):
        """WRITE = 11 Write a word from a specific location in memory to screen"""
        ##write output to memory. Does that need to be done here? Or another function?
        
        location = command[3] + command[4]
        location = int(location)

        message = memory[location]
        ## this function could return true or false if the write was successful or not.
        ##print("Memory Location: ", location, "Message: ", message)
        print(message)





class LoadStore:

    def __init__(self):
        pass

    def load(self, command, memory):
        # 20 load from memory into accumulator
        # acc = registers[i] 
        location = command[3] + command[4]
        location = int(location)
        return memory[location]

    def store(self, command, memory, accumulator):
        # 21 load from accumulator into memory
        # registers[i] = acc
        location = command[3] + command[4]
        location = int(location)
        memory[location] = accumulator
        return memory




class Arithmetic:
    def __init__(self):
        pass

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

        if result >= 0:
             result = f"+ {result}"
        else:
             result = str(result)
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

        if result >= 0:
             result = f"+ {result}"
        else:
             result = str(result)
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

        result = num2/num1

        if result >= 0:
             result = f"+ {result}"
        else:
             result = str(result)
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

        if result >= 0:
             result = f"+ {result}"
        else:
             result = str(result)
        return result