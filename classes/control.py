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
