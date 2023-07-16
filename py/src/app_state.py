from tkinter import Tk
from typing import Dict, Tuple

from Blinker import Blinker
from State import State
from load_data import get_dattAMsh, dattAMshType, CONFIG_DATA
from just_playback import Playback

"App's State"
chalitah = State(False)
"""App's On/Off State"""

fileID = State("")
fileInfo = State[Tuple[str, str, int]](("", "", 0))

dattAMsh = State[dattAMshType]({})
"""All the file related data"""

listening_keys = State(False)
"""State for is the keys pressed should be listened"""

blinker_root = Tk()
"""Blinker root is defined also to stop the app from closing, also using it instead of `kb.wait`"""
blinker = Blinker(blinker_root)
ALL_KEYS_TO_LISTEN = ""
audio_playback_ref: Playback | None = None
time_start_listen_key: float = 0
recorded_keys: str = ""

def add_events():
    # Blink notification for On and Off
    chalitah.add_callback(lambda vl: blinker.blink("green" if vl else "black"))

    # Blink
    def show_blue(vl):
        if vl:
            blinker.blink("blue")
    listening_keys.add_callback(show_blue)


add_events()

dattAMsh.set(get_dattAMsh())
# Calculating All Keys to listen
if True:
    r = ""
    for x in dattAMsh.get():
        r += x
    ALL_KEYS_TO_LISTEN = "".join(list(set(r)))
