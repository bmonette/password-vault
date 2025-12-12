from ui.master_password import MasterPasswordWindow
from ui.main_window import MainWindow
from vault import Vault
from models import Account


def open_main_window(master_password):
    vault = Vault("vault.enc")
    vault.load(master_password)

    MainWindow(vault, master_password).mainloop()


if __name__ == "__main__":
    vault = Vault("vault.enc")
    app = MasterPasswordWindow(open_main_window, vault)
    app.mainloop()
