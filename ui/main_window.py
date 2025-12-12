import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class MainWindow(tk.Tk):
    """
    Main UI window that appears after unlocking the vault.
    Displays a list of accounts and details for the selected account.
    """

    def __init__(self, vault, master_password):
        super().__init__()

        self.vault = vault
        self.master_password = master_password

        self.title("Password Vault")
        self.geometry("700x400")
        self.resizable(False, False)

        self._build_ui()

    def _build_ui(self):
        # Main container frame
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # ====================================
        # Left Side: Account List + Search Bar
        # ====================================
        left_frame = ttk.Frame(container, width=250)
        left_frame.pack(side="left", fill="y")

        # Search Bar
        search_label = ttk.Label(left_frame, text="Search:")
        search_label.pack(anchor="w")

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(left_frame, textvariable=self.search_var)
        search_entry.pack(fill="x", pady=5)

        # Account Listbox
        self.account_list = tk.Listbox(left_frame, height=20)
        self.account_list.pack(fill="both", expand=True)

        # ====================================
        # Right Side: Account Details
        # ====================================
        right_frame = ttk.Frame(container)
        right_frame.pack(side="right", fill="both", expand=True, padx=20)

        self.details_title = ttk.Label(right_frame, text="Select an account", font=("Arial", 14))
        self.details_title.pack(pady=10)

        self.username_label = ttk.Label(right_frame, text="Username: ")
        self.username_label.pack(anchor="w")

        self.password_label = ttk.Label(right_frame, text="Password: ")
        self.password_label.pack(anchor="w", pady=5)

        self.notes_label = ttk.Label(right_frame, text="Notes: ")
        self.notes_label.pack(anchor="w", pady=5)

        # Buttons (Copy, Edit, Delete)
        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(pady=20)

        self.copy_user_btn = ttk.Button(btn_frame, text="Copy Username", command=self._copy_username)
        self.copy_user_btn.grid(row=0, column=0, padx=5)

        self.copy_pass_btn = ttk.Button(btn_frame, text="Copy Password", command=self._copy_password)
        self.copy_pass_btn.grid(row=0, column=1, padx=5)

        self.edit_btn = ttk.Button(btn_frame, text="Edit", command=self._edit_account)
        self.edit_btn.grid(row=0, column=2, padx=5)

        self.delete_btn = ttk.Button(btn_frame, text="Delete", command=self._delete_account)
        self.delete_btn.grid(row=0, column=3, padx=5)

        # Status Label (for clipboard countdown)
        self.status_label = ttk.Label(right_frame, text="")
        self.status_label.pack(anchor="w", pady=10)

        self.account_list.bind("<<ListboxSelect>>", self._on_select_account)

        self._refresh_account_list()

    def _copy_username(self):
        selection = self.account_list.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an account first.")
            return

        index = selection[0]
        account = self.vault.accounts[index]

        import pyperclip
        pyperclip.copy(account.username)

        self.status_label.config(text="Username copied to clipboard.")

    def _copy_password(self):
        selection = self.account_list.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an account first.")
            return

        index = selection[0]
        account = self.vault.accounts[index]

        from core import copy_password_safely

        # Start safe clipboard copy with 20-second timeout
        copy_password_safely(account.password, timeout=20, callback=self._update_clipboard_countdown)

        # Immediate UI feedback
        self.status_label.config(text="Password copied. Clipboard clearing in: 20s")

    def _edit_account(self):
        messagebox.showinfo("Info", "Edit account not implemented yet.")

    def _delete_account(self):
        messagebox.showinfo("Info", "Delete account not implemented yet.")

    def _refresh_account_list(self):
        """
        Load account names into the Listbox.
        """

        self.account_list.delete(0, tk.END)

        for account in self.vault.accounts:
            self.account_list.insert(tk.END, account.name)

    def _on_select_account(self, event):
        """
        Called when user selects an account from the list.
        Displays account details on the right panel.
        """

        selection = self.account_list.curselection()
        if not selection:
            return

        index = selection[0]
        account = self.vault.accounts[index]

        # Update the right-side labels
        self.details_title.config(text=account.name)
        self.username_label.config(text=f"Username: {account.username}")
        self.password_label.config(text=f"Password: {'*' * len(account.password)}")
        self.notes_label.config(text=f"Notes: {account.notes}")

    def _update_clipboard_countdown(self, remaining_seconds):
        """
        Called every second by core.py to update countdown label.
        """

        if remaining_seconds > 0:
            self.status_label.config(
                text=f"Password copied. Clipboard clearing in: {remaining_seconds}s"
            )
        else:
            self.status_label.config(
                text="Clipboard cleared."
            )
