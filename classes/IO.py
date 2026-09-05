import os
class IO:
    def __init__(self):
        pass

    def get_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()

                ##Does the data need to be processed into a list before returning it? If so, add the processing logic here.

            return content
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return None
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            return None
        
    def write_file(self, file_path, content):
        try:
            with open(file_path, 'w') as file:

                ##Does the data need to be written in a loop?

                file.write(content)
            print(f"Content written to {file_path}")
        except Exception as e:
            print(f"An error occurred while writing to the file: {e}")


    ##may also need to create a method to update one data point in the list


##simple function to test the IO class
def test_io():
    io = IO()

    test_file = os.path.join(os.path.dirname(__file__), "test_data.txt")
        
    # Test reading from the file
    read_content = io.get_file(test_file)
    print(read_content)

    new_data = []
    for i in read_content.splitlines():
        new_data.append(i)
    

    # Test writing to the file
    new_file = os.path.join(os.path.dirname(__file__), "write_data.txt")
    io.write_file(new_file, "\n".join(new_data))
    

test_io()