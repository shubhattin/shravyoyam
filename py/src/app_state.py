from tkinter import Tk
from subprocess import Popen

from Blinker import Blinker
from State import State
import load_data
from just_playback import Playback

"App's State"
chalitah = State(False)
"""App's On/Off State"""

fileID = State("")

dattAMsh = State[load_data.dattAMshType]({})
"""All the file related data"""

listening_keys = State(False)
"""State for is the keys pressed should be listened"""

blinker_root = Tk()
"""Blinker root is defined also to stop the app from closing, also using it instead of `kb.wait`"""
blinker = Blinker(blinker_root)


class PLAYER_REFERENCES:
    audio: Playback | None = None
    video: Popen | None = None


media_refs = PLAYER_REFERENCES()

time_start_listen_key: float = 0
recorded_keys: str = ""
