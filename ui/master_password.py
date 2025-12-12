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
        self._center_window(self, 380, 230)

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
        Attempt to unlock an existing vault with the entered password.
        """

        password = self.password_var.get().strip()

        if not password:
            messagebox.showerror("Error", "Please enter a master password.")
            return

        try:
            self.vault.load(password)
        except FileNotFoundError:
            messagebox.showerror("Error", "No vault found. Create a new one.")
            return
        except ValueError:
            messagebox.showerror("Error", "Incorrect master password.")
            return
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")
            return

        # If we reach this point: loaded successfully
        self.destroy()
        self.on_unlock_callback(password)


    def _create_new(self):
        """
        Create a new vault using the entered password.
        """

        password = self.password_var.get().strip()

        if not password:
            messagebox.showerror("Error", "Please enter a master password.")
            return

        try:
            self.vault.create_new(password)
        except Exception as e:
            messagebox.showerror("Error", f"Could not create vault: {e}")
            return

        messagebox.showinfo("Success", "Vault created successfully!")

        self.destroy()
        self.on_unlock_callback(password)

    def _center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        window.geometry(f"{width}x{height}+{x}+{y}")
