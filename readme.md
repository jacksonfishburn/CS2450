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

### Load a File

1. Click **Load File** and choose a `.txt` program. 
2. If the file loads, the file name turns green and **Step** and **Run** become available.
3. If the file is invalid, the file name turns red and **Step** and **Run** stay disabled.

### Editing a file
1. Once a file is loaded, the memory can be directly editied through the UI.
### Saving the File
1. Clicking on the save button will save current memory over the loaded file. The name of the loaded file is displayed.
### Running the File

1. Click **Step** to run one instruction.
2. Click **Run** to keep running instructions. The button changes to **Pause**. Click it again to pause.
3. Click **Reset** to stop a run and clear the console.
4. When a program needs input, a dialog asks for a signed 4-digit integer: `+xxxx` or `-xxxx`, where `x` is a digit from `0` to `9`. Canceling the dialog stops the program.
5. Program output is written in the console as `OUTPUT: ...`.
6. When the program halts, the console shows `Program HALT reached`.


## How to write files for this program to run

1. Create a `.txt` file.
2. Each line must contain a signed 4-digit integer, as described above. These are called an **instruction**.
3. The first 2 digits (`+XXxx`) of the **instruction** describe which *operation* to perform.
    - The sign of the **instruction** has no effect on its function but is conventionally positive.
4. The third and fourth digits (`+xxXX`) describe which position in memory to *operate* on.
    - There are 100 memory slots, from `00` through `99`.
    - A program with `n` instructions occupies slots up to `n-1`.
    - Do not operate on memory slots below `n`.
5. End the program with the `+4300` **instruction**.

## What are the available operations?

| Name       | Code      | Description |
|------------|-----------|-------------|
| READ       | `+10xx`   | Read a word from a dialog into the memory at `xx` |
| WRITE      | `+11xx`   | Write a word from the memory at `xx` to the console |
| LOAD       | `+20xx`   | Load a word from the memory at `xx` into the accumulator |
| STORE      | `+21xx`   | Store a word from the accumulator into the memory at `xx` |
| ADD        | `+30xx`   | Add a word from the memory at `xx` to the word in the accumulator (result stays in the accumulator) |
| SUBTRACT   | `+31xx`   | Subtract a word from the memory at `xx` from the word in the accumulator (result stays in the accumulator) |
| DIVIDE     | `+32xx`   | Divide the word in the accumulator by a word from the memory at `xx` (result stays in the accumulator) |
| MULTIPLY   | `+33xx`   | Multiply a word from the memory at `xx` to the word in the accumulator (result stays in the accumulator) |
| BRANCH     | `+40xx`   | Branch to the memory at `xx` |
| BRANCHNEG  | `+41xx`   | Branch to the memory at `xx` if the accumulator is negative |
| BRANCHZERO | `+42xx`   | Branch to the memory at `xx` if the accumulator is zero |
| HALT       | `+43xx`   | Stop the program |
