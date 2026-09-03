class Arithmetic:
    def __init__():
        """"""
        pass

    def add(self, word_mem, word_acu):
        """30 Add a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator)"""
        word_acu = word_acu + word_mem
    
    def subtract(self, word_mem, word_acu):
        """31 Subtract a word from a specific location in memory from the word in the accumulator (leave the result in the accumulator)"""
        word_acu = word_acu - word_mem

    def divide(self, word_mem, word_acu):
        """32 Divide the word in the accumulator by a word from a specific location in memory (leave the result in the accumulator)"""
        word_acu = word_acu / word_mem

    def multiply(self, word_mem, word_acu):
        """33 multiply a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator)"""
        word_acu = word_acu * word_mem