import os
import customtkinter as ctk
from gui.shell import Shell
from script.data import update_json, json_data
from script.metadata import get_app_version
from tkinter import filedialog, ttk
import tkinter as tk
from script.data import user_db

def init_gui():
  ctk.set_appearance_mode("dark")
  app = App()
  app.title(f"CypherStone v{get_app_version()}")
  app.geometry("320x520")
  app.resizable(False, False)
  app.mainloop()

##
class App(ctk.CTk):
  def __init__(self):
    super().__init__()

    self.rowconfigure((0, 2), weight=1)
    self.columnconfigure((0, 1), weight=1)

    self.user_frame = UserFrame(self)
    self.user_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    self.configure_frame = ConfigureFrame(self)
    self.configure_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="nsew")
    self.filepicker_frame = FilepickerFrame(self)
    self.filepicker_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="nsew")

    self.button = ctk.CTkButton(self, text="Encrypt", command=self.button_encrypt)
    self.button.grid(row=999, column=0, pady=(0, 10))
    self.button2 = ctk.CTkButton(self, text="Decrypt", command=self.button_decrypt)
    self.button2.grid(row=999, column=1, pady=(0, 10))

  def button_encrypt(self):
    print("Encrypt ", self.configure_frame.get_setting(), self.filepicker_frame.file_path_var.get())

  def button_decrypt(self):
    print("Decrypt ", self.configure_frame.get_setting())

##
class UserFrame(ctk.CTkFrame):
  def __init__(self, master):
    super().__init__(master)
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
    self.tree.column("Name", stretch=False, anchor="center")
    self.tree.column("Status", width=80, stretch=False, anchor="center")
    self.tree.pack(fill="both", expand=True)

    self.init_table(data=user_db.list_all_table_data())

  def init_table(self, data):
    self.tree.delete()
    for item in data:
        self.tree.insert("", tk.END, values=item)

##
class ConfigureFrame(ctk.CTkFrame):
  def __init__(self, master):
    super().__init__(master)
    # self.title = ctk.CTkLabel(self, text="Configure", fg_color="gray30", corner_radius=6, text_color="white")
    # self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

    # self.checkbox_1 = ctk.CTkCheckBox(self, text="checkbox 1")
    # self.checkbox_1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
    # self.checkbox_2 = ctk.CTkCheckBox(self, text="checkbox 2")
    # self.checkbox_2.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")

    self.checkboxs = {}
    for index, value in enumerate(json_data):
      checkbox = ctk.CTkCheckBox(self, text=value, command=self.update_setting)
      checkbox.grid(row=index + 1, padx=10, pady=(0, 10), sticky="w")
      if json_data[value]==1:
        checkbox.select()
        # print("select checkbox", index+1)
      if index==0:
        checkbox.grid(pady=(10, 10)) # overwrite above
      self.checkboxs[value] = checkbox

  def update_setting(self):
    setting = self.get_setting()
    update_json(setting)

  def get_setting(self):
    setting_data = {}
    for k in self.checkboxs:
      setting_data[k] = self.checkboxs[k].get()
    return setting_data

##
class FilepickerFrame(ctk.CTkFrame):
  def __init__(self, master):
    super().__init__(master)
    self.columnconfigure(0, weight=1)
    self.file_path_var = ctk.StringVar(value="No file selected...")
    self.file_entry = ctk.CTkButton(
        self, 
        textvariable=self.file_path_var, 
        fg_color="#333333", 
        hover_color="#444444",
        command=self.browse_file
    )
    self.file_entry.grid(padx=10, pady=10, sticky="nsew")

  def browse_file(self):
    filename = filedialog.askopenfilename(
      title="Select a file for CypherStone",
      # initialdir=os.path.expanduser("~/Documents")
    )
    if filename:
      self.file_path_var.set(filename)
      # self.big_browse_btn.configure(text=f"Selected:\n{os.path.basename(filename)}")

##
# class OperationFrame(ctk.CTkFrame):
#     def __init__(self, master):
#         super().__init__(master)

#         self.button = ctk.CTkButton(self, text="my button")
