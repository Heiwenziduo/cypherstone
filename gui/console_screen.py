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

def cys_greeting():
    '''Hello from CypherStone.'''
    if _app_console_screen:
        _app_console_screen.write("Welcome using CypherStone.", is_greeting=True)
    else:
        print(f"Console not ready: greeting")

def cys_console_current_user():
    ''''''
    if _app_console_screen:
        _app_console_screen.write("")

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

        # Define some "Highlighters" (Tags)
        # Note: We access the underlying tkinter widget using self.textbox._textbox
        self.txt = self.textbox._textbox 
        self.txt.tag_config("info", foreground="white")
        self.txt.tag_config("success", foreground="#00FF00") # Lime Green
        self.txt.tag_config("error", foreground="#FF4444")   # Soft Red
        self.txt.tag_config("cursor", foreground="white")
        
        self.cursor_char = "█" # substitute: _  ┃
        self.cursor_visible = False
        self.is_typing = False # Track if typewriter is active
        
        # Start the blinking loop immediately
        self._blink()

    def _blink(self):
        """Toggle the cursor on and off."""
        # Only blink if we aren't currently typing (typewriter handles its own cursor)
        if not self.is_typing:
            self.textbox.configure(state="normal")
            if self.cursor_visible:
                # Delete the last character (the cursor)
                self.textbox.delete("end-2c", "end-1c")
                self.cursor_visible = False
            else:
                # Insert the cursor
                self.textbox.insert("end", self.cursor_char, "cursor")
                self.cursor_visible = True
            self.textbox.configure(state="disabled")

        # Repeat every a few ms
        self.after(750, self._blink)

    def write(self, message, tag="info", typewriter=True, is_greeting=False):
        self.is_typing = True
        self.textbox.configure(state="normal")
        
        # Remove cursor before starting typewriter
        if self.cursor_visible:
            self.textbox.delete("end-2c", "end-1c")
            self.cursor_visible = False

        # Check if this is the first line
        # is_greeting = len(self.textbox.get("0.0", "end")) == 0 or self.textbox.get("0.0", "end").startswith(self.cursor_char)
        msg = f"> {message}" if is_greeting else f"\n> {message}" # this make cursor at the same line

        if typewriter:
            self._typewriter_effect(msg, tag, 0)
        else:
            self.textbox.insert("end", msg, tag)
            self._finish_writing()

    def _typewriter_effect(self, full_text, tag, index):
        if index < len(full_text):
            # Insert one character at a time with the tag
            self.textbox.insert("end", full_text[index], tag)
            self.textbox.see("end")
            # Wait 30ms then call itself for the next character
            # TODO: longer text shorter delay
            delay = 30
            self.after(delay, lambda: self._typewriter_effect(full_text, tag, index + 1))
        else:
            self._finish_writing()

    def _finish_writing(self):
        """Cleanup after text is finished."""
        self._check_memory()
        self.is_typing = False
        self.textbox.configure(state="disabled")

    def _check_memory(self):
        # TODO: cursor effect may wreck the line_count
        # Keeps the console from getting too long
        line_count = int(self.textbox.index('end-1c').split('.')[0])
        if line_count > 100:
            self.textbox.delete("1.0", "2.0")