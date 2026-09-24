Functional Requirements:
1. The system will provide an addressable memory of 100 elements each capable of storing a signed four digit number
2. On start the program will ask the user for a text file to load into memory while doing so the program will validate each line ensuring each loaded element is appropriately formatted
3. The system shall parse each word in memory and call the operation specified in the first two digits on the location in memory specified in the last two digits
4. When the read command is run the system will accept user input from the keyboard and store the entered element into the memory location specified by the last two digits of the read command
5. When the write command is run the system will output the element stored at the memory location specified by the last two digits of the element
6. The system shall set the accumulator to a value in a specified location in memory when the LOAD operation is called
7. The system shall set a specified location in memory to the value in the accumulator when the STORE operation is called
8. When the add command is run the system will take the element stored in the memory location specified by the last two digits of the command and add it too the element stored inside the accumulator storing the result in the accumulator. if the result is larger than the expected element length the left most numeric digits will be removed until the element is the correct size
9. When the subtract command is run the system will take the element stored in the memory location specified by the last two digits of the command and subtract it from the element stored inside the accumulator storing the result in the accumulator if the absolute value of the result is larger than the expected element length the left most numeric digits will be removed until the element is the correct size
10. The system shall set the accumulator to the product of the accumulator and a specified word in memory when the MULTIPLY operation is called
11. The system shall set the accumulator to the quotient of a specified word in memory and the accumulator when the DIVIDE operation is called
12. When the branch command is run the system will move the location in memory from which it is reading to the location specified by the last two digits of the command
13. When the branch neg command is run the system will move the location in memory from which it is reading to the location specified by the last two digits of the command only if the element in the accumulator is negative
14. The system shall change its parse pointer to a specified location in memory only if the word in the accumulator is zero when the BRANCHZERO operation is called
15. The system shall stop parsing the memory when the HALT operation is called

Non-functional Requirements:
1. The system will execute BasicML programs without crashing
2. The system shall be accurate
3. The system will run each command in under 0.5 seconds