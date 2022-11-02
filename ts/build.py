import shubhlipi as sh, os
from getpass import getpass
import dotenv

dotenv.load_dotenv(".env_karah.local")

for x in sh.argv:
    if x == "build":
        sh.cmd("pnpm karah", direct=False)
        dir = os.listdir("out")
        for x in dir:
            tp = x.split(".")[-1]
            if tp == "html":
                f = sh.read(f"out/{x}")
                f = f.replace('href="/', 'href="./')
                f = f.replace('src="/', 'src="./')
                sh.write(f"out/{x}", f)
        for lc in ["out/_next/static/chunks/pages", "out/_next/static/chunks"]:
            dir = os.listdir(lc)
            for x in dir:
                if lc == "out/_next/static/chunks" and (
                    "framework" in x or "polyfills" in x
                ):
                    continue
                tp = x.split(".")[-1]
                if tp == "js":
                    f = sh.read(f"{lc}/{x}")
                    f = f.replace("/_next/", "./_next/")
                    sh.write(f"{lc}/{x}", f)
    elif x == "avahar":
        if os.path.isdir("build_apk"):
            sh.delete_folder("build_apk")
        sh.makedir("build_apk")
        sh.download_file(
            "https://github.com/shubhamudi/shravyoyam/releases/download/bin/shravyoyam.apk",
            "build_apk/shravyoyam.apk",
        )
    elif x == "build_apk":
        pth = sh.parent(__file__) + "\\build_apk\\shravyoyam.apk"
        sh.extract(pth, pth[:-4])
        sh.delete_file(pth)
        sh.delete_folder(pth[:-4] + r"\assets\www")
        sh.copy_folder("out/", pth[:-4] + r"\assets\www")
        sh.delete_folder(pth[:-4] + r"\META-INF")
        sh.cmd(
            f'"{sh.tool}\\7zip\\7za.exe" a -tzip -mx9 -r "{pth[:-4]}.zip" "{pth[:-4]}\\*" -y',
            display=False,
        )
        sh.delete_folder(pth[:-4])
        sh.zipalign_apk(f"{pth[:-4]}.zip", pth)
        sh.delete_file(f"{pth[:-4]}.zip")
        sh.sign_apk(pth, "shubham", sh.from_base64(os.environ["SIGN_KEY"]))
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
            "ofsfobnelip/shravyoyam",
            "bin",
            sh.from_base64(os.getenv("GIT_KEY")),
        )
    elif x == "clear":
        sh.delete_folder("out")
        sh.delete_folder("build_apk")
