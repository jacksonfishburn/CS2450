class Accumulator:
    def __init__(self):
        """A separate register into which information can be placed for the UVSim CPU to use it in calculations is also part of the system"""
        self.word = 0 # store word in accumulator

    def add(self, word_mem):
        """30 Add a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator)"""
        self.word = self.word + word_mem # modify word in accumulator with word from memory
    
    def subtract(self, word_mem):
        """31 Subtract a word from a specific location in memory from the word in the accumulator (leave the result in the accumulator)"""
        self.word = self.word - word_mem # modify word in accumulator with word from memory

    def divide(self, word_mem):
        """32 Divide the word in the accumulator by a word from a specific location in memory (leave the result in the accumulator)"""
        self.word = self.word / word_mem # modify word in accumulator with word from memory

    def multiply(self, word_mem):
        """33 multiply a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator)"""
        self.word = self.word * word_mem # modify word in accumulator with word from memory