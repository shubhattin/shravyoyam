from app_state import blinker_root
from key_events import start_keyboard_event_listeners, register_state_change_callbacks
from taskbar import start_taskbar
from threading import Thread

if __name__ == "__main__":
    register_state_change_callbacks()
    start_keyboard_event_listeners()
    th = Thread(target=start_taskbar)
    th.daemon = True
    th.start()
    blinker_root.mainloop()
