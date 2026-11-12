import tkinter as tk
from tkinter import filedialog, simpledialog, ttk
import os

from classes.uvsim import UVSim, NeedValue, GotValue, Halted
from classes.signed_int import SignedInt

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

        self.open_files = {} 
        self.current_file = None

        self._build_ui()
        self._refresh_display()

    def _build_ui(self):
        ctrl_frame = tk.Frame(self.root, pady=10, bg=self.primary)
        ctrl_frame.pack(side=tk.TOP, fill=tk.X)

        button_color = {"bg": self.off, "fg": "black", "activebackground": self.off, "activeforeground": "black"}
        tk.Button(ctrl_frame, text="Load File", command=self.load_file, **button_color).pack(side=tk.LEFT, padx=5)
        
        self.btn_step = tk.Button(ctrl_frame, text="Step", command=self.step_execution, state="normal", **button_color)
        self.btn_step.pack(side=tk.LEFT, padx=5)
        self.btn_run = tk.Button(ctrl_frame, text="Run", state="normal", command=self.toggle_run, **button_color)
        self.btn_run.pack(side=tk.LEFT, padx=5)

        tk.Button(ctrl_frame, text="Reset", command=self.reset_sim, **button_color).pack(side=tk.LEFT, padx=5)

        tk.Button(ctrl_frame, text="Save File", command=self.save_file, **button_color).pack(side=tk.LEFT, padx=5)

        tk.Button(ctrl_frame, text="New Window", command=self.new_window, **button_color).pack(side=tk.LEFT, padx=5)

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

        # Initial population of 1000 placeholder lines
        self.mem_editor.insert("1.0", "\n".join(["+000000"] * self.cpu.memory_size))

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
        line_num_str = "\n".join([f"{i:03d}" for i in range(max(lines, self.cpu.memory_size))])
        
        self.line_numbers.insert("1.0", line_num_str)
        self.line_numbers.config(state='disabled')

    ##self.mem_editor
    def sync_and_validate_memory(self):
        """Pulls text from the editor, enforces memory_size lines, validates, and updates backend."""
        # Read directly from single mem_editor widget
        raw_text = [line.strip() for line in self.mem_editor.get("1.0", "end-1c").split('\n')]
                  
        # Remove trailing empty lines to prevent artificial padding conflicts
        while raw_text and not raw_text[-1]:
            raw_text.pop()
                           
        if len(raw_text) > self.cpu.memory_size:
            self.log(f"Warning: Code exceeds {self.cpu.memory_size} lines. Truncating.")
            raw_text = raw_text[:self.cpu.memory_size]
            self.mem_editor.delete(f"{self.cpu.memory_size + 1}.0", tk.END)
            self._update_line_numbers()
                           
        # Dynamically determine the dominant word length of the actual code
        dominant_len = 6 # default to 6
        for line in raw_text:
            if line and line not in ("+0000", "+000000"):
                # If a 4-digit word (+XXXX) is detected, switch dominant length to 4
                if len(line) == 5 or (len(line) == 4 and line[0] not in ('+', '-')):
                    dominant_len = 4
                break
                
        pad_word = "+0000" if dominant_len == 4 else "+000000"
        
        # Sanitize: if a line is just the wrong default padding, auto-replace it to match
        wrong_pad = "+000000" if dominant_len == 4 else "+0000"
        for i in range(len(raw_text)):
            if raw_text[i] == wrong_pad:
                raw_text[i] = pad_word

        # Pad the rest of the editor with the matching word length
        while len(raw_text) < self.cpu.memory_size:
            raw_text.append(pad_word)
                           
        try:
            # Backend validation and loading of memory (also converts 4-digit to 6-digit)
            self.cpu.load_memory(raw_text)
            
            # Update the open files dictionary if a file is currently active
            if self.current_file:
                self.open_files[self.current_file] = [str(w) for w in self.cpu.get_memory()]
                
            # Auto-update the GUI editor (shows the 4-to-6 digit conversion visually)
            self.mem_editor.config(state="normal")
            self.mem_editor.delete("1.0", tk.END)
            self.mem_editor.insert("1.0", "\n".join(str(w) for w in self.cpu.get_memory()))
            
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
                # Convert SignedInt objects back to strings
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

    def new_window(self):
        GUI(tk.Toplevel(self.root))

    def load_file(self):
        filepath = filedialog.askopenfilename(title="Select BasicML File", parent=self.root)
        if filepath:
            filename = os.path.basename(filepath)
            self.root.title(f"UVSim - {filename}")
            
            with open(filepath, "r") as f:
                # Replaces any weird formatting/newlines with spaces, then splits into individual words
                raw_content = f.read()
                lines = [word.strip() for word in raw_content.replace('\n', ' ').split() if word.strip()]
                
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
        filepath = filedialog.asksaveasfilename(title="Select Save Location", defaultextension=".txt", filetypes=[("Text Files", "*.txt")], parent=self.root)

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
        # Stop the loop immediately if the user clicked Pause or closed this window
        if not self.is_running or not self.root.winfo_exists():
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
                
        # 2. Prevent stepping past memory limits
        if self.cpu.get_pointer() >= self.cpu.memory_size - 1:
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
            raw_data = simpledialog.askstring("Input", f"Enter Valid Signed {self.cpu._mem.int_size}-digit Integer for location {e.location:03d}:", parent=self.root)
            if raw_data is not None and raw_data.strip() != "":
                try:
                    self.cpu.set_memory_at(e.location, SignedInt(raw_data.strip(), size=self.cpu._mem.int_size))
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
                      
        # 3. Refresh the UI AFTER the CPU has executed the instruction
        self._refresh_display()
        return halted