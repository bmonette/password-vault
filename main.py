from ui.master_password import MasterPasswordWindow
from vault import Vault


def on_unlock():
    print("Unlocked! (Placeholder)")


if __name__ == "__main__":
    vault = Vault("vault.enc")
    app = MasterPasswordWindow(on_unlock, vault)
    app.mainloop()
