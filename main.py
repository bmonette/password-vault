from ui.master_password import MasterPasswordWindow
from vault import Vault


def open_main_window(master_password):
    print("Vault unlocked with password:", master_password)
    print("Next step: open the main window (UI coming next).")


if __name__ == "__main__":
    vault = Vault("vault.enc")
    app = MasterPasswordWindow(open_main_window, vault)
    app.mainloop()
