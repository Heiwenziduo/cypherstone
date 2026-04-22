import tkinter as tk
from tkinter import Event, ttk
import customtkinter as ctk
import gui.style_constants as sty
import script.data as cdata
from gui.dialog import alias_dialog
from gui.console_screen import cys_console
from script.asymmetry import import_public_key, query_export_public_key, create_key_pairs

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
        self.db_data = cdata.user_db.list_all_table_data()
        for item in self.db_data:
            # print("init row: ", item)
            # if item[0] == cdata._current_user_fp:
                # item = (cdata._current_user_fp + "?????" if i==0 else e for i, e in enumerate(item)) # generator object
                # print(item)
            self.tree.insert("", tk.END, values=item)

    def on_tree_selected(self, event: Event[ttk.Treeview]):
        tree = event.widget
        selected_item = tree.selection()
        if selected_item:
            selected_row = tree.item(selected_item[0])["values"]
            if selected_row and selected_row[0] != cdata._current_user_fp:
                # print(tree.item(selected_item[0])["values"])
                cdata._current_user_fp = selected_row[0]
                # tree.item(selected_item[0], values=(selected_row[0], "1111" + selected_row[1], selected_row[2]))
                print("new fp", cdata._current_user_fp)
                # self.init_table()

    def update_current_user(self):
        ''''''

    def user_operations(self, button_type):
        print(button_type)
        if button_type == "import":
            file_path = cdata.file_path_picker()
            if file_path:
                alias = alias_dialog(self)
                if alias:
                    # TODO: maybe analyze first, then type alias
                    import_public_key(alias, file_path=file_path)
                    self.init_table()
                # else:
                #     print("alias can not be empty!")

        elif button_type == "export":
            if cdata._current_user_fp:
                query_export_public_key(cdata._current_user_fp)
            else:
                print("no current user to export!")

        elif button_type == "new pair":
            alias = alias_dialog(self)
            if alias:
                create_key_pairs(alias)
                self.init_table()
                cys_console("New pair created: " + alias)
            # else:
            #     print("alias can not be empty!")
