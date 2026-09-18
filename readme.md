# How to use this program?
1. Run the `main.py` file.
2. It will ask for a file path. This path must be absolute.
3. If the file being run requires inputs then the program will request those. Inputs must be signed $4$-digit integers: `+xxxx` or `-xxxx` where `x` is a digit from $0$ to $9$.
4. If the file being run writes an output, it will do so.
## How to write files for this program to run?
1. Create a `.txt` file.
2. Within the `.txt` file, each line must contain a signed $4$-digit integer as previously described. These will be called an **instruction**.
3. The first $2$ digits (`+__xx`) of the **instruction** describe which *operation* to preform.
    - The sign of the **instruction** has no effect on its function but is conventionally positive.
4. The third and fourth digits (`+xx__`) describe which position in memory to *operate* on.
    - There are $100$ memory slots initialized at `00` and ending at `99`.
    - A program with $n$ instructions will occupy slots up to $n-1$.
    - ***DO NOT*** *operate* on memory slots $<n$.
5. Remember to end the program with the `+4300` **instruction**.
## What are the available operations?
| Name       | Code      | Description |
|------------|-----------|-------------|
| READ       | `+10xx`   | Read a word from the terminal into a specific location in memory |
| WRITE      | `+11xx`   | Write a word from a specific location in memory to screen |
| LOAD       | `+20xx`   | Load a word from a specific location in memory into the accumulator |
| STORE      | `+21xx`   | Store a word from the accumulator into a specific location in memory |
| ADD        | `+30xx`   | Add a word from a specific location in memory to the word in the accumulator (result stays in the accumulator) |
| SUBTRACT   | `+31xx`   | Subtract a word from a specific location in memory from the word in the accumulator (result stays in the accumulator) |
| DIVIDE     | `+32xx`   | Divide the world in the accumulator by a word from a specific location in memory (result stays in the accumulator) |
| MULTIPLY   | `+33xx`   | Multiply a word from a specific location in memory to the word in the accumulator (result stays in the accumulator) |
| BRANCH     | `+40xx`   | Branch to a specific location in memory |
| BRANCHNEG  | `+41xx`   | Branch to a specific location in memory if the accumulator is negative |
| BRANCHZERO | `+42xx`   | Branch to a specific location in memory if the accumulator is zero |
| HALT       | `+43xx`   | Stop the program |