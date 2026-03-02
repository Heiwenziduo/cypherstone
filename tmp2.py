import customtkinter as ctk
from tkinter import filedialog
import os

class CypherStoneApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("CypherStone - Asymmetric Key Manager")
        self.geometry("450x650") # Taller window to fit the layout
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Main layout configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) # User table area
        self.grid_rowconfigure(1, weight=2) # File picker area
        self.grid_rowconfigure(2, weight=0) # Buttons area

        # ==========================================
        # TOP SECTION: User / Key Selector Table
        # ==========================================
        self.table_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.table_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nsew")
        self.table_frame.grid_columnconfigure(1, weight=1)

        # Table Headers
        self.header_ready = ctk.CTkLabel(self.table_frame, text="Ready", font=ctk.CTkFont(weight="bold"), text_color="#3b8ed0", width=80)
        self.header_ready.grid(row=0, column=0, padx=2, pady=2)
        
        self.header_user = ctk.CTkLabel(self.table_frame, text="User", font=ctk.CTkFont(weight="bold"), text_color="#3b8ed0")
        self.header_user.grid(row=0, column=1, padx=2, pady=2, sticky="ew")

        # Scrollable list for users
        self.user_list = ctk.CTkScrollableFrame(self.table_frame, height=100, corner_radius=5)
        self.user_list.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.user_list.grid_columnconfigure(1, weight=1)

        # Populate with dummy data (like your sketch)
        self.add_user_row("Yes", "HAL9000", status_color="#4CAF50", user_color="#FFEB3B")
        self.add_user_row("No", "Alice_Work", status_color="gray", user_color="white")
        self.add_user_row("Yes", "Bob_Personal", status_color="#4CAF50", user_color="white")

        # ==========================================
        # MIDDLE SECTION: Large File Picker
        # ==========================================
        self.picker_frame = ctk.CTkFrame(self)
        self.picker_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.picker_frame.grid_columnconfigure(0, weight=1)
        self.picker_frame.grid_rowconfigure(1, weight=1)

        # Path Entry (Top of the picker)
        self.filepath_var = ctk.StringVar(value="No file selected...")
        self.path_entry = ctk.CTkEntry(self.picker_frame, textvariable=self.filepath_var, state="readonly", border_width=1)
        self.path_entry.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        # Large "Drop Zone" Button
        self.big_browse_btn = ctk.CTkButton(
            self.picker_frame, 
            text="(Click to open file picker)", 
            font=ctk.CTkFont(size=16),
            fg_color="#333333", 
            hover_color="#444444",
            command=self.browse_file
        )
        self.big_browse_btn.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # ==========================================
        # BOTTOM SECTION: Action Buttons
        # ==========================================
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="ew")
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)

        # Two large buttons
        self.btn_left = ctk.CTkButton(self.button_frame, text="Encrypt for User", height=50, font=ctk.CTkFont(size=14, weight="bold"))
        self.btn_left.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        self.btn_right = ctk.CTkButton(self.button_frame, text="Decrypt File", height=50, font=ctk.CTkFont(size=14, weight="bold"), fg_color="#2b2b2b", hover_color="#3b3b3b")
        self.btn_right.grid(row=0, column=1, padx=(10, 0), sticky="ew")

    def add_user_row(self, status, username, status_color="white", user_color="white"):
        """Helper function to add rows to our custom 'table'"""
        row_index = len(self.user_list.winfo_children()) // 2  # Calculate current row
        
        status_lbl = ctk.CTkLabel(self.user_list, text=status, text_color=status_color, width=80)
        status_lbl.grid(row=row_index, column=0, pady=2)
        
        user_lbl = ctk.CTkLabel(self.user_list, text=username, text_color=user_color, anchor="w")
        user_lbl.grid(row=row_index, column=1, pady=2, sticky="ew")

    def browse_file(self):
        """Opens standard Windows file explorer"""
        filename = filedialog.askopenfilename(
            title="Select a file for CypherStone",
            initialdir=os.path.expanduser("~/Documents")
        )
        if filename:
            self.filepath_var.set(filename)
            self.big_browse_btn.configure(text=f"Selected:\n{os.path.basename(filename)}")

if __name__ == "__main__":
    app = CypherStoneApp()
    app.mainloop()