from classes import Operators

def LoadMemory(file, memory):
    newMemory = []
    with open(file, "r") as f:
        newMemory = f.readlines()
        newMemory = [i.strip() for i in newMemory]
        for i in range(0, len(newMemory)): ##This may crash if a file longer than 100 lines is loaded.
            memory[i] = newMemory[i]
    return memory


def CheckMemory(memory):
    for i in memory:
        if i[0] not in ["+", "-"] or (not i[1:].isdigit() or len(i) != 5):
            print("The file you loaded is incompatible")


def ValidateLine(line):
    #print(type(line))
    if line[0] not in ["+", "-"]:
        raise Exception("first character of line no + or -")
    if not line[1:].isdigit():
        raise Exception("A none digit was detected in the line")
    if len(line) > 5:
        raise Exception("line", line, "is to long")


def Run(memory):
    arithmetic = Operators.Arithmetic()
    control = Operators.Control()
    inOut = Operators.InOut()
    loadStore = Operators.LoadStore()
    accumulator = "+0000"
    memoryLoc = 0


    while True:
        i = memory[memoryLoc]
        if i is not None:
            prevMem = memoryLoc
            cmd = i[1] + i[2]
            match cmd:
                case "10":
                    loc, data = inOut.read_input(i)
                    memory[loc] = data
                case "11":
                    inOut.write_output(memory, i)
                case "20":
                    accumulator = loadStore.load(i, memory)
                case "21":
                    memory = loadStore.store(i, memory, accumulator)
                case "30":
                    accumulator = arithmetic.add(i, memory, accumulator)
                case "31":
                    accumulator = arithmetic.subtract(i, memory, accumulator)
                case "32":
                    accumulator = arithmetic.divide(i, memory, accumulator)
                case "33":
                    accumulator = arithmetic.multiply(i, memory, accumulator)
                case "40":
                    memoryLoc = control.Branch(i)
                case "41":
                    memoryLoc = control.BranchNeg(i, accumulator, prevMem)
                case "42":
                    control.BranchZero(i, accumulator, prevMem)
                case "43":
                    break
                case _:
                    print("Loaded program contains invalid command")

            if len(accumulator) > 5:
                accumulator = f"+{accumulator[-4:]}"

            ValidateLine(accumulator)

            if memoryLoc == prevMem:
                memoryLoc += 1



def main():
    
    fileSelect = input("Enter the file path you would like to load into memory: ")
    
    memory = []
    for i in range(0, 100):
        memory.append("+0000")
    

    memory = LoadMemory(fileSelect, memory)
    CheckMemory(memory)

    Run(memory)



main()