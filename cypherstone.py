import customtkinter as ctk
import tkinter as tk
from gui.console_screen import ConsoleScreen
from gui.frame_decrypt import DecypherFrame
from gui.frame_encrypt import EncypherFrame
from gui.frame_setting import SettingFrame
from gui.frame_user import UserFrame
import gui.style_constants as sty
from gui.console_screen import cys_console

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

        # self.min_btn = ctk.CTkButton(
        #     self.title_bar, text="—", width=24, height=24, corner_radius=12,
        #     fg_color="transparent", border_width=2, border_color="#ffbd2e", text_color="#ffbd2e",
        #     hover_color="#594314", command=self.minimize_window
        # )
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

        # ==========================================
        # BOTTOM CONSOLE SCREEN
        # ==========================================
        self.console_screen = ConsoleScreen(self.main_frame, height=180, corner_radius=2, fg_color=sty.console_bg,
                                        border_color="#ffffff", border_width=1,
                                        )
        self.console_screen.pack(side="bottom", fill="both", **sty.bundle_main_frame_padding, pady=(0, 12))

        self.after(200, lambda: cys_console("Welcome using CypherStone."))

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

if __name__ == "__main__":
    app = CypherStoneApp()
    app.mainloop()