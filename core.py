import threading
import time
import secrets
import pyperclip

# ============================================================
# GLOBAL STATE — CLIPBOARD MANAGEMENT
# ============================================================

# Timer thread for clearing the clipboard
_clipboard_timer = None

# UI callback for countdown updates (UI sets this)
_clipboard_callback = None


# ============================================================
# GLOBAL STATE — AUTO-LOCK SYSTEM
# ============================================================

# Timer thread for auto-lock
_auto_lock_timer = None

# Callback the UI registers (UI calls register_auto_lock_callback)
_auto_lock_callback = None

# Default timeout (in seconds) before auto-lock triggers
_auto_lock_timeout = 600  # 10 minutes

# Last moment the user interacted with the UI
_last_activity = time.time()


# ============================================================
# CLIPBOARD CLEARING WORKER
# Runs in background to clear clipboard securely
# ============================================================

def _clipboard_clear_worker(timeout: int, callback):
    """
    Background thread:
    - Counts down
    - Sends countdown updates to UI
    - Overwrites clipboard with random data when done
    """

    try:
        for remaining in range(timeout, 0, -1):
            if callback:
                callback(remaining)
            time.sleep(1)

        # Overwrite clipboard with secure random junk on timeout
        junk = secrets.token_hex(16)
        pyperclip.copy(junk)

        if callback:
            callback(0)  # Signal completion

    except Exception as e:
        print("Clipboard clear error:", e)


def copy_password_safely(password: str, timeout: int = 20, callback=None):
    """
    Public function for UI:
    - Copies password to clipboard
    - Starts countdown to auto-clear
    - Sends updates to UI through callback
    """

    global _clipboard_timer, _clipboard_callback

    # Copy password immediately
    pyperclip.copy(password)

    # Cancel old timer if running
    if _clipboard_timer and _clipboard_timer.is_alive():
        try:
            _clipboard_timer.cancel()  # type: ignore
        except:
            pass

    _clipboard_callback = callback

    # Start background countdown thread
    _clipboard_timer = threading.Thread(
        target=_clipboard_clear_worker,
        args=(timeout, callback),
        daemon=True
    )
    _clipboard_timer.start()


# ============================================================
# AUTO-LOCK WORKER
# Runs in background and locks vault after inactivity
# ============================================================

def _auto_lock_worker():
    global _last_activity

    while True:
        time.sleep(1)

        # If inactivity exceeds timeout → lock the vault
        if time.time() - _last_activity >= _auto_lock_timeout:
            if _auto_lock_callback:
                _auto_lock_callback()
            break


def set_auto_lock_timeout(seconds: int):
    """
    Set how long the vault can stay idle before locking.
    """

    global _auto_lock_timeout
    _auto_lock_timeout = seconds


def register_auto_lock_callback(callback):
    """
    UI uses this to tell core.py what function to call on auto-lock.
    """

    global _auto_lock_callback
    _auto_lock_callback = callback


def touch_activity():
    """
    UI must call this on every user interaction:
    clicks, typing, switching tabs, etc.
    """

    global _last_activity
    _last_activity = time.time()


def start_auto_lock_timer():
    """
    Starts the auto-lock worker thread if it's not already running.
    """

    global _auto_lock_timer

    if _auto_lock_timer and _auto_lock_timer.is_alive():
        return  # Already running

    _auto_lock_timer = threading.Thread(
        target=_auto_lock_worker,
        daemon=True
    )
    _auto_lock_timer.start()
