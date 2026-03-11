import customtkinter as ctk
import gui.style_constants as sty
from gui.console_screen import cys_console

class CypherDialog(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Settings")

        self.overrideredirect(True) # Removes the Windows border/title bar completely
        self.geometry("340x300")
        self._drag_x = 0
        self._drag_y = 0
        TRANSPARENT_COLOR = "#000001"
        self.configure(fg_color=TRANSPARENT_COLOR)
        self.wm_attributes("-transparentcolor", TRANSPARENT_COLOR)

        self.main_frame = ctk.CTkFrame(self, corner_radius=5, fg_color=sty.main_bg)
        self.main_frame.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)
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

        # Make it "Modal" (stays on top and blocks main window)
        self.lift()  # Bring to front
        # self.attributes("-topmost", True)  # Keep on top
        self.grab_set()  # Block interaction with main window

    def start_drag(self, event):
        """Records the mouse position when you click the title bar"""
        self._drag_x = event.x
        self._drag_y = event.y

    def do_drag(self, event):
        """Calculates how far the mouse moved and moves the window"""
        x = self.winfo_x() + (event.x - self._drag_x)
        y = self.winfo_y() + (event.y - self._drag_y)
        self.geometry(f"+{x}+{y}")

class InputDialog(CypherDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("340x200")
        self.result = None # To store data
        # --- Layout ---
        self.label_1 = ctk.CTkLabel(self.main_frame, text="Key alias:", text_color="#ffffff", anchor="w")
        self.label_1.pack(fill="x", expand=True, side="top", padx=15, pady=(10, 0))
        self.entry_1 = ctk.CTkEntry(self.main_frame, placeholder_text="Enter name")
        self.entry_1.pack(fill="x", expand=True, padx=15, pady=(5, 10))

        # self.label_2 = ctk.CTkLabel(self.main_frame, text="Age:")
        # self.label_2.pack(pady=(10, 0))
        # self.entry_2 = ctk.CTkEntry(self.main_frame, placeholder_text="Enter age")
        # self.entry_2.pack(pady=10)

        # Custom Button Logic
        self.ok_button = ctk.CTkButton(self.main_frame, text="Confirm", command=self.on_confirm, **sty.bundle_common_button)
        self.ok_button.pack(pady=(10, 20))

        '''
        Sometimes, if you call .focus() the exact millisecond the window is created,
        Windows hasn't finished "drawing" the window yet, and the focus fails.
        A safer way is to use .after(), which waits a tiny fraction of a second before focusing.
        '''
        self.after(200, lambda: self.entry_1.focus())

    def on_confirm(self):
        # Handle the logic here!
        self.result = self.entry_1.get()
        print(f"Dialog input captured: {self.result}")
        self.destroy() # Close the dialog

# --- How to call it from your main app ---
def input_dialog(root):
    dialog = InputDialog()
    # Optional: wait for it to close if you need the data immediately
    root.wait_window(dialog)
    if dialog.result:
        return dialog.result
    else:
        cys_console("warn: alais can not be None")
        return dialog.result