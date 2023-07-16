from app_state import blinker_root
from key_events import start_keyboard_event_listeners
from taskbar import start_taskbar
from threading import Thread

if __name__ == "__main__":
    start_keyboard_event_listeners()
    th = Thread(target=start_taskbar)
    th.daemon = True
    th.start()
    blinker_root.mainloop()
