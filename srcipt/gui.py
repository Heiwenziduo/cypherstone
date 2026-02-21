import customtkinter
from srcipt.metadata import get_app_version
# from metadata import app_version # not work, missing module (?)

def init_gui():
  app = App()
  app.mainloop()

##
class App(customtkinter.CTk):
  def __init__(self):
    super().__init__()
    customtkinter.set_appearance_mode("dark")

    self.app_version = get_app_version()
    self.title(f"CypherStone v{self.app_version}")
    self.geometry("320x520")
    # self.rowconfigure(0, weight=1)
    self.columnconfigure((0, 1), weight=1)

    self.configure_frame = ConfigureFrame(self)
    self.configure_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 10), sticky="nsew")

    button = customtkinter.CTkButton(self, text="encrypt", command=self.button_callbck)
    button.grid(row=999, column=0)
    button2 = customtkinter.CTkButton(self, text="decrypt", command=self.button_callbck)
    button2.grid(row=999, column=1)
    # customtkinter.CTkButton(self, text="bbb").grid(row=999, column=1)
    # customtkinter.CTkCheckBox(self, text="1").grid(row=0, column=0, sticky="ew")
    # customtkinter.CTkCheckBox(self, text="2").grid(row=1, column=0, sticky="ew")

  def button_callbck(self):
    print("button ", self.configure_frame.get())

##
class ConfigureFrame(customtkinter.CTkFrame):
  box_list = ["deepclean", "check2"]
  def __init__(self, master):
    super().__init__(master)
    self.title = customtkinter.CTkLabel(self, text="Configure", fg_color="gray30", corner_radius=6, text_color="white")
    self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

    # self.checkbox_1 = customtkinter.CTkCheckBox(self, text="checkbox 1")
    # self.checkbox_1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
    # self.checkbox_2 = customtkinter.CTkCheckBox(self, text="checkbox 2")
    # self.checkbox_2.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")

    for index, value in enumerate(self.box_list):
      checkbox = customtkinter.CTkCheckBox(self, text=value)
      checkbox.grid(row=index + 1, padx=10, pady=(10, 0), sticky="w")
      setattr(self, value, checkbox)

  def get(self):
    result = []
    for index, value in enumerate(self.box_list):
      checkbox = getattr(self, value)
      if checkbox.get() == 1:
        result.append(checkbox.cget("text"))
    return result

##
# class OperationFrame(customtkinter.CTkFrame):
#     def __init__(self, master):
#         super().__init__(master)

#         self.button = customtkinter.CTkButton(self, text="my button")
