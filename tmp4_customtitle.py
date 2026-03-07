import os

import customtkinter as ctk
from tkinter import filedialog, ttk
import tkinter as tk
from script.data import user_db
from script.openpgp import openpgp_encrypt, openpgp_decrypt

class CypherStoneApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. REMOVE STANDARD TITLE BAR & SET TRANSPARENCY
        self.overrideredirect(True) # Removes the Windows border/title bar completely
        self.geometry("400x600")

        # This is the magic! We pick a color (#000001 is almost black) and tell Windows to make it invisible.
        TRANSPARENT_COLOR = "#000001"
        self.configure(fg_color=TRANSPARENT_COLOR)
        self.wm_attributes("-transparentcolor", TRANSPARENT_COLOR)

        # Variables for custom window dragging
        self._drag_x = 0
        self._drag_y = 0

        # ==========================================
        # MAIN LAYOUT AREAS
        # ==========================================
        # The Main Application Box (occupies the left 85% of the width)
        self.main_frame = ctk.CTkFrame(self, corner_radius=5, fg_color="#4d4d4d")
        self.main_frame.place(relx=0, rely=0, relwidth=0.85, relheight=1.0)

        # The Tabs Container (occupies the right 15%, background is transparent!)
        self.tabs_container = ctk.CTkFrame(self, corner_radius=0, fg_color="#512dbe")
        self.tabs_container.place(relx=0.84, rely=0.07, relwidth=0.15, relheight=0.9)

        # ==========================================
        # CUSTOM TITLE BAR
        # ==========================================
        self.title_bar = ctk.CTkFrame(self.main_frame, height=40, corner_radius=15, fg_color="#ffa6ff", bg_color=TRANSPARENT_COLOR)
        self.title_bar.pack(fill="x", side="top", pady=(0, 0))

        # Bind the dragging events to the title bar
        self.title_bar.bind("<ButtonPress-1>", self.start_drag)
        self.title_bar.bind("<B1-Motion>", self.do_drag)

        # App Title Text
        self.title_label = ctk.CTkLabel(self.title_bar, text="CypherStone", font=ctk.CTkFont(weight="bold"), text_color="#1B8BFB")
        self.title_label.pack(side="left", padx=15)
        self.title_label.bind("<ButtonPress-1>", self.start_drag) # Let user drag by clicking the text too
        self.title_label.bind("<B1-Motion>", self.do_drag)

        # The Red-Bordered Window Controls (Close & Minimize)
        self.close_btn = ctk.CTkButton(
            self.title_bar, text="X", width=24, height=24, corner_radius=12,
            fg_color="transparent", border_width=2, border_color="#ff5f56", text_color="#ff5f56",
            hover_color="#5c2022", command=self.destroy
        )
        self.close_btn.pack(side="right", padx=(5, 10), pady=8)

        self.min_btn = ctk.CTkButton(
            self.title_bar, text="—", width=24, height=24, corner_radius=12,
            fg_color="transparent", border_width=2, border_color="#ffbd2e", text_color="#ffbd2e",
            hover_color="#594314", command=self.minimize_window
        )
        # self.min_btn.pack(side="right", padx=0, pady=8)

        # ==========================================
        # CONTENT FRAMES (The pages to switch between)
        # ==========================================
        # We create frames for each page and put them in the same spot
        self.page_users = UserFrame(self.main_frame, fg_color="transparent")
        self.page_encypher = EncypherFrame(self.main_frame, fg_color="transparent")
        self.page_decypher = DecypherFrame(self.main_frame, fg_color="transparent")

        # Setup basic content for pages so we can see the switch
        # ctk.CTkLabel(self.page_users, text="USERS PAGE", font=("Arial", 24)).pack(pady=50)
        ctk.CTkLabel(self.page_encypher, text="ENCYPHER PAGE", font=("Arial", 24)).pack(pady=50)
        ctk.CTkLabel(self.page_decypher, text="DECYPHER PAGE", font=("Arial", 24)).pack(pady=50)

        # Show the first page by default
        self.current_page = self.page_users
        self.current_page.pack(fill="both", expand=True, padx=15, pady=(10, 20))

        # ==========================================
        # THE SIDE TABS (Blue Rectangles)
        # ==========================================
        self.tab_users = self.create_side_tab("Users", self.page_users, is_active=True)
        self.tab_encypher = self.create_side_tab("Encypher", self.page_encypher)
        self.tab_decypher = self.create_side_tab("Decypher", self.page_decypher)

        # Keep a list so we can update their colors when clicked
        self.all_tabs = [self.tab_users, self.tab_encypher, self.tab_decypher]

    # --- TAB NAVIGATION LOGIC ---
    def create_side_tab(self, text, target_page, is_active=False):
        """Creates a custom tab button on the right side"""
        color = "#1f6aa5" if is_active else "#333333" # Blue if active, dark gray if not

        btn = ctk.CTkButton(
            self.tabs_container,
            text=text,
            width=60,
            height=60,
            corner_radius=0, # Square rectangles as in your draft
            fg_color=color,
            hover_color="#144870",
            border_width=3,
            border_color="#09E1EC",
        )
        # Attach the command after creation so we can pass the button itself
        btn.configure(command=lambda: self.switch_page(target_page, btn))
        btn.pack(padx=(0, 0), pady=(0, 4), anchor="w") # Anchor west so they stick to the main frame
        return btn
    
    def create_side_bottom_tab(self, text, target_page, is_active=False):
        """Creates a custom tab button on the right side"""
        color = "#1f6aa5" if is_active else "#333333" # Blue if active, dark gray if not

        btn = ctk.CTkButton(
            self.tabs_container,
            text=text,
            width=60,
            height=60,
            corner_radius=0, # Square rectangles as in your draft
            fg_color=color,
            hover_color="#144870",
            border_width=3,
            border_color="#09E1EC",
        )
        # Attach the command after creation so we can pass the button itself
        btn.configure(command=lambda: self.switch_page(target_page, btn))
        btn.pack(padx=(0, 0), pady=(0, 4), anchor="w") # Anchor west so they stick to the main frame
        return btn

    def switch_page(self, target_page, clicked_tab):
        """Hides old page, shows new page, and updates tab colors"""
        # 1. Hide current page
        self.current_page.pack_forget()
        # 2. Show new page
        self.current_page = target_page
        self.current_page.pack(fill="both", expand=True, padx=20, pady=10)

        # 3. Reset all tab colors to gray
        for tab in self.all_tabs:
            tab.configure(fg_color="#333333")
        # 4. Set clicked tab to blue
        clicked_tab.configure(fg_color="#1f6aa5")

    # --- CUSTOM DRAGGING LOGIC ---
    def start_drag(self, event):
        """Records the mouse position when you click the title bar"""
        self._drag_x = event.x
        self._drag_y = event.y

    def do_drag(self, event):
        """Calculates how far the mouse moved and moves the window"""
        x = self.winfo_x() + (event.x - self._drag_x)
        y = self.winfo_y() + (event.y - self._drag_y)
        self.geometry(f"+{x}+{y}")

    def minimize_window(self):
        """Custom minimize function since we removed the OS one"""
        self.state('iconic')

