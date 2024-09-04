import customtkinter as ctk


class MessageBox(ctk.CTkToplevel):
    def __init__(self, parent, title="Message", message=""):
        super().__init__(parent)

        self.title(title)
        self.geometry("300x150")
        self.resizable(False, False)

        # Message label
        self.label = ctk.CTkLabel(self, text=message, wraplength=250)
        self.label.pack(pady=20)

        # OK button
        self.ok_button = ctk.CTkButton(self, text="OK", command=self.destroy)
        self.ok_button.pack(pady=10)

        # Center the window
        self.update_idletasks()

        parent.update()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)

        self.geometry(f"+{x}+{y}")

        # Make the dialog modal
        self.transient(parent)
        self.grab_set()
        self.wait_window(self)
