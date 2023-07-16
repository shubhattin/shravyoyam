from app_state import blinker_root
from key_events import start_keyboard_event_listeners

if __name__ == "__main__":
    start_keyboard_event_listeners()
    blinker_root.mainloop()
