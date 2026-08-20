import subprocess
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ==========================================
# COLOR PALETTE (modern, consistent)
# ==========================================
ACCENT = "#3B82F6"  # active nav / accent
ACCENT_HOVER = "#2563EB"
SIDEBAR_BG = "#111827"
CONTENT_BG = "#0B0F17"
CARD_BG = "#1B2432"
CARD_HOVER = "#242F42"
DANGER = "#EF4444"
SUCCESS = "#10B981"
WARNING = "#F59E0B"
WARNING_HOVER = "#D97706"
TEXT_MUTED = "#8A93A6"


class WinToolApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Windows System Utility Tool")
        self.geometry("820x560")

        # Window Icon & Taskbar Icon ထည့်သွင်းခြင်း
        try:
            self.iconbitmap("my_icon.ico")
        except Exception as e:
            print(f"Icon loading error: {e}")

        self.title("Windows System Utility Tool")
        self.geometry("820x560")
        self.minsize(700, 480)
        self.configure(fg_color=CONTENT_BG)
        self.resizable(True, True)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # keep track of nav buttons so we can highlight the active one
        self.nav_buttons = {}

        # ==========================================
        # 1. SIDEBAR NAVIGATION
        # ==========================================
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=SIDEBAR_BG)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_propagate(False)
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="🛠️  Win Tool",
            font=("Segoe UI", 22, "bold"),
            text_color="#FFFFFF"
        )
        self.logo_label.grid(row=0, column=0, padx=24, pady=(28, 4), sticky="w")

        self.logo_sub = ctk.CTkLabel(
            self.sidebar_frame,
            text="System Utility Panel",
            font=("Segoe UI", 12),
            text_color=TEXT_MUTED
        )
        self.logo_sub.grid(row=1, column=0, padx=24, pady=(0, 20), sticky="w")

        self.btn_nav_security = self.add_nav_button("🛡️  Security & Cleanup", 2, self.show_security_page)
        self.btn_nav_hardware = self.add_nav_button("💻      System Control", 3, self.show_hardware_page)
        self.btn_nav_system = self.add_nav_button("🖥️  Update the system", 4, self.show_system_page)

        # footer status bar inside sidebar
        self.status_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="● Ready",
            font=("Segoe UI", 11),
            text_color=SUCCESS
        )
        self.status_label.grid(row=7, column=0, padx=24, pady=(0, 18), sticky="w")

        # ==========================================
        # 2. PAGES / FRAMES
        # ==========================================
        # PAGE 1: Security & Cleanup Tools
        self.page_security = ctk.CTkScrollableFrame(
            self, label_text="🛡️  Security & Cleanup Tools", fg_color=CONTENT_BG,
            label_font=("Segoe UI", 16, "bold")
        )

        self.add_action_button(self.page_security, "🛡️", "Windows Security", "Check Windows Security", ACCENT, ACCENT_HOVER, lambda: self.run_cmd(["start", "windowsdefender:"]))
        self.add_action_button(self.page_security, "📦", "Windows Update", "Check update settings", ACCENT, ACCENT_HOVER, lambda: self.run_cmd(["start", "ms-settings:windowsupdate"]))
        self.add_action_button(self.page_security, "🧹", "Temp Folder", "Delete temporary files", ACCENT, ACCENT_HOVER, lambda: self.run_cmd(["explorer", "temp"]))
        self.add_action_button(self.page_security, "🧹", "%temp% Folder", "Delete AppData temp files", ACCENT, ACCENT_HOVER, lambda: self.run_cmd(["explorer", "shell:local appdata\\temp"]))
        self.add_action_button(self.page_security, "🧹", "Prefetch Folder", "Delete Prefetch file", ACCENT, ACCENT_HOVER, lambda: self.run_cmd(["explorer", "C:\\Windows\\Prefetch"]))
        self.add_action_button(self.page_security, "🧹", "Disk Cleanup", "Clean up drive using cleanmgr", ACCENT, ACCENT_HOVER, lambda: self.run_cmd(["cleanmgr"]))

        # PAGE 2: Hardware & Device Control
        self.page_hardware = ctk.CTkScrollableFrame(
            self, label_text="💻  System Control", fg_color=CONTENT_BG,
            label_font=("Segoe UI", 16, "bold")
        )
        self.add_action_button(self.page_hardware, "🤖", "Control Panel", "Classic control panel", ACCENT, ACCENT_HOVER, lambda: self.run_cmd(["control"]))
        self.add_action_button(self.page_hardware, "📦", "Installed Apps", "Check installed apps", ACCENT, ACCENT_HOVER, lambda: self.run_cmd(["appwiz.cpl"]))
        self.add_action_button(self.page_hardware, "💾", "Disk Management", "Check disk partition", ACCENT, ACCENT_HOVER, lambda: self.run_cmd(["diskmgmt.msc"]))
        self.add_action_button(self.page_hardware, "🔌", "Device Manager", "Check connected devices", ACCENT, ACCENT_HOVER, lambda: self.run_cmd(["devmgmt.msc"]))
        self.add_action_button(self.page_hardware, "🌐", "Network Connections", "Check Network Connections", ACCENT, ACCENT_HOVER, lambda: self.run_cmd(["ncpa.cpl"]))
        self.add_action_button(self.page_hardware, "⚙️", "Registry Editor", "Customize Windows Features", ACCENT, ACCENT_HOVER, lambda: self.run_cmd(["regedit"]))

        # PAGE 3: System Control Page
        self.page_system = ctk.CTkScrollableFrame(
            self, label_text="🖥️  Update the system", fg_color=CONTENT_BG,
            label_font=("Segoe UI", 16, "bold")
        )
        self.add_action_button(self.page_system, "🚀", "Chris Titus WinUtil", "Fix the Windows Operating System", SUCCESS, SUCCESS, self.launch_winutil)
        self.add_action_button(self.page_system, "📈", "Update All Apps", "Update software on the PC", WARNING, WARNING_HOVER, self.launch_winget_update)
        self.add_action_button(self.page_system, "📁", "File Explorer", "Open File Explorer", SUCCESS, SUCCESS, lambda: self.run_cmd(["explorer"]))
        self.add_action_button(self.page_system, "⚙️", "Windows Settings", "Open Windows Settings", SUCCESS, SUCCESS, lambda: self.run_cmd(["start", "ms-settings:"], shell=True))
        self.add_action_button(self.page_system, "📊", "Task Manager", "Open Task Manager", ACCENT, ACCENT_HOVER, lambda: self.run_cmd(["taskmgr"]))

        # Default Page
        self.show_security_page()

    # ==========================================
    # HELPER & ACTION FUNCTIONS
    # ==========================================
    def add_nav_button(self, text, row, command):
        btn = ctk.CTkButton(
            self.sidebar_frame,
            text=text,
            font=("Segoe UI", 14),
            anchor="w",
            compound="left",
            height=44,
            corner_radius=8,
            fg_color="transparent",
            text_color="#C7CDD9",
            hover_color="#1F2937",
            command=command
        )
        btn.grid(row=row, column=0, padx=8, pady=4, sticky="ew")
        self.nav_buttons[btn] = text
        return btn

    def set_active_nav(self, active_btn):
        for btn in self.nav_buttons:
            if btn is active_btn:
                btn.configure(fg_color=ACCENT, text_color="#FFFFFF", hover_color=ACCENT_HOVER)
            else:
                btn.configure(fg_color="transparent", text_color="#C7CDD9", hover_color="#1F2937")

    def add_action_button(self, parent_frame, icon, title, subtitle, color, hover_color, command_func):
        card = ctk.CTkFrame(parent_frame, corner_radius=12, fg_color=CARD_BG, cursor="hand2")
        card.pack(pady=6, padx=6, fill="x")

        # Icon Label
        icon_label = ctk.CTkLabel(card, text=icon, font=("Segoe UI", 22), width=50)
        icon_label.pack(side="left", padx=(15, 10), pady=12)

        # Text Frame
        text_frame = ctk.CTkFrame(card, fg_color="transparent")
        text_frame.pack(side="left", fill="both", expand=True, pady=10)

        title_label = ctk.CTkLabel(
            text_frame, text=title, font=("Segoe UI", 14, "bold"),
            text_color="#FFFFFF", anchor="w"
        )
        title_label.pack(fill="x", anchor="w")

        sub_label = ctk.CTkLabel(
            text_frame, text=subtitle, font=("Segoe UI", 11),
            text_color=TEXT_MUTED, anchor="w"
        )
        sub_label.pack(fill="x", anchor="w", pady=(2, 0))

        # Event Binding
        widgets = (card, icon_label, text_frame, title_label, sub_label)
        for widget in widgets:
            widget.bind("<Button-1>", lambda e, cmd=command_func, t=title: self.execute_action(cmd, t))
            widget.bind("<Enter>", lambda e: card.configure(fg_color=CARD_HOVER))
            widget.bind("<Leave>", lambda e: card.configure(fg_color=CARD_BG))

    def execute_action(self, command_func, title):
        self.status_label.configure(text=f"● Running: {title}", text_color=WARNING)
        
        try:
            command_func()
            # 1 စက္ကန့်အကြာတွင် Status ကို Ready ဟု safe အပြောင်းအလဲလုပ်ရန် after() သုံးခြင်း
            self.after(1000, lambda: self.status_label.configure(text="● Ready", text_color=SUCCESS))
        except Exception as e:
            self.status_label.configure(text=f"● Error: {e}", text_color=DANGER)

    def hide_all_pages(self):
        self.page_security.grid_forget()
        self.page_hardware.grid_forget()
        self.page_system.grid_forget()

    def show_security_page(self):
        self.hide_all_pages()
        self.page_security.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.set_active_nav(self.btn_nav_security)

    def show_hardware_page(self):
        self.hide_all_pages()
        self.page_hardware.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.set_active_nav(self.btn_nav_hardware)

    def show_system_page(self):
        self.hide_all_pages()
        self.page_system.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.set_active_nav(self.btn_nav_system)

    def run_cmd(self, cmd_args, shell=True):
        """Subprocess ဖြင့် System Tools များ တိုက်ရိုက်ပွင့်စေခြင်း"""
        subprocess.Popen(cmd_args, shell=shell)

    def launch_winutil(self):
        """Chris Titus WinUtil ကို PowerShell (Admin) ဖြင့် ပွင့်စေခြင်း"""
        ps_command = "Start-Process powershell -Verb RunAs -ArgumentList '-NoExit -Command irm christitus.com/win | iex'"
        subprocess.Popen(["powershell", "-Command", ps_command], shell=True)

    def launch_winget_update(self):
        """CMD ကို Admin ဖွင့်ပြီး Winget Upgrade လုပ်ဆောင်ခြင်း"""
        cmd_command = "Start-Process cmd -Verb RunAs -ArgumentList '/k winget upgrade --all'"
        subprocess.Popen(["powershell", "-Command", cmd_command], shell=True)


if __name__ == "__main__":
    app = WinToolApp()
    app.mainloop()