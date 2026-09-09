class InOut:
    def __init__(self):
        pass

    def read_input(self): ##does this need to to also take memory location as a parameter?
        """READ 10 Read a word from the keyboard into a specific location in memory"""
        input_data = input("Enter valid input ex.(+1234, -1234): ")
        
        ##checks if 
        ##1: the starting character is + or -
        ##2: the rest of the input is a number
        ##3: the length of the input is 5 characters total
        if (input_data[0] not in ['+', '-']) or (not input_data[1:].isdigit() or len(input_data) != 5):
            print("Invalid input. Please enter a valid signed integer.")
            return self.read_input()  # Recursively call read_input until valid input is provided

        ##this function could return the data, or write it to the memory location.
        return input_data
    
    def write_output(self, memory, command):
        """WRITE = 11 Write a word from a specific location in memory to screen"""
        ##write output to memory. Does that need to be done here? Or another function?
        
        location = command[3] + command[4]
        location = int(location)

        message = memory[location]
        ## this function could return true or false if the write was successful or not.
        print("Memory Location: ", location, "Message: ", message)
