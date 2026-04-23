from collections import deque
import multiprocessing

import customtkinter as ctk
import gui.style_constants as sty
from thread.cs_multiprocessing import multiprocessing_decrypt, multiprocessing_encrypt

# --- GLOBAL INTERFACE ---
_app_console_screen: ConsoleScreen | None = None
'''This variable holds the console screen instance.'''
_app_multiprocessing_queue = multiprocessing.Queue()
''''''

def multiprocessing_crypto(name: str, *args):
    '''name=encrypt for encrypting otherwise for decrypting'''
    if _app_console_screen:
        target = multiprocessing_encrypt if name=="encrypt" else multiprocessing_decrypt
        ## RSAPublicKey is unhashable
        worker = multiprocessing.Process(target=target, args={*args, _app_multiprocessing_queue})
        worker.start()

        _app_console_screen._multiprocessing_queue()

        return worker



def cys_console(*text, tag="info"):
    '''log something on the console screen'''
    if _app_console_screen:
        for t in text:
            _app_console_screen.write(t, tag=tag)
    else:
        print(f"Console not ready: {text}")

def cys_error(e: Exception):
    cys_console(e, tag="error")

def cys_greeting():
    '''Hello from CypherStone.'''
    if _app_console_screen:
        _app_console_screen.write("Welcome using CypherStone.", is_greeting=True)
        cys_console_current_user()
    else:
        print(f"Console not ready: greeting")

def cys_console_current_user():
    ''''''
    if _app_console_screen:
        _app_console_screen.write(f"Current user: {"unknown user"}.")

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
        
        # cursor
        self.cursor_char = "█" # substitute: _  ┃
        self.cursor_visible = False
        self.MIN_DELAY = 5
        self.MAX_DELAY = 40
        self.BASE_DELAY = 30
        
        # queue
        self.msg_queue = deque() # Stores (message, tag) tuples
        self.is_processing = False

        # Start the blinking loop immediately
        self._blink()

    def write(self, message, tag="info", typewriter=True, is_greeting=False):
        """Public method to add messages to the queue."""
        msg = f"> {message}" if is_greeting else f"\n> {message}" # this make cursor at the same line
        self.msg_queue.append((msg, tag))
        if not self.is_processing:
            self._msg_queue()

        # if typewriter:
        #     self._typewriter_step(msg, tag, 0)
        # else:
        #     self.textbox.insert("end", msg, tag)
        #     self._finish_writing()

    def _msg_queue(self):
        """Picks the next message from the queue."""
        if not self.msg_queue:
            self._finish_writing()
            return

        self.is_processing = True
        self.textbox.configure(state="normal")

        # Remove cursor before typing starts
        if self.cursor_visible:
            self.textbox.delete("end-2c", "end-1c")
            self.cursor_visible = False

        next_msg, tag = self.msg_queue.popleft()
        left = len(self.msg_queue)
        self._typewriter_step(next_msg, tag, 0)

    def _multiprocessing_queue(self):
        """Checks the queue every 100ms."""
        try:
            while not _app_multiprocessing_queue.empty():
                msg = _app_multiprocessing_queue.get_nowait()
                if msg == "Done":
                    # log_to_console("Success!", tag="success")
                    return
                elif "Error" in str(msg):
                    # log_to_console(msg, tag="error")
                    return
                else:
                    ''
                    # progress bar number
                    # log_to_console(f"Progress: {msg}")
                    
                    # Keep checking until we get a 'Done' or 'Error'
            self.after(100, self._multiprocessing_queue)
        except:
            # print()
            pass

    def _blink(self):
        """Toggle the cursor on and off."""
        # Only blink if we aren't currently typing (typewriter handles its own cursor)
        if not self.is_processing:
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

    def _typewriter_step(self, full_text, tag, index):
        """Handles the actual character emergence."""
        if index < len(full_text):
            # Insert one character at a time with the tag
            self.textbox.insert("end", full_text[index], tag)
            self.textbox.see("end")

            queue_len = len(self.msg_queue)
            dynamic_delay = self.BASE_DELAY // (queue_len + 1)
            final_delay = max(self.MIN_DELAY, min(self.MAX_DELAY, dynamic_delay))
            self.after(final_delay, lambda: self._typewriter_step(full_text, tag, index + 1))
        else:
            self._check_memory()
            self._msg_queue()
        

    def _finish_writing(self):
        """Cleanup after text is finished."""
        # self._check_memory()
        self.is_processing = False
        self.textbox.configure(state="disabled")
        # self._blink()


    def _check_memory(self):
        # TODO: cursor effect may wreck the line_count
        # Keeps the console from getting too long
        line_count = int(self.textbox.index('end-1c').split('.')[0])
        if line_count > 100:
            self.textbox.delete("1.0", "2.0")