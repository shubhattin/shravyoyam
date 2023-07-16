from tkinter import Frame, Label, Tk


class Blinker:
    def __init__(self, root: Tk):
        self.__root: Tk = root
        self.__root.wm_withdraw()
        self.__root.overrideredirect(True)
        self.__root.geometry("+20+5")
        self.__root.attributes("-topmost", True)

        self.__color_frame = Frame(self.__root, highlightbackground="purple",
                                   highlightthickness=10)
        Label(self.__color_frame, text="     ").pack()
        self.__color_frame.pack()

        # Blink on Init
        def callback():
            self.blink("green", 3000)
            self.__root.after(1500, lambda: self.blink("blue", 1500))
        self.__root.after(1, callback)

    def blink(self, color:str, tm=500):
        def callback():
            self.__root.wm_deiconify()
            self.__color_frame.configure(highlightbackground=color)
            self.__root.after(tm, lambda: self.__root.wm_withdraw())
        self.__root.after(1, callback)
