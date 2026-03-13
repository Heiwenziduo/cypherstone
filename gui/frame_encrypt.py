import customtkinter as ctk
from tkinter import filedialog
from gui.console_screen import cys_console
import gui.style_constants as sty
from script.asymmetry import get_public_key_by_fp
from script.data import current_user_fp, file_path_picker
from script.openpgp import _suffix, openpgp_encrypt

class EncypherFrame(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        ## user selector
        # self.user_selector = ctk.

        self.input_path = ctk.StringVar(value="No file selected...")
        self.output_path = ctk.StringVar(value="")

        self.label_1 = ctk.CTkLabel(self, text="Encrypt file path:", text_color="#ffffff", anchor="w")
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

        self.process_button = ctk.CTkButton(
            self,
            text="Encrypt", 
            command=self.process_encrypt_file, 
            **sty.bundle_common_button,
            state="disabled"
        )
        self.process_button.pack(padx=10, pady=30, anchor="s")

    # def browse_file(self, text_var: ctk.StringVar):
    #     filename = file_path_picker()
    #     if filename:
    #         text_var.set(filename)

    def input_file(self):
        filename = file_path_picker()
        if filename:
            self.input_path.set(filename)
            self.input_file_button.configure(anchor="w")
            self.output_file_button.configure(state="normal")
            self.process_button.configure(state="normal")
            # TODO: only change file name but remember the folder path
            # if not self.output_path.get():
            self.output_path.set(filename + _suffix)

    def output_file(self):
        ''''''
        filename = file_path_picker(self.output_path.get())
        if filename:
            self.output_path.set(filename)

    def process_encrypt_file(self):
        # cys_console("Start encrypting...")
        self.process_button.configure(state="disabled")
        self.after(200, lambda: self.process_button.configure(state="normal"))

        # print("encrypt: ", self.input_path.get(), " ---> ", self.output_path.get())
        public_key = get_public_key_by_fp(current_user_fp())
        if public_key:
            openpgp_encrypt(public_key, self.input_path.get())
            cys_console("Success, encrypted file at: " + self.output_path.get())
        # openpgp_encrypt()
        # success = True
        # if success:
        #     self.output_file_button.configure(state="disabled")
        #     self.process_button.configure(state="disabled")
