# User Stories

- As a Student, I want to be able to upload a variety of files, so that I can test and learn about machine language.
- As a Professor, I want to see the output, so that I can make sure the starting file and the additional values entered through the terminal are correct.
- As a math student, I want to create BasicML programs that perform calculations and automate formulas, so that I can quickly calculate results without performing the calculations manually.

# Use Cases

## Use Case 1: Load a program file
Actor: User  
System: LoadMemory / CheckMemory in main.py

Goal: Get a BasicML file into the 100-word memory list so Run can execute it.

Steps:
1. User enters a file path.
2. LoadMemory reads each line from the file.
3. Each line is copied into the matching memory slot.
4. CheckMemory makes sure the words look valid (+/- plus 4 digits).

---

## Use Case 2: READ command
Actor: InOut  
System: memory  

Goal: Read a signed word from the keyboard into a memory location.

Steps:
1. Prompt the user for a signed value.
2. Get the address from the last two digits of the word.
3. Store the entered value at that address.

---

## Use Case 3: Validate READ input
Actor: User  
System: InOut.read_input  

Goal: Only accept a valid signed 5-character word (+1234 or -1234).

Steps:
1. Prompt for input.
2. User types a word that starts with + or -.
3. Check that the rest is digits and the length is 5.
4. If it is invalid, ask again until it is valid.

---

## Use Case 4: ADD command
Actor: Arithmetic  
System: memory and accumulator  

Goal: Add a memory value to the accumulator.

Steps:
1. Parse opcode 30.
2. Get the address from the last two digits of the word.
3. Add that memory value to the accumulator.
4. Put the formatted result back in the accumulator.

---

## Use Case 5: SUBTRACT command
Actor: Arithmetic  
System: memory and accumulator  

Goal: Subtract a memory value from the accumulator.

Steps:
1. Parse opcode 31.
2. Get the address from the last two digits of the word.
3. Subtract that memory value from the accumulator.
4. Put the formatted result back in the accumulator.

---

## Use Case 6: MULTIPLY command
Actor: Arithmetic  
System: memory and accumulator  

Goal: Multiply the accumulator by a memory value.

Steps:
1. Parse opcode 33.
2. Get the address from the last two digits of the word.
3. Multiply the accumulator by that memory value.
4. Put the formatted result back in the accumulator.

---

## Use Case 7: DIVIDE command
Actor: Arithmetic  
System: memory and accumulator  

Goal: Divide the accumulator by a memory value.

Steps:
1. Parse opcode 32.
2. Get the address from the last two digits of the word.
3. Integer-divide the accumulator by that memory value.
4. Put the formatted result back in the accumulator.

---

## Use Case 8: STORE command
Actor: LoadStore  
System: memory and accumulator  

Goal: Copy the accumulator into a memory location.

Steps:
1. Parse opcode 21.
2. Get the address from the last two digits of the word.
3. Confirm the accumulator is a valid number.
4. Write the accumulator into that memory slot.

---

## Use Case 9: LOAD command
Actor: LoadStore  
System: memory and accumulator  

Goal: Load a value from memory into the accumulator.

Steps:
1. Parse opcode 20.
2. Get the address from the last two digits of the word.
3. Fetch the value at that address.
4. Copy it into the accumulator.

---

## Use Case 10: WRITE command
Actor: InOut  
System: memory  

Goal: Print a word from memory to the screen.

Steps:
1. Parse opcode 11.
2. Get the address from the last two digits of the word.
3. Fetch the value at that address.
4. Print it.

---

## Use Case 11: BRANCH command
Actor: Control  
System: memoryLoc in Run  

Goal: Jump to another instruction.

Steps:
1. Parse opcode 40.
2. Get the target address from the last two digits of the word.
3. Make sure that address is in range (0–99).
4. Set memoryLoc to that address so the next instruction comes from there.

---

## Use Case 12: BRANCHNEG / BRANCHZERO
Actor: Control  
System: accumulator and memoryLoc  

Goal: Jump only if the accumulator is negative or zero.

Steps:
1. Parse opcode 41 or 42.
2. Check the accumulator (- for BRANCHNEG, 0 for BRANCHZERO).
3. If the condition matches, jump to the address in the word.
4. If not, keep going at the next instruction.

---

## Use Case 13: HALT command
Actor: Run  
System: the instruction loop in main.py  

Goal: Stop executing when HALT is reached.

Steps:
1. Parse opcode 43.
2. Break out of the while True loop.
3. No more instructions are run.

---

## Use Case 14: Invalid opcode
Actor: Run  
System: the instruction loop in main.py  

Goal: Notice a command that is not one of the supported opcodes.

Steps:
1. Read the opcode from the current word.
2. If it does not match a known case (10–11, 20–21, 30–33, 40–43), hit the default branch.
3. Print that the loaded program contains an invalid command.