class UserFrame(ctk.CTkFrame):
    '''
        *args: Collects all positional arguments.
        **kwargs: Collects all keyword arguments (like a=1).
    '''
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        # 1. Create a Style object
        style = ttk.Style()
        # 2. Pick a theme that allows color changes (like 'clam' or 'default')
        style.theme_use("clam")
        # 3. Configure Treeview colors to match CTk Dark Theme
        # Background: #242424, Foreground: white, Field (empty space): #242424
        style.configure("Treeview",
                        background="#2b2b2b",
                        foreground="white",
                        fieldbackground="#2b2b2b",
                        bordercolor="#2b2b2b",
                        borderwidth=0)
        # Configure the Headers
        style.configure("Treeview.Heading",
                        background="#333333",
                        foreground="white",
                        relief="flat")
        # Change selection color
        style.map("Treeview", background=[('selected', '#1f538d')])
        style.map("Treeview.Heading",
            background=[('active', '#1f538d')], # Changes to blue on hover
            foreground=[('active', 'white')])   # Keeps text white

        self.tree = ttk.Treeview(self, columns=("FP", "Name", "Status"), show='headings')
        self.tree.heading("FP", text="FP")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Status", text="Status")
        self.tree.column("FP", width=100, stretch=False)
        self.tree.column("Name", stretch=True, anchor="center")
        self.tree.column("Status", width=80, stretch=False, anchor="center")
        self.tree.pack(fill="both", expand=True)
        self.init_table(data=user_db.list_all_table_data())
        '''
        Since there is no "resizable" flag,
        the common trick to stop a user from manually dragging the columns
        is to bind the mouse events that trigger resizing and tell Python to ignore them.
        '''
        self.tree.bind('<Button-1>', lambda event: 'break' if self.tree.identify_region(event.x, event.y) == "separator" else None)
        # Block the mouse cursor from changing to the 'resize' arrows
        self.tree.bind('<Motion>', lambda event: 'break' if self.tree.identify_region(event.x, event.y) == "separator" else None)
    
    def init_table(self, data):
        self.tree.delete()
        for item in data:
            self.tree.insert("", tk.END, values=item)

class EncypherFrame(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        ## user selector
        # self.user_selector = ctk.

        self.process_path = ctk.StringVar(value="No file selected...")
        self.result_path = ctk.StringVar(value="")

        self.process_file_entry = ctk.CTkButton(
            self, 
            textvariable=self.process_path, 
            fg_color="#333333", 
            hover_color="#444444",
            command=lambda: self.browse_file(self.process_path)
        )
        self.process_file_entry.pack(padx=10, pady=10, anchor="s")

        self.result_file_entry = ctk.CTkButton(
            self, 
            textvariable=self.result_path, 
            fg_color="#333333", 
            hover_color="#444444",
            command=lambda: self.browse_file(self.result_path)
        )
        self.result_file_entry.pack(padx=10, pady=10, anchor="s")

        self.process_button = ctk.CTkButton(self, text="Process", command=self.encrypt_file)
        self.process_button.pack(padx=10, pady=10, anchor="s")

    def browse_file(self, text_var: ctk.StringVar):
        filename = filedialog.askopenfilename(
            title="Select a file for CypherStone",
            # initialdir=os.path.expanduser("~/Documents")
        )
        if filename:
            text_var.set(filename)

    def encrypt_file(self):
        print("encrypt: ", self.process_path.get(), " ---> ", self.result_path.get())
        # openpgp_encrypt()

class DecypherFrame(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

if __name__ == "__main__":
    app = CypherStoneApp()
    app.mainloop()