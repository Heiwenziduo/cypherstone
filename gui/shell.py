import customtkinter as ctk

class Shell(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # 1. Hide the default title bar
        self.overrideredirect(True)
        self.geometry("600x400")

        # 2. Create the Custom Title Bar
        self.title_bar = ctk.CTkFrame(self, height=40, corner_radius=0, fg_color="#222222")
        self.title_bar.pack(side="top", fill="x")

        # Title Label
        self.title_label = ctk.CTkLabel(self.title_bar, text="My Custom App", font=("Arial", 14))
        self.title_label.pack(side="left", padx=10)

        # Close Button
        self.close_button = ctk.CTkButton(self.title_bar, text="✕", width=40, height=40, 
                                        fg_color="transparent", hover_color="red", 
                                        command=self.destroy)
        self.close_button.pack(side="right")

        # Minimize Button
        self.min_button = ctk.CTkButton(self.title_bar, text="—", width=40, height=40, 
                                        fg_color="transparent", 
                                        command=self.minimize_window)
        self.min_button.pack(side="right")

        # 3. Bind dragging events
        self.title_bar.bind("<Button-1>", self.get_pos)
        self.title_bar.bind("<B1-Motion>", self.move_window)

    def get_pos(self, event):
        self.xwin = event.x
        self.ywin = event.y

    def move_window(self, event):
        # Calculate new position
        new_x = self.winfo_x() + (event.x - self.xwin)
        new_y = self.winfo_y() + (event.y - self.ywin)
        self.geometry(f"+{new_x}+{new_y}")

    def minimize_window(self):
        self.update_idletasks()
        self.withdraw()
        self.overrideredirect(False)
        self.state('iconic')
        self.bind("<FocusIn>", self.on_restore)

    def on_restore(self, event):
        self.overrideredirect(True)
        self.deiconify()
