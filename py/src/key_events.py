from subprocess import Popen
from time import time

import keyboard as kb
from just_playback import Playback

from app_state import (blinker, chalitah, dattAMsh, fileID, listening_keys,
                       load_data, media_refs, recorded_keys,
                       time_start_listen_key)
from kry import clear_all_media, close_app, pause, resume, stop_media_playback

if True:
    # Blink notification for On and Off
    chalitah.add_callback(lambda vl: blinker.blink("green" if vl else "black"))

    # Blink
    def show_blue(vl):
        if vl:
            blinker.blink("blue")
    listening_keys.add_callback(show_blue)

    dattAMsh.set(load_data.get_dattAMsh())

    def on_vichalitah(active: bool):
        if not active:
            clear_all_media()
    chalitah.add_callback(on_vichalitah)


def start_keyboard_event_listeners():

    kb.add_hotkey("windows+esc+control", close_app)

    # Testing if Keyboard listeners are still working
    kb.add_hotkey("windows+f4", lambda: blinker.blink("purple"))

    # Turning App On/Off
    kb.add_hotkey("windows+f12", lambda: chalitah.set(True))
    kb.add_hotkey("windows+f11", lambda: chalitah.set(False))

    kb.add_hotkey("windows+shift", stop_media_playback)

    # ALL_KEYS_TO_LISTEN

    def listen_keys_for_playing(name: str):
        if not listening_keys.get():
            return
        global recorded_keys
        recorded_keys += name.lower()
    # Calculating All Keys to listen
    all_keys_to_listen = ""
    for x in dattAMsh.get():
        all_keys_to_listen += x
    ALL_KEYS_TO_LISTEN = "".join(list(set(all_keys_to_listen)))
    for key in ALL_KEYS_TO_LISTEN:
        kb.on_press_key(
            key, lambda info: listen_keys_for_playing(str(info.name)))

    def play_key_pressed(_):
        if not listening_keys.get():
            return
        global time_start_listen_key, recorded_keys
        if time() - time_start_listen_key >= 3.0:
            pass
        else:
            data = dattAMsh.get()
            if recorded_keys in data:
                fileID.set(recorded_keys)
        listening_keys.set(False)
    kb.on_press_key("shift", play_key_pressed)

    def set_listening_keys_status():
        if not chalitah.get():
            return
        listening_keys.set(True)
    kb.add_hotkey("windows+f10", set_listening_keys_status)

    def record_start_time():
        global time_start_listen_key, recorded_keys
        time_start_listen_key = time()
        recorded_keys = ""
    listening_keys.add_callback(lambda _: record_start_time())

    # Pause/Resume
    kb.add_hotkey("left+right", pause)

    kb.add_hotkey("ctrl+up+down", resume)


def set_media_file(val: str):
    if val == "":
        return
    # Set new file whenver fileID changes
    clear_all_media(clear_file_id=False)
    fl_info = dattAMsh.get()[val]

    fldr_loc = load_data.CONFIG_DATA.folder_loc
    loc = f'{fldr_loc}/{fl_info[0]}'
    if fl_info[2] == 0:  # Music File
        media_refs.audio = Playback(loc)
        media_refs.audio.play()
        media_refs.audio.loop_at_end(True)
    elif fl_info[2] == 1:  # Video File
        command = f'"{load_data.CONFIG_DATA.vlc_loc}" "{loc}"'
        media_refs.video = Popen(command)

    blinker.blink("brown", 1000)


fileID.add_callback(set_media_file)
