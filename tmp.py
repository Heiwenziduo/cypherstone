import customtkinter as ctk
from tkinter import filedialog, messagebox
import tomllib
from pathlib import Path
import os

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

        # Window Setup
        self.app_version = get_app_version()
        self.title(f"CypherStone v{self.app_version}")
        self.geometry("500x400")
        
        # Set modern theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Configure Grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Main Container (The "Card")
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

        self.sub_label = ctk.CTkLabel(
            self.main_frame, 
            text="Secure local file encryption", 
            font=ctk.CTkFont(size=13),
            text_color="gray"
        )
        self.sub_label.pack(pady=(0, 20))

        # Selected File Display (A nice entry box)
        self.file_path_var = ctk.StringVar(value="No file selected...")
        self.file_entry = ctk.CTkEntry(
            self.main_frame, 
            textvariable=self.file_path_var, 
            width=350,
            state="readonly",
            fg_color="transparent"
        )
        self.file_entry.pack(pady=10, padx=20)

        # Buttons Frame
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(pady=20)

        self.browse_btn = ctk.CTkButton(
            self.button_frame, 
            text="Select File", 
            command=self.browse_file,
            fg_color="#3b3b3b",
            hover_color="#4b4b4b"
        )
        self.browse_btn.grid(row=0, column=0, padx=10)

        self.action_btn = ctk.CTkButton(
            self.button_frame, 
            text="Process File", 
            command=self.process_file,
            state="disabled" # Disabled until a file is picked
        )
        self.action_btn.grid(row=0, column=1, padx=10)

        # Status Footer
        self.status_label = ctk.CTkLabel(self.main_frame, text="Ready", font=ctk.CTkFont(size=11))
        self.status_label.pack(side="bottom", pady=10)

    def browse_file(self):
        """Opens standard Windows file explorer"""
        filename = filedialog.askopenfilename(
            title="Select a file to CypherStone",
            initialdir=os.path.expanduser("~/Documents")
        )
        
        if filename:
            self.file_path_var.set(filename)
            self.action_btn.configure(state="normal")
            self.status_label.configure(text=f"Selected: {os.path.basename(filename)}")

    def process_file(self):
        """Placeholder for our PGP logic"""
        file_path = self.file_path_var.get()
        messagebox.showinfo("CypherStone", f"Ready to encrypt/decrypt:\n{file_path}")

if __name__ == "__main__":
    app = CypherStoneApp()
    app.mainloop()