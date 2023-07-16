from pystray import MenuItem, Menu, Icon as SysTray
from PIL import Image
from kry import pause, resume, close_app, stop_media_playback
from app_state import dattAMsh, fileID


def start_taskbar():
    systray:SysTray = SysTray(
        "Lipi Lekhika",
        Image.open("./icon.ico"),
        "श्रव्योऽयम्",
        get_menu_options(),
    )

    def update_menu(_):
        systray.menu = get_menu_options()
    fileID.add_callback(update_menu)
    systray.run_detached()


def get_menu_options():
    file_items: str = ""
    datt = dattAMsh.get()
    file_id = fileID.get()

    for x in datt:
        dt = datt[x]
        file_items += f"""MenuItem(
            "{("🎵" if dt[2]==0 else "📀")} {dt[1]} - {x}",
            lambda _: fileID.set("{x}"),
            checked=lambda _: "{file_id}" == "{x}",
            radio=True
        ),"""
    files_menu: Menu = eval(f"Menu({file_items})")
    menu = Menu(
        MenuItem("📂 श्रव्याणि", files_menu),
        MenuItem("▶️ Pause", lambda _: pause()),
        MenuItem("⏸ Resume", lambda _: resume()),
        MenuItem("⏹ Stop", lambda _: stop_media_playback()),
        MenuItem("❌ Close", lambda _: close_app()),
    )
    return menu
