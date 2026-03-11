import os
import customtkinter as ctk
from tkinter import Event, filedialog, ttk
import tkinter as tk
from script.data import user_db, file_path_picker
from script.openpgp import openpgp_encrypt, openpgp_decrypt
from script.asymmetry import import_keys, export_public_key, create_key_pairs
import gui.style_constants as sty

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
        self.main_frame = ctk.CTkFrame(self, corner_radius=5, fg_color=sty.main_bg)
        self.main_frame.place(relx=0, rely=0, relwidth=0.85, relheight=1.0)

        # The Tabs Container (occupies the right 15%, background is transparent!)
        self.tabs_container = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.tabs_container.place(relx=0.85, rely=0.07, relwidth=0.15, relheight=0.9)

        # ==========================================
        # BOTTOM CONSOLE SCREEN
        # ==========================================
        self.console_screen = ctk.CTkFrame(self.main_frame, height=180, corner_radius=2, fg_color=sty.console_bg,
                                        border_color="#ffffff", border_width=1,
                                        )
        self.console_screen.pack(side="bottom", fill="both", **sty.bundle_main_frame_padding, pady=(0, 12))

        # ==========================================
        # CUSTOM TITLE BAR
        # ==========================================
        self.title_bar = ctk.CTkFrame(self.main_frame, height=40, corner_radius=0, fg_color=sty.titlebar_bg, bg_color=TRANSPARENT_COLOR)
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
        self.page_setting = SettingFrame(self.main_frame, fg_color="transparent")

        # Setup basic content for pages so we can see the switch
        # ctk.CTkLabel(self.page_users, text="USERS PAGE", font=("Arial", 24)).pack(pady=50)
        # ctk.CTkLabel(self.page_encypher, text="ENCYPHER PAGE", font=("Arial", 24)).pack(pady=50)
        # ctk.CTkLabel(self.page_decypher, text="DECYPHER PAGE", font=("Arial", 24)).pack(pady=50)

        # Show the first page by default
        self.current_page = self.page_users
        self.current_page.pack(fill="both", expand=True, **sty.bundle_main_frame_padding, pady=(10, 10))

        # ==========================================
        # THE SIDE TABS (Blue Rectangles)
        # ==========================================
        self.tab_users = self.create_side_tab("Users", self.page_users, is_active=True)
        self.tab_encypher = self.create_side_tab("Encypher", self.page_encypher)
        self.tab_decypher = self.create_side_tab("Decypher", self.page_decypher)

        # spacer = ctk.CTkLabel(self.tabs_container, text="")
        # spacer.pack(expand=True, fill="both")
        self.tab_setting = self.create_side_bottom_tab("Setting", self.page_setting)

        # Keep a list so we can update their colors when clicked
        self.all_tabs = [self.tab_users, self.tab_encypher, self.tab_decypher, self.tab_setting]

    # --- TAB NAVIGATION LOGIC ---
    def create_side_tab(self, text, target_page, is_active=False):
        """Creates a custom tab button on the right side"""
        color = sty.sidebar_active if is_active else sty.sidebar_inactive
        btn = ctk.CTkButton(
            self.tabs_container,
            text=text,
            fg_color=color,
            **sty.bundle_sidebar_button
        )
        # Attach the command after creation so we can pass the button itself
        btn.configure(command=lambda: self.switch_page(target_page, btn))
        btn.pack(padx=(0, 0), pady=(0, 4), anchor="w") # Anchor west so they stick to the main frame
        return btn
    
    def create_side_bottom_tab(self, text, target_page, is_active=False):
        """Creates a custom tab button on the right bottom side"""
        color = sty.sidebar_active if is_active else sty.sidebar_inactive
        btn = ctk.CTkButton(
            self.tabs_container,
            text=text,
            fg_color=color,
            **sty.bundle_sidebar_button
        )
        # Attach the command after creation so we can pass the button itself
        btn.configure(command=lambda: self.switch_page(target_page, btn))
        btn.pack(padx=(0, 0), pady=(4, 0), anchor="sw", side=tk.BOTTOM)
        return btn

    def switch_page(self, target_page, clicked_tab):
        """Hides old page, shows new page, and updates tab colors"""
        # 1. Hide current page
        self.current_page.pack_forget()
        # 2. Show new page
        self.current_page = target_page
        self.current_page.pack(fill="both", expand=True, **sty.bundle_main_frame_padding, pady=10)

        # 3. Reset all tab colors to gray
        for tab in self.all_tabs:
            tab.configure(fg_color=sty.sidebar_inactive)
        # 4. Set clicked tab to blue
        clicked_tab.configure(fg_color=sty.sidebar_active)

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
    ''''''
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        '''
        *args: Collects all positional arguments.
        **kwargs: Collects all keyword arguments (like a=1).
        '''
        self.operation_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.operation_frame.pack(padx=(4, 4), pady=(4, 4), anchor=tk.CENTER, fill="both")
        self.operation_frame_buttons = []
        # operation_button_type = ("import", "export", "new pair") # quirk: n points at "new pair" always
        # for n in operation_button_type:
        #     button = ctk.CTkButton(self.operation_frame, text=n, width=80, command=lambda: self.user_operations(n))
        #     button.pack(padx=(6, 0), pady=(0, 4), side="right")
        #     self.operation_frame_buttons.append(button)
        self.operation_frame_buttons.append(
            ctk.CTkButton(self.operation_frame, text="export", 
                          width=80, command=lambda: self.user_operations("export"), **sty.bundle_common_button)
            )
        self.operation_frame_buttons.append(
            ctk.CTkButton(self.operation_frame, text="import", 
                          width=80, command=lambda: self.user_operations("import"), **sty.bundle_common_button)
            )
        self.operation_frame_buttons.append(
            ctk.CTkButton(self.operation_frame, text="new pair", 
                          width=80, command=lambda: self.user_operations("new pair"), **sty.bundle_common_button)
            )
        for btn in self.operation_frame_buttons:
            btn.pack(padx=(6, 0), pady=(0, 4), side="right")

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
        style.map("Treeview", background=[('selected', sty.cyan1)])
        style.map("Treeview.Heading",
            background=[('active', sty.cyan1)], # Changes to blue on hover
            foreground=[('active', 'white')])   # Keeps text white

        self.tree = ttk.Treeview(self, columns=("FP", "Name", "Status"), show='headings')
        self.tree.heading("FP", text="FP")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Status", text="Status")
        self.tree.column("FP", width=100, stretch=False)
        self.tree.column("Name", stretch=True, anchor="center")
        self.tree.column("Status", width=80, stretch=False, anchor="center")
        self.tree.pack(fill="both", expand=True, pady=(0, 0))

        self.tree_selection_fp = ""
        self.db_data = []
        self.init_table()
        '''
        Since there is no "resizable" flag,
        the common trick to stop a user from manually dragging the columns
        is to bind the mouse events that trigger resizing and tell Python to ignore them.
        '''
        self.tree.bind('<Button-1>', lambda event: 'break' if self.tree.identify_region(event.x, event.y) == "separator" else None)
        # Block the mouse cursor from changing to the 'resize' arrows
        self.tree.bind('<Motion>', lambda event: 'break' if self.tree.identify_region(event.x, event.y) == "separator" else None)

        # Triggered only on double-click
        # self.tree.bind("<Double-1>", on_tree_select)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_selected)

    def init_table(self):
        # clear all data and fetch again. # glitch: selection loss
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.db_data = user_db.list_all_table_data()
        for item in self.db_data:
            print("init row: ", item)
            # if item[0] == self.tree_selection_fp:
                # item = (self.tree_selection_fp + "?????" if i==0 else e for i, e in enumerate(item)) # generator object
                # print(item)
            self.tree.insert("", tk.END, values=item)

    def on_tree_selected(self, event: Event[ttk.Treeview]):
        tree = event.widget
        selected_item = tree.selection()
        print(selected_item)
        selected_row = tree.item(selected_item[0])["values"]
        if selected_item and selected_row[0] != self.tree_selection_fp:
            # print(tree.item(selected_item[0])["values"])
            self.tree_selection_fp = selected_row[0]
            # tree.item(selected_item[0], values=(selected_row[0], "1111" + selected_row[1], selected_row[2]))
            print("new fp", self.tree_selection_fp)
            # self.init_table()

    def update_current_user(self):
        ''''''

    def user_operations(self, button_type):
        print(button_type)
        if button_type == "import":
            file_path = file_path_picker()
            if file_path:
                ## open a dialog and get alias
                alias = self.open_input_dialog(text="Type in a number:", title="Test")
                if alias:
                    import_keys(alias, file_path=file_path)
                else:
                    print("alias can not be empty!")
        elif button_type == "export":
            rowdata = user_db.get_row_by_fp(self.tree_selection_fp)
            if not rowdata:
                print("///row-data is None///")
                return
            name = rowdata[0] + ".public_key.pem"
            file_path = file_path_picker(name)
            if file_path:
                export_public_key("", file_path)
            else:
                print()

        elif button_type == "new pair":
            ## open a dialog and get alias
            create_key_pairs("alias")
            self.init_table()

    def open_input_dialog(self, *args, **kwargs):
        ''''''
        dialog = ctk.CTkInputDialog(*args, **kwargs)
        return dialog.get_input()


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

class SettingFrame(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

if __name__ == "__main__":
    app = CypherStoneApp()
    app.mainloop()