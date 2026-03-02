import os
import customtkinter as ctk
from gui.shell import Shell
from srcipt.metadata import get_app_version
from tkinter import filedialog

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
    print("Encrypt ", self.configure_frame.get(), self.filepicker_frame.file_path_var.get())

  def button_decrypt(self):
    print("Decrypt ", self.configure_frame.get())

##
class UserFrame(ctk.CTkFrame):
  def __init__(self, master):
    super().__init__(master)

##
class ConfigureFrame(ctk.CTkFrame):
  box_list = ["deepclean", "check2"]
  def __init__(self, master):
    super().__init__(master)
    # self.title = ctk.CTkLabel(self, text="Configure", fg_color="gray30", corner_radius=6, text_color="white")
    # self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

    # self.checkbox_1 = ctk.CTkCheckBox(self, text="checkbox 1")
    # self.checkbox_1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
    # self.checkbox_2 = ctk.CTkCheckBox(self, text="checkbox 2")
    # self.checkbox_2.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")

    for index, value in enumerate(self.box_list):
      checkbox = ctk.CTkCheckBox(self, text=value)
      checkbox.grid(row=index + 1, padx=10, pady=(0, 10), sticky="w")
      if index==0:
        checkbox.grid(pady=(10, 10)) # overwrite above
      setattr(self, value, checkbox)

  def get(self):
    result = []
    for index, value in enumerate(self.box_list):
      checkbox = getattr(self, value)
      if checkbox.get() == 1:
        result.append(checkbox.cget("text"))
    return result

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
      initialdir=os.path.expanduser("~/Documents")
    )
    if filename:
      self.file_path_var.set(filename)
      # self.big_browse_btn.configure(text=f"Selected:\n{os.path.basename(filename)}")

##
# class OperationFrame(ctk.CTkFrame):
#     def __init__(self, master):
#         super().__init__(master)

#         self.button = ctk.CTkButton(self, text="my button")
