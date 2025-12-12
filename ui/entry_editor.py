import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from models import Account


class EntryEditor(tk.Toplevel):
    """
    Popup window used for adding or editing an account.
    If account is None → Add Mode
    If account is provided → Edit Mode
    """

    def __init__(self, parent, account=None):
        super().__init__(parent)

        self.parent = parent
        self.account = account
        self.result = None  # Will hold the new or updated Account object

        self.title("Edit Account" if account else "Add Account")
        self.geometry("350x380")
        self.resizable(False, False)

        self._build_ui()
        self._load_account_data()

    def _build_ui(self):
        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Name
        ttk.Label(frame, text="Account Name:").pack(anchor="w")
        self.name_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.name_var).pack(fill="x", pady=5)

        # Username
        ttk.Label(frame, text="Username / Email:").pack(anchor="w")
        self.username_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.username_var).pack(fill="x", pady=5)

        # Password
        ttk.Label(frame, text="Password:").pack(anchor="w")
        self.password_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.password_var).pack(fill="x", pady=5)

        # Notes
        ttk.Label(frame, text="Notes:").pack(anchor="w")
        self.notes_text = tk.Text(frame, height=5)
        self.notes_text.pack(fill="both", pady=5)

        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Save", command=self._save).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.destroy).grid(row=0, column=1, padx=5)

    def _load_account_data(self):
        if not self.account:
            return

        self.name_var.set(self.account.name)
        self.username_var.set(self.account.username)
        self.password_var.set(self.account.password)
        self.notes_text.insert("1.0", self.account.notes)

    def _save(self):
        name = self.name_var.get().strip()
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        notes = self.notes_text.get("1.0", "end").strip()

        if not name:
            messagebox.showerror("Error", "Account name is required.")
            return

        if not password:
            messagebox.showerror("Error", "Password is required.")
            return

        # Build an Account object
        new_account = Account(name, username, password, notes)

        self.result = new_account
        self.destroy()
