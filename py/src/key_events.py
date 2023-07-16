from time import time

import keyboard as kb

from app_state import (ALL_KEYS_TO_LISTEN, CONFIG_DATA, Playback,
                       audio_playback_ref, blinker, blinker_root, chalitah,
                       dattAMsh, fileID, fileInfo, listening_keys,
                       recorded_keys, time_start_listen_key)


def start_keyboard_event_listeners():
    # Closing App
    def close_app():
        blinker.blink("red")

        blinker_root.after(500, blinker_root.destroy)
    kb.add_hotkey("windows+esc+control", close_app)

    # Testing if Keyboard listeners are still working
    kb.add_hotkey("windows+f4", lambda: blinker.blink("purple"))

    # Turning App On/Off
    kb.add_hotkey("windows+f12", lambda: chalitah.set(True))
    kb.add_hotkey("windows+f11", lambda: chalitah.set(False))

    # Stop Playback
    def stop_media_playback():
        clear_all_media()
        blinker.blink("purple", 700)
    kb.add_hotkey("windows+shift", stop_media_playback)

    # ALL_KEYS_TO_LISTEN
    def listen_keys_for_playing(name: str):
        if not listening_keys.get():
            return
        global recorded_keys
        recorded_keys += name.lower()
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
                fileInfo.set(data[recorded_keys])
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


def clear_all_media():
    global audio_playback_ref
    if audio_playback_ref:  # For audio
        audio_playback_ref.stop()
        audio_playback_ref = None


def pause():
    global audio_playback_ref
    if not audio_playback_ref:
        return
    audio_playback_ref.pause()
    blinker.blink("orange")


def resume():
    global audio_playback_ref
    if not audio_playback_ref:
        return
    audio_playback_ref.resume()
    blinker.blink("blue")


def set_media_file(_):
    # Set new file whenver fileID changes
    clear_all_media()
    fl_info = fileInfo.get()

    if fl_info[2] == 0:  # Music File
        global audio_playback_ref
        fldr_loc = CONFIG_DATA.folder_loc.replace("/", "\\")
        loc = f'{fldr_loc}\\'+fl_info[0].replace("/", "\\")
        audio_playback_ref = Playback(loc)
        audio_playback_ref.play()
        audio_playback_ref.loop_at_end(True)

    blinker.blink("brown", 1000)


fileID.add_callback(set_media_file)
