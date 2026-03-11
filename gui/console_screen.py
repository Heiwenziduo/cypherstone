import customtkinter as ctk

def cys_console(*text):
    '''log something on the console screen'''
    print("log: ", *text)

class ConsoleScreen(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
