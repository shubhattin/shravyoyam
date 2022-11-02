from threading import Thread
from time import sleep, time
from audioplayer import AudioPlayer
from keyboard import on_press_key, add_hotkey, on_release_key
from tkinter import Label, Tk, Frame
from os import kill
from winregistry import WinRegistry
import psutil
from win32gui import GetWindowText, GetForegroundWindow
from win32process import GetWindowThreadProcessId
from subprocess import Popen


class kAryaM:
    def __init__(self):
        self.__pUrva = WinRegistry().read_entry(
            "HKCU\\SOFTWARE\\shravyo'yam", "sthAnam").value
        self.__pUrva = self.__pUrva.split("?")
        self.paristhAnam = self.__pUrva[0]
        self.paristhAnam = self.paristhAnam.replace("\\", "/")
        file = open(self.paristhAnam+"/saYc.js", mode="r+", encoding="utf-8")
        dattAMsh = file.read()
        file.close()
        self.__key = ""
        self.__chalitaH = False
        dattAMsh = dattAMsh[dattAMsh.index("{"): dattAMsh.index("}") + 1]
        dattAMsh = eval(dattAMsh)
        self.__dattAMsh = dattAMsh
        self.__lasan = False
        self.__esc_pressed = False
        r = ""
        for x in dattAMsh:
            r += x
        r = "".join(list(set(r)))
        for x in r:
            on_press_key(
                x, lambda st: self.__kuYjikAsandesham_prayAsi(st.name, True))
        on_press_key(
            "shift", lambda st: self.__kuYjikAsandesham_prayAsi(st.name, True))

        self.__a = ""
        self.shravya = False
        self.__time = time()
        self.__kunj = False
        add_hotkey("control+up+down",
                   lambda: self.__kuYjikAsandesham_prayAsi("punarchalan"))
        add_hotkey(
            "left+right", lambda: self.__kuYjikAsandesham_prayAsi("vishramatu"))
        add_hotkey("windows+f12",
                   lambda: self.__kuYjikAsandesham_prayAsi("muchyate"))
        add_hotkey("windows+f11",
                   lambda: self.__kuYjikAsandesham_prayAsi("vimuchyate"))
        add_hotkey("windows+f8",
                   lambda: self.__kuYjikAsandesham_prayAsi("kunj_muchyate"))
        add_hotkey("windows+f9",
                   lambda: self.__kuYjikAsandesham_prayAsi("kunj_vimuchyate"))
        add_hotkey("windows+shift",
                   lambda: self.__kuYjikAsandesham_prayAsi("vichalan"))
        add_hotkey("windows+f10",
                   lambda: self.__kuYjikAsandesham_prayAsi("lasatu"))
        on_press_key(
            "end", lambda d: self.__kuYjikAsandesham_prayAsi("kunj_prakriyA"))
        on_press_key(
            "esc", lambda d: self.__kuYjikAsandesham_prayAsi("kunj_prakriyA"))

        def df():
            self.__esc_pressed = False
        on_release_key("esc", lambda s: df())
        on_release_key("end", lambda s: df())
        self.__listen = False
        self.__msg = ""
        th = Thread(target=self.__recieve_sansesh)
        th.daemon = True
        th.start()
        self.__r = Tk()
        self.__r.wm_withdraw()
        self.__r.overrideredirect(True)
        self.__r.geometry("+20+5")
        self.__r.attributes("-topmost", True)
        self.b = Frame(self.__r, highlightbackground="purple",
                       highlightthickness=10)
        Label(self.b, text="     ").pack()
        self.b.pack()
        add_hotkey("windows+esc+control", lambda:
                   self.__kuYjikAsandesham_prayAsi("close"))
        add_hotkey("windows+f4",
                   lambda: self.__kuYjikAsandesham_prayAsi("signal"))

        def gh():
            self.__change_color("green", 3000)
            self.__r.after(1500, lambda: self.__change_color("blue", 1500))
        self.__r.after(1, gh)
        self.__r.mainloop()

    def __kuYjikAsandesham_prayAsi(self, n, key=False):
        self.__msg = ("~" if key else "") + n

    def __recieve_sansesh(self):
        while True:
            if self.__msg != "":
                if self.__msg[0] == "~":
                    self.__kuYjikA(self.__msg[1:])
                elif self.__msg == "muchyate":
                    self.__chalitaH = True
                    self.__shravyachAlakam("kUjanam")
                elif self.__msg == "vimuchyate":
                    self.__lasan = False
                    self.__nirdesh_pAlanam("vichalan")
                    self.__chalitaH = False
                elif self.__msg == "kunj_muchyate":
                    self.__change_color("green")
                    self.__kunj = True
                elif self.__msg == "kunj_vimuchyate":
                    self.__change_color("red")
                    self.__kunj = False
                elif self.__msg == "close":
                    self.__change_color("red")
                    self.__r.after(1, self.__clear_all)
                    self.__r.after(500, self.__r.destroy)
                elif self.__msg == "signal":
                    self.__change_color("purple")
                elif self.__msg == "kunj_prakriyA" and not self.__esc_pressed:
                    self.__esc_pressed = True
                    if self.__kunj:
                        self.__vinashatu()
                else:
                    self.__nirdesh_pAlanam(self.__msg)
                self.__msg = ""
            sleep(0.1)

    def __clear_all(self):
        try:
            self.__a.close()
        except:
            pass
        try:
            self.kl.terminate()
        except:
            pass

    def __kuYjikA(self, k):
        t = time()
        if self.__listen:
            if t-self.__time >= 3.0:
                self.__listen = False
                self.__key = ""
                return
            if "shift" in k:
                self.__shravyachAlakam("lasatu")
            elif not(k.isascii() and len(k) == 1):
                self.__listen = False
                self.__key = ""
            else:
                self.__key += k
                self.__time = t

    def __nirdesh_pAlanam(self, msg):
        if self.__chalitaH:
            if msg == "vichalan":
                if not self.__lasan:
                    self.__shravyachAlakam("vichalan")

            elif msg == "lasatu":
                self.__listen = True
                self.__key = ""
                self.__change_color("blue", 1000)
                self.__time = time()
            elif msg == "vishramatu":
                self.__shravyachAlakam("vishramatu")
                self.__lasan = False
            elif msg == "punarchalan":
                self.__shravyachAlakam("punarchalan")
        elif msg == "vichalan":
            if not self.__lasan:
                self.__shravyachAlakam("vichalan")

    def __shravyachAlakam(self, n, i=True):
        if i:
            self.__r.after(1, lambda: self.__shravyachAlakam(n, False))
            return
        if n == "vishramatu":
            try:
                if self.shravya:
                    self.__a.pause()
                    self.__change_color("orange")
            except:
                pass
        elif n == "punarchalan":
            try:
                if self.shravya:
                    self.__a.resume()
                    self.__change_color("blue")
            except:
                pass
        elif n == "vichalan":
            try:
                if self.shravya:
                    self.__a.close()
                    self.__change_color("black")
                else:
                    self.kl.terminate()
            except:
                pass
        elif n in ("lasatu", "kUjanam"):
            if n == "kUjanam":
                self.__change_color("green")
            else:
                # if True:
                try:
                    m = self.__dattAMsh[self.__key]
                    if m[2] == 0:
                        self.__clear_all()
                        self.__a = AudioPlayer(
                            self.paristhAnam+"\\" + m[0].replace("/", "\\"))
                        self.__a.play(loop=True)
                        self.shravya = True
                    elif m[2] == 1:
                        self.__clear_all()
                        self.shravya = False
                        asf = r'"{0}" "{1}"'.format(
                            self.__pUrva[1].replace("/", "\\"), self.__pUrva[0]+"\\" + m[0].replace("/", "\\"))
                        self.kl = Popen(asf)

                    self.__change_color("brown", 1000)
                except:
                    pass

            self.__listen = False
            self.__key = ""

    def __change_color(self, color, t=500):
        def gh():
            self.__r.wm_deiconify()
            self.b.configure(highlightbackground=color)
            self.__r.after(t, lambda: self.__r.wm_withdraw())
        self.__r.after(1, gh)

    def __vinashatu(self):
        for proc in psutil.process_iter():
            n = self.__vartamAna_sakriya_koShTha_prakriyAnAma()
            try:
                name = proc.name()
                id = proc.pid
                if n == name:
                    a = proc.parents()
                    b = False
                    if len(a) == 0:
                        b = True
                    elif a[0].name() == "explorer.exe":
                        b = True
                    try:
                        if b:
                            kill(id, 9)
                    except:
                        pass
            except:
                pass

    def __vartamAna_sakriya_koShTha_prakriyAnAma(self):
        try:
            pid = GetWindowThreadProcessId(GetForegroundWindow())
            n = psutil.Process(pid[-1]).name()
            return n
        except:
            pass

    def __vartamAna_sakriya_koShTha_nAma(self):
        return GetWindowText(GetForegroundWindow())


kAryaM()
