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

    def _copy_username(self):
        messagebox.showinfo("Info", "Copy username not implemented yet.")

    def _copy_password(self):
        messagebox.showinfo("Info", "Copy password not implemented yet.")

    def _edit_account(self):
        messagebox.showinfo("Info", "Edit account not implemented yet.")

    def _delete_account(self):
        messagebox.showinfo("Info", "Delete account not implemented yet.")
