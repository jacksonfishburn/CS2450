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