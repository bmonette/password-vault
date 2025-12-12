import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class MasterPasswordWindow(tk.Tk):
    """
    First window shown to the user.
    Used to unlock an existing vault or create a new one.
    """

    def __init__(self, on_unlock_callback, vault):
        super().__init__()

        self.on_unlock_callback = on_unlock_callback
        self.vault = vault

        self.title("Password Vault - Unlock")
        self.geometry("380x230")
        self.resizable(False, False)

        self._build_ui()

    def _build_ui(self):
        # Title label
        title = ttk.Label(self, text="Unlock Your Vault", font=("Arial", 16))
        title.pack(pady=10)

        # Password label + entry
        self.password_var = tk.StringVar()
        password_label = ttk.Label(self, text="Master Password:")
        password_label.pack()

        self.password_entry = ttk.Entry(
            self, textvariable=self.password_var, show="*"
        )
        self.password_entry.pack(pady=5)

        # Buttons frame
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=15)

        unlock_btn = ttk.Button(btn_frame, text="Unlock", command=self._unlock)
        unlock_btn.grid(row=0, column=0, padx=5)

        create_btn = ttk.Button(btn_frame, text="Create New Vault", command=self._create_new)
        create_btn.grid(row=0, column=1, padx=5)

    def _unlock(self):
        """
        Placeholder: unlock vault using entered password.
        Logic will be added later.
        """

        messagebox.showinfo("Info", "Unlock logic not implemented yet.")

    def _create_new(self):
        """
        Placeholder: create a new vault using entered password.
        Logic will be added later.
        """

        messagebox.showinfo("Info", "Create logic not implemented yet.")
