import tkinter as tk
from tkinter import filedialog, simpledialog, ttk
import os

from classes.uvsim import UVSim, NeedValue, GotValue, Halted
from classes.signed_4_digit_int import S4DI

_DEFAULT_PRIMARY = "#4C721D"
_DEFAULT_OFF = "#FFFFFF"

def load_colors():
    """Read primary and off colors from color_config.txt. Falls back to UVU green and white."""
    primary, off = _DEFAULT_PRIMARY, _DEFAULT_OFF
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "color_config.txt")
    try:
        with open(path, encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = (part.strip() for part in line.split("=", 1))
                if len(value) == 6:
                    value = "#" + value
                if len(value) != 7 or not value.startswith("#"):
                    continue
                try:
                    int(value[1:], 16)
                except ValueError:
                    continue
                if key.lower() == "primary":
                    primary = value
                elif key.lower() == "off":
                    off = value
    except OSError:
        pass
    return primary, off

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("UVSim - BasicML Simulator")
        self.root.geometry('800x600')

        self.primary, self.off = load_colors()
        self.root.configure(bg=self.primary)

        self.cpu = UVSim()

        self.is_running = False

        self._build_ui()
        self._refresh_display()

    def _build_ui(self):
        ctrl_frame = tk.Frame(self.root, pady=10, bg=self.primary)
        ctrl_frame.pack(side=tk.TOP, fill=tk.X)

        button_color = {"bg": self.off, "fg": "black", "activebackground": self.off, "activeforeground": "black"}
        tk.Button(ctrl_frame, text="Load File", command=self.load_file, **button_color).pack(side=tk.LEFT, padx=5)
        
        self.btn_step = tk.Button(ctrl_frame, text="Step", command=self.step_execution, state="disabled", **button_color)
        self.btn_step.pack(side=tk.LEFT, padx=5)
        self.btn_run = tk.Button(ctrl_frame, text="Run", state="disabled", command=self.toggle_run, **button_color)
        self.btn_run.pack(side=tk.LEFT, padx=5)

        tk.Button(ctrl_frame, text="Reset", command=self.reset_sim, **button_color).pack(side=tk.LEFT, padx=5)

        tk.Button(ctrl_frame, text="Save File", command=self.save_file, **button_color).pack(side=tk.LEFT, padx=5)

        reg_frame = tk.Frame(self.root, pady=10, bg=self.primary)
        reg_frame.pack(side=tk.TOP, fill=tk.X)
        self.lbl_acc = tk.Label(reg_frame, text=f"Accumulator: {self.cpu.get_accumulator()}", font=("Consolas", 14, "bold"), bg=self.primary, fg=self.off)
        self.lbl_acc.pack(side=tk.LEFT, padx=20)
        self.lbl_ip = tk.Label(reg_frame, text=f"Instruction Pointer: {self.cpu.get_pointer()}", font=("Consolas", 14), bg=self.primary, fg=self.off)
        self.lbl_ip.pack(side=tk.LEFT, padx=20)
        self.lbl_file = tk.Label(reg_frame, text="Loaded File: None", font=("Consolas", 14), bg=self.primary, fg=self.off)
        self.lbl_file.pack(side=tk.LEFT, padx=15)

        pane = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg=self.primary)
        pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        mem_frame = tk.LabelFrame(pane, text="Memory Editor(00-99)", bg=self.primary, fg=self.off)
        pane.add(mem_frame, width=300)

        self.line_numbers = tk.Text(mem_frame, width=4, padx=3, takefocus=0, state='disabled', font=("Consolas", 11))
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        self.mem_editor = tk.Text(mem_frame, wrap=tk.NONE, undo=True, font=("Consolas", 11))
        self.mem_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Initial population of 100 placeholder lines
        self.mem_editor.insert("1.0", "\n".join(["+0000"] * 100))

        # Scrollbar Syncing (Keeps line numbers and text vertically aligned)
        editor_scroll = ttk.Scrollbar(mem_frame, orient=tk.VERTICAL, command=self.mem_editor.yview)
        editor_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        def sync_yscroll(*args):
            editor_scroll.set(*args)
            self.line_numbers.yview_moveto(args[0])

        self.mem_editor.configure(yscrollcommand=sync_yscroll)
        self.mem_editor.bind("<KeyRelease>", self._update_line_numbers)

        out_frame = tk.LabelFrame(pane, text="Console Output", bg=self.primary, fg=self.off)
        pane.add(out_frame)
        self.console = tk.Text(out_frame, state="disabled", bg="black", fg="green", font=("Consolas", 10))
        self.console.pack(fill=tk.BOTH, expand=True)

    def _update_line_numbers(self, event=None):
        """Updates the line numbers dynamically as the user types or pastes."""
        self.line_numbers.config(state='normal')
        self.line_numbers.delete("1.0", tk.END)
        
        lines = int(self.mem_editor.index('end-1c').split('.')[0])
        line_num_str = "\n".join([f"{i:02d}" for i in range(max(lines, 100))])
        
        self.line_numbers.insert("1.0", line_num_str)
        self.line_numbers.config(state='disabled')

    def sync_and_validate_memory(self):
        """Pulls text from the editor, enforces 100 lines, validates, and updates backend."""
        raw_text = [line.strip() for line in self.mem_editor.get("1.0", "end-1c").split('\n')]
        
        if len(raw_text) > 100:
            self.log(f"Warning: Code exceeds 100 lines. Truncating bottom {len(raw_text) - 100} lines.")
            raw_text = raw_text[:100]
            self.mem_editor.delete("101.0", tk.END)
            self._update_line_numbers()
            
        while len(raw_text) < 100:
            raw_text.append("+0000")
            
        try:
            #Backend validation and loading of memory
            self.cpu.load_memory(raw_text)
            return True
        except Exception as e:
            self.log(f"Validation Error: {str(e)}")
            return False

    def log(self, message):
        self.console.config(state="normal")
        self.console.insert(tk.END, message + "\n")
        self.console.see(tk.END)
        self.console.config(state="disabled")

    def _refresh_display(self):
            self.lbl_acc.config(text=f"Accumulator: {self.cpu.get_accumulator()}")
            self.lbl_ip.config(text=f"Instruction Pointer: {self.cpu.get_pointer() + 1}")
            
            # Lock editor during execution & sync to backend (shows STORE updates visually)
            if self.cpu.get_pointer() > -1 or self.is_running:
                self.mem_editor.config(state="normal")
                self.mem_editor.delete("1.0", tk.END)
                # Convert S4DI objects back to strings
                self.mem_editor.insert("1.0", "\n".join(str(w) for w in self.cpu.get_memory()))
                self.mem_editor.config(state="disabled") # Lock
            else:
                self.mem_editor.config(state="normal") # Unlock for manual editing
                
            # Highlight active instruction
            self.mem_editor.tag_remove("active", "1.0", tk.END)
            next_ip = self.cpu.get_pointer() + 1 # Pointer is -1 before first step
            
            if 0 <= next_ip < 100:
                active_line = next_ip + 1
                self.mem_editor.tag_add("active", f"{active_line}.0", f"{active_line}.end")
                self.mem_editor.tag_config("active", background="#cce5ff", foreground="#004085")
                self.mem_editor.see(f"{active_line}.0")
                
            self._update_line_numbers()

    def load_file(self):
        filepath = filedialog.askopenfilename(title="Select BasicML File")
        if filepath:
            filename = os.path.basename(filepath) 
            
            with open(filepath, "r") as f:
                lines = [line.strip() for line in f.readlines()]
                
            self.mem_editor.config(state="normal")
            self.mem_editor.delete("1.0", tk.END)
            self.mem_editor.insert("1.0", "\n".join(lines))
            self._update_line_numbers()
            
            self.lbl_file.config(text=f"Loaded File: {filename}")
            self.log(f"Loaded {filename} into editor. Review, edit, and click Run/Step to execute.")
            
            self.reset_sim()
            self.btn_step.config(state="normal")
            self.btn_run.config(state="normal")

    def save_file(self):
        filepath = filedialog.asksaveasfilename(title="Select Save Location", defaultextension=".txt", filetypes=[("Text Files", "*.txt")])

        if not filepath:
            return

        self.sync_and_validate_memory()
        file = self.cpu.get_memory()

        with open(filepath, 'w') as f:
            for i in file:
                f.write(f"{i}\n")


    def reset_sim(self):
        # 1. Stop any active loops and reset button appearances/states
        self.is_running = False
        self.btn_run.config(text="Run", state="normal")
        self.btn_step.config(state="normal")
        
        # 2. Reset the backend CPU
        self.cpu.reset()
        self._refresh_display()
        
        # 3. Clear the console
        self.console.config(state="normal")
        self.console.delete(1.0, tk.END)
        self.console.config(state="disabled")


    def toggle_run(self):
        # CPU pointer starts at -1. If starting fresh, validate the editor text first.
        if self.cpu.get_pointer() == -1 and not self.is_running:
            if not self.sync_and_validate_memory():
                return
                
        self.is_running = not self.is_running
        self.btn_run.config(text="Pause" if self.is_running else "Run")
        if self.is_running:
            self.run_cycle()

    def run_cycle(self):
        # Stop the loop immediately if the user clicked Pause
        if not self.is_running: 
            return
            
        # Execute exactly one instruction
        halted = self.step_execution()
        
        # If the program hasn't halted, schedule the next cycle in 150 milliseconds
        if not halted and self.is_running:
            self.root.after(150, self.run_cycle)

    def step_execution(self):
        # 1. Sync and validate the editor text to the CPU before the very first step
        if self.cpu.get_pointer() == -1 and not self.is_running:
            if not self.sync_and_validate_memory():
                return True
                
        # 2. Prevent the simulator from attempting to step past index 99
        if self.cpu.get_pointer() >= 99:
            self.log("End of memory reached without HALT command. Halting execution.")
            self.is_running = False
            self.btn_run.config(text="Run", state="disabled")
            self.btn_step.config(state="disabled")
            self._refresh_display()
            return True
            
        halted = False
        try:
            self.cpu.step()
        except NeedValue as e:
            raw_data = simpledialog.askstring("Input", f"Enter Valid Signed 4-digit Integer for location {e.location}:", parent=self.root)
            if raw_data is not None:
                try:
                    self.cpu.set_memory_at(e.location, S4DI(raw_data))
                except ValueError as v:
                    self.log(str(v))
                    self.cpu.go_back()
            else:
                self.log("Input cancelled. Halting execution.")
                self.is_running = False
                self.btn_run.config(text="Run")
                halted = True
        except GotValue as e:
            self.log(f"OUTPUT: {e.value}")
        except Halted:
            self.log("Program HALT reached")
            self.is_running = False
            self.btn_run.config(text="Run", state="disabled") 
            self.btn_step.config(state="disabled")
            halted = True
            
        # 2. Refresh the UI AFTER the CPU has executed the instruction
        self._refresh_display()
        return halted