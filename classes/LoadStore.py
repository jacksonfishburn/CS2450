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