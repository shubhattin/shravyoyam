from app_state import blinker, blinker_root, chalitah, media_refs, fileID


def clear_all_media(clear_file_id=True):
    if media_refs.audio:  # For audio
        media_refs.audio.stop()
        media_refs.audio = None
    elif media_refs.video:  # For video
        media_refs.video.kill()
        media_refs.video = None
    if clear_file_id:
        fileID.set("")

def pause():
    if not media_refs.audio:
        return
    media_refs.audio.pause()
    blinker.blink("orange")


def resume():
    if not media_refs.audio:
        return
    media_refs.audio.resume()
    blinker.blink("blue")


def close_app():
    blinker.blink("red")
    clear_all_media()

    blinker_root.after(500, blinker_root.destroy)


def stop_media_playback():
    if not chalitah.get():
        return
    clear_all_media()
    blinker.blink("purple", 700)
