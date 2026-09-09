##CS2450
from classes import Arithmetic, Control, InOut, LoadStore


def main():
    
    fileSelect = input("enter the file path you would like to load into memory")
    
    memory = []
    for i in range(0, 100):
        memory.append(None)
    
    #print(memory)
    memory = LoadMemory(fileSelect, memory)
    CheckMemory(memory)

    Run(memory)



main()

def LoadMemory(file, memory):
    with open(file, "r") as f:
        for i in f:
            memory[i] = i
    return memory


def CheckMemory(memory):
    for i in memory:
        if i[0] not in ["+", "-"] or (not i[1:].isdigit() or len(i) != 5):
            print("The file you loaded is incompatible")


def Run(memory):
    arithmetic = Arithmetic.Arithmetic()
    control = Control.Control()
    inOut = InOut.InOut()
    loadStore = LoadStore.LoadStore()
    accumulator = 0
    memoryLoc = 0


    while True:
        i = memory[memoryLoc]
        if i is not None:
            prevMem = memoryLoc
            cmd = i[1] + i[2]
            match cmd:
                case "10":
                    memory[memoryLoc] = inOut.read_input(memory)
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
                    memoryLoc = control.BranchNeg(i, prevMem)
                case "42":
                    control.BranchZero(i, accumulator, prevMem)
                case "43":
                    break
                case _:
                    print("Loaded program contains invalid command")
            if memoryLoc == prevMem:
                memoryLoc += 1