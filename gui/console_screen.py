import customtkinter as ctk
import gui.style_constants as sty

# --- GLOBAL INTERFACE ---
_app_console_screen: ConsoleScreen | None = None
'''This variable holds the console screen instance.'''

def cys_console(*text):
    '''log something on the console screen'''
    if _app_console_screen:
        for t in text:
            _app_console_screen.write(t)
    else:
        print(f"Console not ready: {text}")

class ConsoleScreen(ctk.CTkFrame):
    def __init__(self, master, max_lines=100, *args, **kwargs):
        super().__init__(master, fg_color=sty.console_bg,
                          *args, **kwargs)
        self.max_lines = max_lines
        self.textbox = ctk.CTkTextbox(
            self, 
            fg_color="transparent", 
            text_color="lime", # Classic "Hacker" green
            font=("Consolas", 12), # Good monospaced font for Windows
            state="disabled" # Prevent user from typing in it
        )
        self.textbox.pack(expand=True, fill="both", padx=5, pady=(5, 10))

    def write(self, message):
        # 1. Enable editing to add text
        self.textbox.configure(state="normal")
        
        # 2. Add the message with a newline
        self.textbox.insert("end", f"> {message}\n")
        
        # 3. Auto-cut logic (Memory Management)
        line_count = int(self.textbox.index('end-1c').split('.')[0])
        if line_count > self.max_lines:
            # Delete from the very beginning (1.0) to the end of the first line (2.0)
            self.textbox.delete("1.0", "2.0")
            
        # 4. Auto-scroll to the bottom
        self.textbox.see("end")
        
        # 5. Disable editing again
        self.textbox.configure(state="disabled")