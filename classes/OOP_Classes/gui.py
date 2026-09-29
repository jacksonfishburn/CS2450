import tkinter as tk
from tkinter import filedialog, simpledialog, ttk
import os

from uvsim import UVSim, NeedValue, GotValue, Halted
from signed_4_digit_int import S4DI

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("UVSim - BasicML Simulator")
        self.root.geometry('800x600')

        self.cpu = UVSim()

        self.is_running = False

        self._build_ui()
        self._refresh_display()

    def _build_ui(self):
        ctrl_frame = tk.Frame(self.root, pady=10)
        ctrl_frame.pack(side=tk.TOP, fill=tk.X)

        tk.Button(ctrl_frame, text="Load File", command=self.load_file).pack(side=tk.LEFT, padx=5)
        
        self.btn_step = tk.Button(ctrl_frame, text="Step", command=self.step_execution, state="disabled")
        self.btn_step.pack(side=tk.LEFT, padx=5)
        self.btn_run = tk.Button(ctrl_frame, text="Run", state="disabled", command=self.toggle_run)
        self.btn_run.pack(side=tk.LEFT, padx=5)

        tk.Button(ctrl_frame, text="Reset", command=self.reset_sim).pack(side=tk.LEFT, padx=5)

        reg_frame = tk.Frame(self.root, pady=10)
        reg_frame.pack(side=tk.TOP, fill=tk.X)
        self.lbl_acc = tk.Label(reg_frame, text=f"Accumulator: {self.cpu.get_accumulator()}", font=("Consolas", 14, "bold"))
        self.lbl_acc.pack(side=tk.LEFT, padx=20)
        self.lbl_ip = tk.Label(reg_frame, text=f"Instruction Pointer: {self.cpu.get_pointer()}", font=("Consolas", 14))
        self.lbl_ip.pack(side=tk.LEFT, padx=20)
        self.lbl_file = tk.Label(reg_frame, text="Loaded File: None", font=("Consolas", 14))
        self.lbl_file.pack(side=tk.LEFT, padx=15)

        pane = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        mem_frame = tk.LabelFrame(pane, text="Memory (00-99)")
        pane.add(mem_frame, width=300)

        self.mem_tree = ttk.Treeview(mem_frame, columns=("Address", "Word"), show="headings")
        self.mem_tree.heading("Address", text="Address")
        self.mem_tree.heading("Word", text="Word")
        self.mem_tree.column("Address", width=80, anchor="center")
        self.mem_tree.column("Word", width=120, anchor="center")
        self.mem_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        out_frame = tk.LabelFrame(pane, text="Console Output")
        pane.add(out_frame)
        self.console = tk.Text(out_frame, state="disabled", bg="black", fg="green", font=("Consolas", 10))
        self.console.pack(fill=tk.BOTH, expand=True)

    def log(self, message):
        self.console.config(state="normal")
        self.console.insert(tk.END, message + "\n")
        self.console.see(tk.END)
        self.console.config(state="disabled")

    def _refresh_display(self):
        self.lbl_acc.config(text=f"Accumulator: {self.cpu.get_accumulator()}")
        self.lbl_ip.config(text=f"Instruction Pointer: {self.cpu.get_pointer()}")

        self.mem_tree.delete(*self.mem_tree.get_children())
        for i, word in enumerate(self.cpu.get_memory()):
            self.mem_tree.insert("", tk.END, values=(f"{i:02d}", word))

    def load_file(self):
        filepath = filedialog.askopenfilename(title="Select BasicML File")
        self.log(f"loading {filepath}")
        if filepath:
            new = []
            with open(filepath, 'r') as f:
                new = [i.strip() for i in f.readlines()]
            try:
                self.cpu.load_memory(new)
                check_memory = True
            except:
                check_memory = False

            filename = os.path.basename(filepath) 
            
            ## resets the simulator every time a new file is loaded.
            self.reset_sim()
            if check_memory:
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

    def reset_sim(self):
        self.is_running = False
        self.btn_run.config(text="Run")
        self.memoryLoc = 0
        self.accumulator = "+0000"
        self._refresh_display()
        self.console.config(state="normal")
        self.console.delete(1.0, tk.END)
        self.console.config(state="disabled")

    def toggle_run(self):
        self.is_running = not self.is_running
        self.btn_run.config(text="Pause" if self.is_running else "Run")
        if self.is_running:
            self.run_cycle()

    def run_cycle(self):
        if not self.is_running: 
            return
            
        halted = self.step_execution()
        if not halted and self.is_running:
            # Executes the next step in 1ms instead of blocking the UI
            self.root.after(1, self.run_cycle)

    def step_execution(self):
        if self.cpu.get_pointer() >= 100:
            return True
        try:
            self.cpu.step()
        except NeedValue as e:
            raw_data = simpledialog.askstring("Input", f"Enter Valid Signed 4-digit Integer for location {e.location}:", parent=self.root)
            if raw_data is not None:
                try:
                    self.cpu.set_memory_at(e.location, S4DI(raw_data))
                except ValueError as v:
                    self.log(str(e))
                    self.cpu.go_back()
            else:
                self.log("Input cancelled. Halting execution.")
                self.is_running = False
                self.btn_run.config(text="Run")
                return True
        except GotValue as e:
            self.log(f"OUTPUT: {e.value}")
        except Halted:
            self.log("Program HALT reached")
            self.is_running = False
            self.btn_run.config(text="Run")
            return True
        self._refresh_display()
        return False