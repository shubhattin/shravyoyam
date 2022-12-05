import shubhlipi as sh
import os
import dotenv
from getpass import getpass

dotenv.load_dotenv(".env_karah.local")


def get_git_key():
    global GIT_KEY
    if not GIT_KEY:
        KEY = os.getenv("GIT_KEY")
        if not KEY:
            print("Set 'GIT_KEY' in .env_karah.local")
            exit(-1)
        key = getpass("key = ")
        try:
            GIT_KEY = sh.decrypt_text(KEY, key)
        except:
            print("Wrong key!")
            exit(-1)
    return GIT_KEY


GIT_KEY = None
for x in sh.argv:
    if x == "build":
        sh.start_thread(
            lambda: print(
                "\nPrettier beutify: {0}".format(
                    "Success"
                    if sh.cmd("pnpm format", display=False)[0] == 0
                    else "Fail"
                )
            )
        )
        sh.cmd("pnpm build", direct=False)
    elif x == "avahar":
        if os.path.isdir("build_apk"):
            sh.delete_folder("build_apk")
        sh.makedir("build_apk")
        sh.download_file(
            "https://github.com/shubhattin/shravyoyam/releases/download/bin/shravyoyam.apk",
            "build_apk/shravyoyam.apk",
        )
    elif x == "build_apk":
        pth = str(sh.parent(__file__))+r"\build_apk\shravyoyam.apk"
        sh.extract(pth, pth[:-4])
        sh.delete_file(pth)
        sh.delete_folder(pth[:-4] + r"\assets\www")
        sh.copy_folder("build", pth[:-4] + r"\assets\www")
        sh.delete_folder(pth[:-4] + r"\META-INF")
        sh.cmd(
            f'"{sh.tool}\\7zip\\7za.exe" a -tzip -mx9 -r "{pth[:-4]}.zip" "{pth[:-4]}\\*" -y',
            display=False,
        )
        sh.delete_folder(pth[:-4])
        sh.zipalign_apk(f"{pth[:-4]}.zip", pth)
        sh.delete_file(f"{pth[:-4]}.zip")
        sh.sign_apk(pth, "shubham", getpass("sign key = "))
    elif x == "test":
        adb = f"{sh.tool}\\android\\adb.exe"
        sh.cmd(f"{adb} install build_apk/shravyoyam.apk")
        sh.cmd(
            f"{adb} shell pm grant lasa.shravya android.permission.READ_EXTERNAL_STORAGE"
        )
        sh.cmd(
            f"{adb} shell monkey -p lasa.shravya -c android.intent.category.LAUNCHER 1",
            display=False,
        )
    elif x == "upload_apk":
        sh.upload_release_file(
            "build_apk\\shravyoyam.apk",
            "shubhattin/shravyoyam",
            "bin",
            get_git_key(),
        )
    elif x == "clear":
        sh.delete_folder("dist")
        sh.delete_folder("build_apk")
