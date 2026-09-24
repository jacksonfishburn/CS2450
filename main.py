import tkinter as tk
from tkinter import filedialog, simpledialog, ttk
from classes import Operators
import os

def LoadMemory(file, memory):
    newMemory = []
    with open(file, "r") as f:
        newMemory = f.readlines()
        newMemory = [i.strip() for i in newMemory]
        max_limit = min(len(newMemory), 100) 
        for i in range(0, max_limit): 
            memory[i] = newMemory[i]
    return memory

def ValidateLine(line):
    if line[0] not in ["+", "-"]:
        raise Exception("first character of line no + or -")
    if not line[1:].isdigit():
        raise Exception("A none digit was detected in the line")
    if len(line) > 5:
        raise Exception("line", line, "is to long")


class UVSimGUI:
    def __init__(self, root):
        ##setup of the GUI window
        self.root = root
        self.root.title("UVSim - BasicML Simulator")
        self.root.geometry("800x600")

        ## operators are loaded here to be used in GUI
        self.arithmetic = Operators.Arithmetic()
        self.control = Operators.Control()
        self.inOut = Operators.InOut()
        self.loadStore = Operators.LoadStore()

        ## setup the memory, accumulator and memory location
        self.memory = ["+0000"] * 100
        self.accumulator = "+0000"
        self.memoryLoc = 0
        self.is_running = False

        self._build_ui()
        self._refresh_display()

    def _build_ui(self):
        # top Controls Frame
        ctrl_frame = tk.Frame(self.root, pady=10)
        ctrl_frame.pack(side=tk.TOP, fill=tk.X)

        ##button to load a file
        tk.Button(ctrl_frame, text="Load File", command=self.load_file).pack(side=tk.LEFT, padx=5)

        ##button to run and step through it. Grayed out until needed
        self.btn_step = tk.Button(ctrl_frame, text="Step", command=self.step_execution, state="disabled")
        self.btn_step.pack(side=tk.LEFT, padx=5)
        self.btn_run = tk.Button(ctrl_frame, text="Run", state="disabled", command=self.toggle_run)
        self.btn_run.pack(side=tk.LEFT, padx=5)

        ##button to reset
        tk.Button(ctrl_frame, text="Reset", command=self.reset_sim).pack(side=tk.LEFT, padx=5)

        # Registers Frame to show the values of the accumulator, instruction pointer, and loaded file
        reg_frame = tk.Frame(self.root, pady=10)
        reg_frame.pack(side=tk.TOP, fill=tk.X)
        self.lbl_acc = tk.Label(reg_frame, text=f"Accumulator: {self.accumulator}", font=("Consolas", 14, "bold"))
        self.lbl_acc.pack(side=tk.LEFT, padx=20)
        self.lbl_ip = tk.Label(reg_frame, text=f"Instruction Pointer: {self.memoryLoc:02d}", font=("Consolas", 14))
        self.lbl_ip.pack(side=tk.LEFT, padx=20)
        self.lbl_file = tk.Label(reg_frame, text="Loaded File: None", font=("Consolas", 14))
        self.lbl_file.pack(side=tk.LEFT, padx=15)

        ## Main Display Pane (Memory left, Output right)
        pane = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ## Memory Treeview
        mem_frame = tk.LabelFrame(pane, text="Memory (00-99)")
        pane.add(mem_frame, width=300)
        
        self.mem_tree = ttk.Treeview(mem_frame, columns=("Address", "Word"), show="headings")
        self.mem_tree.heading("Address", text="Address")
        self.mem_tree.heading("Word", text="Word")
        self.mem_tree.column("Address", width=80, anchor="center")
        self.mem_tree.column("Word", width=120, anchor="center")
        self.mem_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ## Console Output Text Widget
        out_frame = tk.LabelFrame(pane, text="Console Output")
        pane.add(out_frame)
        self.console = tk.Text(out_frame, state="disabled", bg="black", fg="green", font=("Consolas", 10))
        self.console.pack(fill=tk.BOTH, expand=True)

        ## method to log to the gui console
    def log(self, message):
        self.console.config(state="normal")
        self.console.insert(tk.END, message + "\n")
        self.console.see(tk.END)
        self.console.config(state="disabled")

        ## refresh the display to show updated values
    def _refresh_display(self):
        self.lbl_acc.config(text=f"Accumulator: {self.accumulator}")
        self.lbl_ip.config(text=f"Instruction Pointer: {self.memoryLoc:02d}")

        self.mem_tree.delete(*self.mem_tree.get_children())
        for i, word in enumerate(self.memory):
            self.mem_tree.insert("", tk.END, values=(f"{i:02d}", word))

        ## method to check the memory for errors
    def check_memory(self):
            idx = -1
            incomp = [False]
            for i in self.memory:
                idx += 1
                if i == '':
                    incomp.append(f"Empty line at {idx:02d}")
                    incomp[0] = True
                else:
                    if i[0] not in ["+", "-"]:
                        incomp.append(f"Unsigned at position {idx:02d}")
                        incomp[0] = True
                    if not i[1:].isdigit():
                        incomp.append(f"Not integer at position {idx:02d}")
                        incomp[0] = True
                    if len(i) < 5:
                        incomp.append(f"Line too short at position {idx:02d}")
                        incomp[0] = True
                    elif len(i) > 5:
                        incomp.append(f"Line too long at position {idx:02d}")
                        incomp[0] = True
                        
            if incomp[0]:
                ## Route all error printing to the GUI console
                self.log("The file you have loaded is incompatible:")
                for i in range(1, len(incomp)):
                    self.log('\t' + incomp[i])
                return False
            else:
                return True

    ## Method to load a file into memory
    def load_file(self):
            filepath = filedialog.askopenfilename(title="Select BasicML File")
            if filepath:
                self.memory = ["+0000"] * 100
                self.memory = LoadMemory(filepath, self.memory) 

                filename = os.path.basename(filepath) 
                
                ## resets the simulator every time a new file is loaded.
                self.reset_sim()
                if self.check_memory(): 
                    self.lbl_file.config(text=f"Loaded File: {filename}", fg="green")
                    self.log(f"Successfully loaded {filename}.")
                    # Enable the execution buttons now that a file is loaded
                    self.btn_step.config(state="normal")
                    self.btn_run.config(state="normal")
                    
                else:
                    self.lbl_file.config(text=f"Error with file: {filename}", fg="red") 
                    self.log(f"Failed to load {filename}. Please fix the errors listed above.")
                    ## disable the execution buttons if file is invalid
                    self.btn_step.config(state="disabled")
                    self.btn_run.config(state="disabled")
                    ##this refreshed the display to show the errors in the memory so the user can know what to change
                    self._refresh_display()

    def reset_sim(self): ##clears out the memory, accumulator, memory location, and console. Does not clear loaded file.
        self.is_running = False
        self.btn_run.config(text="Run")
        self.memoryLoc = 0
        self.accumulator = "+0000"
        self._refresh_display()
        self.console.config(state="normal")
        self.console.delete(1.0, tk.END)
        self.console.config(state="disabled")


    def toggle_run(self): ##runs the program until it is paused or halted.
        self.is_running = not self.is_running
        self.btn_run.config(text="Pause" if self.is_running else "Run")
        if self.is_running:
            self.run_cycle()

    def run_cycle(self):
        if not self.is_running: 
            return
            
        halted = self.step_execution()
        if not halted and self.is_running:
            # Executes the next step in 100ms instead of blocking the UI
            self.root.after(100, self.run_cycle)

    def step_execution(self): ##executes the next command in memory and updates the display. Returns True if halted or error, False otherwise.
        if self.memoryLoc >= 100: 
            return True
            
        i = self.memory[self.memoryLoc]
        if i is not None:
            prevMem = self.memoryLoc
            cmd = i[1] + i[2]
            
            # Adapted from the run method in our logic
            match cmd:
                case "10":
                    loc = int(i[3:5])
                    ##pop up box to get user input
                    raw_data = simpledialog.askstring("Input", f"Enter 5-character word for loc {loc:02d}:", parent=self.root)
                    
                    if raw_data is not None:
                        try:
                            ## Pass the GUI input directly to the read_input method for validation and formatting
                            target_loc, formatted_data = self.inOut.read_input(i, raw_data)
                            self.memory[target_loc] = formatted_data
                        except ValueError as e:
                            ## If user enters invalid, the program will step back one instruction to allow re-entry
                            ## Also shows a message in the console
                            self.log(str(e))
                            prevMem -= 1
                    else:
                        self.log("Input cancelled. Halting execution.")
                        self.is_running = False
                        self.btn_run.config(text="Run")
                        return True
                case "11":
                    # Redirects inOut.write_output terminal print to the GUI console
                    loc = int(i[3:5])
                    self.log(f"OUTPUT: {self.memory[loc]}")
                case "20":
                    self.accumulator = self.loadStore.load(i, self.memory)
                case "21":
                    self.memory = self.loadStore.store(i, self.memory, self.accumulator)
                case "30":
                    self.accumulator = self.arithmetic.add(i, self.memory, self.accumulator)
                case "31":
                    self.accumulator = self.arithmetic.subtract(i, self.memory, self.accumulator)
                case "32":
                    self.accumulator = self.arithmetic.divide(i, self.memory, self.accumulator)
                case "33":
                    self.accumulator = self.arithmetic.multiply(i, self.memory, self.accumulator)
                case "40":
                    self.memoryLoc = self.control.Branch(i)
                case "41":
                    self.memoryLoc = self.control.BranchNeg(i, self.accumulator, prevMem)
                case "42":
                    self.memoryLoc = self.control.BranchZero(i, self.accumulator, prevMem)
                case "43":
                    self.log("Program HALT reached.")
                    self.is_running = False
                    self.btn_run.config(text="Run")
                    return True
                case _:
                    self.log("Loaded program contains invalid command")

            # Retains overflow and validation logic, patching the sign loss bug
            if len(self.accumulator) > 5:
                sign = self.accumulator[0]
                self.accumulator = f"{sign}{self.accumulator[-4:]}"

            try:
                ValidateLine(self.accumulator)
            except Exception as e:
                self.log(f"Validation Error: {str(e)}")
                return True

            if self.memoryLoc == prevMem:
                self.memoryLoc += 1

        self._refresh_display()
        return False

if __name__ == "__main__":
    root = tk.Tk()
    app = UVSimGUI(root)
    root.mainloop()