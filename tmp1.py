import customtkinter as ctk
from tkinter import filedialog, messagebox
import tomllib
from pathlib import Path
import os
import threading
import time
import pyperclip
from cryptography.fernet import Fernet

# --- UTILS ---
def get_app_version():
    """Reads version from pyproject.toml"""
    try:
        path = Path("pyproject.toml")
        if path.exists():
            with open(path, "rb") as f:
                data = tomllib.load(f)
                return data.get("project", {}).get("version", "1.0.0")
    except Exception:
        pass
    return "1.0.0"

# --- MAIN APP ---
class CypherStoneApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Encryption Setup (Symmetric for now)
        self.key_path = Path("cypher.key")
        self.key = self.load_or_generate_key()
        self.fernet = Fernet(self.key)

        # Window Setup
        self.app_version = get_app_version()
        self.title(f"CypherStone v{self.app_version}")
        self.geometry("500x500") # Made it taller for new features
        
        # Set modern theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # UI State
        self.clipboard_monitoring = False

        # Configure Grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Main Container
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.grid(row=0, column=0, padx=30, pady=30, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Header
        self.label = ctk.CTkLabel(
            self.main_frame, 
            text="CYPHERSTONE", 
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold")
        )
        self.label.pack(pady=(30, 5))

        # --- SECTION: FILE ENCRYPTION ---
        self.file_label = ctk.CTkLabel(self.main_frame, text="FILE SECURITY", font=ctk.CTkFont(size=12, weight="bold"), text_color="#3b8ed0")
        self.file_label.pack(pady=(10, 5))

        self.file_path_var = ctk.StringVar(value="No file selected...")
        self.file_entry = ctk.CTkEntry(self.main_frame, textvariable=self.file_path_var, width=350, state="readonly", fg_color="transparent")
        self.file_entry.pack(pady=5, padx=20)

        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(pady=10)

        self.browse_btn = ctk.CTkButton(self.button_frame, text="Browse", width=100, command=self.browse_file, fg_color="#3b3b3b")
        self.browse_btn.grid(row=0, column=0, padx=5)

        self.action_btn = ctk.CTkButton(self.button_frame, text="Encrypt File", width=100, command=self.process_file, state="disabled")
        self.action_btn.grid(row=0, column=1, padx=5)

        # --- SECTION: CLIPBOARD SHIELD ---
        self.sep = ctk.CTkLabel(self.main_frame, text="─" * 40, text_color="gray30")
        self.sep.pack(pady=10)

        self.clip_label = ctk.CTkLabel(self.main_frame, text="CLIPBOARD SHIELD", font=ctk.CTkFont(size=12, weight="bold"), text_color="#3b8ed0")
        self.clip_label.pack(pady=(0, 5))

        self.monitor_switch = ctk.CTkSwitch(
            self.main_frame, 
            text="Auto-Encrypt Copied Text", 
            command=self.toggle_clipboard_monitor
        )
        self.monitor_switch.pack(pady=10)

        # Status Footer
        self.status_label = ctk.CTkLabel(self.main_frame, text="Ready", font=ctk.CTkFont(size=11))
        self.status_label.pack(side="bottom", pady=10)

    def load_or_generate_key(self):
        """Loads existing key or creates a new one for encryption"""
        if self.key_path.exists():
            return self.key_path.read_bytes()
        else:
            new_key = Fernet.generate_key()
            self.key_path.write_bytes(new_key)
            return new_key

    def browse_file(self):
        filename = filedialog.askopenfilename(title="Select a file", initialdir=os.path.expanduser("~/Documents"))
        if filename:
            self.file_path_var.set(filename)
            self.action_btn.configure(state="normal")
            self.status_label.configure(text=f"Selected: {os.path.basename(filename)}")

    def process_file(self):
        messagebox.showinfo("CypherStone", "File encryption logic would run here!")

    def toggle_clipboard_monitor(self):
        """Starts or stops the clipboard monitoring thread"""
        self.clipboard_monitoring = self.monitor_switch.get() == 1
        if self.clipboard_monitoring:
            self.status_label.configure(text="Clipboard Shield: ACTIVE", text_color="#4CAF50")
            # Start background thread
            threading.Thread(target=self.monitor_clipboard_loop, daemon=True).start()
        else:
            self.status_label.configure(text="Clipboard Shield: INACTIVE", text_color="white")

    def monitor_clipboard_loop(self):
        """Background loop to catch clipboard changes"""
        last_clip = pyperclip.paste()
        
        while self.clipboard_monitoring:
            current_clip = pyperclip.paste()
            
            # If the clipboard content changed and isn't empty
            if current_clip != last_clip and current_clip.strip():
                # We check if it's already encrypted to avoid infinite loops
                if not current_clip.startswith("CS_ENC:"):
                    try:
                        encrypted = self.fernet.encrypt(current_clip.encode()).decode()
                        final_output = f"CS_ENC:{encrypted}"
                        pyperclip.copy(final_output)
                        last_clip = final_output
                        print(f"Intercepted and encrypted clipboard content.")
                    except Exception as e:
                        print(f"Encryption error: {e}")
            
            time.sleep(0.5) # Check every half second

if __name__ == "__main__":
    app = CypherStoneApp()
    app.mainloop()