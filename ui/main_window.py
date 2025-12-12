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
        self._build_menu()
        self._center_window(self, 700, 400)

        from core import register_auto_lock_callback, start_auto_lock_timer, set_auto_lock_timeout

        # Set timeout (5 minutes = 300 seconds)
        set_auto_lock_timeout(300)

        # Register callback
        register_auto_lock_callback(self._lock_vault)

        # Start auto-lock timer
        start_auto_lock_timer()

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
        self.search_var.trace_add("write", self._filter_accounts)
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

        self.add_btn = ttk.Button(btn_frame, text="Add", command=self._add_account)
        self.add_btn.grid(row=0, column=0, padx=5)

        self.copy_user_btn = ttk.Button(btn_frame, text="Copy Username", command=self._copy_username)
        self.copy_user_btn.grid(row=0, column=1, padx=5)

        self.copy_pass_btn = ttk.Button(btn_frame, text="Copy Password", command=self._copy_password)
        self.copy_pass_btn.grid(row=0, column=2, padx=5)

        self.edit_btn = ttk.Button(btn_frame, text="Edit", command=self._edit_account)
        self.edit_btn.grid(row=0, column=3, padx=5)

        self.delete_btn = ttk.Button(btn_frame, text="Delete", command=self._delete_account)
        self.delete_btn.grid(row=0, column=4, padx=5)

        # Status Label (for clipboard countdown)
        self.status_label = ttk.Label(right_frame, text="")
        self.status_label.pack(anchor="w", pady=10)

        self.account_list.bind("<<ListboxSelect>>", self._on_select_account)

        self._refresh_account_list()

    def _add_account(self):

        from ui.entry_editor import EntryEditor
        from core import touch_activity

        # Reinitialize auto-lock timer on user activity
        touch_activity()

        editor = EntryEditor(self)
        self.wait_window(editor)

        if editor.result:
            # Add to vault
            self.vault.accounts.append(editor.result)
            self.vault.save(self.master_password)

            # Refresh UI
            self._refresh_account_list()

            # Clear status message
            self.status_label.config(text="Account added successfully!")

    def _copy_username(self):

        from core import touch_activity

        # Reinitialize auto-lock timer on user activity
        touch_activity()

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

        from core import touch_activity

        # Reinitialize auto-lock timer on user activity
        touch_activity()

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

        from core import touch_activity

        # Reinitialize auto-lock timer on user activity
        touch_activity()

        selection = self.account_list.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an account to edit.")
            return

        index = selection[0]
        account = self.vault.accounts[index]

        from ui.entry_editor import EntryEditor
        editor = EntryEditor(self, account=account)
        self.wait_window(editor)

        if editor.result:
            # Update account in vault
            self.vault.accounts[index] = editor.result
            self.vault.save(self.master_password)

            # Refresh display
            self._refresh_account_list()
            self.status_label.config(text="Account updated successfully!")

    def _delete_account(self):

        from core import touch_activity

        # Reinitialize auto-lock timer on user activity
        touch_activity()

        selection = self.account_list.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an account to delete.")
            return

        index = selection[0]
        account = self.vault.accounts[index]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete '{account.name}'?"
        )

        if not confirm:
            return

        # Delete and save
        del self.vault.accounts[index]
        self.vault.save(self.master_password)

        # Refresh UI
        self._refresh_account_list()
        self.details_title.config(text="Select an account")
        self.username_label.config(text="Username:")
        self.password_label.config(text="Password:")
        self.notes_label.config(text="Notes:")
        self.status_label.config(text="Account deleted.")

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

        from core import touch_activity

        # Reinitialize auto-lock timer on user activity
        touch_activity()

        selection = self.account_list.curselection()
        if not selection:
            return

        selected_name = self.account_list.get(selection[0])

        # Find matching account object
        account = next(a for a in self.vault.accounts if a.name == selected_name)

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

    def _filter_accounts(self, *args):
        """
        Filter the account list based on the search field.
        """

        from core import touch_activity

        # Reinitialize auto-lock timer on user activity
        touch_activity()

        query = self.search_var.get().strip().lower()

        self.account_list.delete(0, tk.END)

        for account in self.vault.accounts:
            if query in account.name.lower():
                self.account_list.insert(tk.END, account.name)

    def _lock_vault(self):
        """
        Called automatically when inactivity timeout is reached.
        Closes the main window and returns user to the master password screen.
        """

        messagebox.showinfo("Session Locked", "Your vault was locked due to inactivity.")

        self.destroy()

        # Relaunch master password window
        from ui.master_password import MasterPasswordWindow
        MasterPasswordWindow(
            on_unlock_callback=self._reopen_after_lock,
            vault=self.vault
        ).mainloop()

    def _reopen_after_lock(self, master_password):
        """
        Called after the user re-enters their password following auto-lock.
        """

        from vault import Vault
        from ui.main_window import MainWindow

        vault = Vault("vault.enc")
        vault.load(master_password)
        MainWindow(vault, master_password).mainloop()

    def _build_menu(self):
        menu_bar = tk.Menu(self)

        # File menu (empty for now, expandable later)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.destroy)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self._open_about_window)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        # Attach menu bar to window
        self.config(menu=menu_bar)

    def _open_about_window(self):
        about = tk.Toplevel(self)
        about.title("About Password Vault")
        about.geometry("350x240")
        about.resizable(False, False)

        # Center the About window
        self._center_window(about, 350, 240)

        frame = ttk.Frame(about, padding=15)
        frame.pack(fill="both", expand=True)

        # Labels
        ttk.Label(frame, text="Password Vault — Version 1.0", font=("Arial", 12, "bold")).pack(pady=(0, 10))
        ttk.Label(frame, text="Created by: Benoit Monette").pack(anchor="w")
        ttk.Label(frame, text="Email: benoitmonette80@gmail.com").pack(anchor="w", pady=(0, 10))
        ttk.Label(frame, text="Website: https://foriloop.com").pack(anchor="w", pady=(0, 10))

        ttk.Label(frame, text="A simple offline password manager built in Python.\n"
                              "All data is encrypted locally using AES-GCM.",
                  justify="left", wraplength=300).pack(anchor="w", pady=5)

        ttk.Button(frame, text="Close", command=about.destroy).pack(pady=10)

        about.grab_set()

    def _center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        window.geometry(f"{width}x{height}+{x}+{y}")
