# UVSim

UVSim is a BasicML simulator with a graphical interface.

## Prerequisites

- Python 3.10 or newer.
- Tkinter, which comes with the standard Python installer. No extra packages need to be installed.

## How to run

1. Open a terminal in this project folder.
2. Run:

```
python main.py
```

3. A window titled `UVSim - BasicML Simulator` will open.

## How to use the GUI

The window shows the accumulator, the instruction pointer, the loaded file name, memory addresses `00` through `99`, and a console.

1. Click **Load File** and choose a `.txt` program. 
2. If the file loads, the file name turns green and **Step** and **Run** become available.
3. If the file is invalid, the file name turns red and **Step** and **Run** stay disabled.
4. Click **Step** to run one instruction.
5. Click **Run** to keep running instructions. The button changes to **Pause**. Click it again to pause.
6. Click **Reset** to stop a run and clear the console. To start the program over, load the file again.
7. When a program needs input, a dialog asks for a signed 4-digit integer: `+xxxx` or `-xxxx`, where `x` is a digit from `0` to `9`. Canceling the dialog stops the program.
8. Program output is written in the console as `OUTPUT: ...`.
9. When the program halts, the console shows `Program HALT reached`.

## How to write files for this program to run

1. Create a `.txt` file.
2. Each line must contain a signed 4-digit integer, as described above. These are called an **instruction**.
3. The first 2 digits (`+__xx`) of the **instruction** describe which *operation* to perform.
    - The sign of the **instruction** has no effect on its function but is conventionally positive.
4. The third and fourth digits (`+xx__`) describe which position in memory to *operate* on.
    - There are 100 memory slots, from `00` through `99`.
    - A program with `n` instructions occupies slots up to `n-1`.
    - Do not operate on memory slots below `n`.
5. End the program with the `+4300` **instruction**.

## What are the available operations?

| Name       | Code      | Description |
|------------|-----------|-------------|
| READ       | `+10xx`   | Read a word from a dialog into a specific location in memory |
| WRITE      | `+11xx`   | Write a word from a specific location in memory to the console |
| LOAD       | `+20xx`   | Load a word from a specific location in memory into the accumulator |
| STORE      | `+21xx`   | Store a word from the accumulator into a specific location in memory |
| ADD        | `+30xx`   | Add a word from a specific location in memory to the word in the accumulator (result stays in the accumulator) |
| SUBTRACT   | `+31xx`   | Subtract a word from a specific location in memory from the word in the accumulator (result stays in the accumulator) |
| DIVIDE     | `+32xx`   | Divide the word in the accumulator by a word from a specific location in memory (result stays in the accumulator) |
| MULTIPLY   | `+33xx`   | Multiply a word from a specific location in memory to the word in the accumulator (result stays in the accumulator) |
| BRANCH     | `+40xx`   | Branch to a specific location in memory |
| BRANCHNEG  | `+41xx`   | Branch to a specific location in memory if the accumulator is negative |
| BRANCHZERO | `+42xx`   | Branch to a specific location in memory if the accumulator is zero |
| HALT       | `+43xx`   | Stop the program |
