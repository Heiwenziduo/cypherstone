import customtkinter as ctk
from tkinter import filedialog
import gui.style_constants as sty

class EncypherFrame(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        ## user selector
        # self.user_selector = ctk.

        self.process_path = ctk.StringVar(value="No file selected...")
        self.result_path = ctk.StringVar(value="")

        self.label_1 = ctk.CTkLabel(self, text="Encrypt file path:", text_color="#ffffff", anchor="w")
        self.label_1.pack(fill="x", expand=True, side="top", padx=15, pady=(10, 0))
        self.process_file_entry = ctk.CTkButton(
            self, 
            textvariable=self.process_path, 
            fg_color="#333333", 
            hover_color="#444444",
            command=lambda: self.browse_file(self.process_path)
        )
        self.process_file_entry.pack(expand=True, fill="x", padx=10, pady=10, anchor="s")

        self.label_2 = ctk.CTkLabel(self, text="Output path:", text_color="#ffffff", anchor="w")
        self.label_2.pack(fill="x", expand=True, side="top", padx=15, pady=(10, 0))
        self.result_file_entry = ctk.CTkButton(
            self, 
            textvariable=self.result_path, 
            fg_color="#333333", 
            hover_color="#444444",
            command=lambda: self.browse_file(self.result_path)
        )
        self.result_file_entry.pack(expand=True, fill="x", padx=10, pady=10, anchor="s")

        self.process_button = ctk.CTkButton(self, text="Process", command=self.process_encrypt_file, **sty.bundle_common_button)
        self.process_button.pack(padx=10, pady=30, anchor="s")

    def browse_file(self, text_var: ctk.StringVar):
        filename = filedialog.askopenfilename(
            title="Select a file for CypherStone",
            # initialdir=os.path.expanduser("~/Documents")
        )
        if filename:
            text_var.set(filename)

    def process_encrypt_file(self):
        print("encrypt: ", self.process_path.get(), " ---> ", self.result_path.get())
        # openpgp_encrypt()
