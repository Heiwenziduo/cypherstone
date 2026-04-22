import customtkinter as ctk
import gui.style_constants as sty
from script.data import file_path_picker
from gui.console_screen import cys_console
from script.openpgp import _suffix

class DecypherFrame(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.input_path = ctk.StringVar(value="No file selected...")
        self.output_path = ctk.StringVar(value="")

        self.label_1 = ctk.CTkLabel(self, text="Decrypt file path:", text_color="#ffffff", anchor="w")
        self.label_1.pack(fill="x", expand=True, side="top", padx=15, pady=(10, 0))
        self.input_file_button = ctk.CTkButton(
            self, 
            textvariable=self.input_path, 
            command=self.input_file,
            **sty.bundle_formrow_button
        )
        self.input_file_button.pack(expand=True, fill="x", padx=10, pady=10, anchor="s")
        # ==========================================
        # ==========================================

        self.label_2 = ctk.CTkLabel(self, text="Output path:", text_color="#ffffff", anchor="w")
        self.label_2.pack(fill="x", expand=True, side="top", padx=15, pady=(10, 0))
        self.output_file_button = ctk.CTkButton(
            self, 
            textvariable=self.output_path, 
            command=self.output_file,
            anchor="w",
            **sty.bundle_formrow_button,
            state="disabled"
        )
        self.output_file_button.pack(expand=True, fill="x", padx=10, pady=10, anchor="s")
        # ==========================================
        # ==========================================

        self.process_button = ctk.CTkButton(
            self,
            text="Decrypt", 
            command=self.process_decrypt_file, 
            **sty.bundle_common_button,
            state="disabled"
        )
        self.process_button.pack(padx=10, pady=30, anchor="s")

    def input_file(self):
        filename = file_path_picker()
        if filename:
            self.input_path.set(filename)
            self.input_file_button.configure(anchor="w")
            self.output_file_button.configure(state="normal")
            self.process_button.configure(state="normal")
            self.output_path.set(filename.removesuffix(_suffix))

    def output_file(self):
        ''''''
        filename = file_path_picker(self.output_path.get())
        if filename:
            self.output_path.set(filename)

    def process_decrypt_file(self):
        cys_console("Success, decrypted file at: " + self.output_path.get())
        return