"""
Streaming Radio GUI.
A tk-based streaming radio GUI that gets a station list from a local JSON file.
Requires VLC Player to be installed as well. Match 32-bit or 64-bit based on
what Python is using.
"""
from tkinter import Tk, Label, PhotoImage, Button, EW, W
from tkinter import StringVar, OptionMenu
from tkmarquee import Marquee
import vlc, json

class App(Tk):
    """App class to create Tk application."""

    def __init__(self):
        """__init__ for class App."""
        Tk.__init__(self)
        self.ico_data = """
        iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB
        6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAwFBMVEUAAADXACjYACfYACf/AADZAC
        bYACfYACfYACfYACfYACfZACbSAC3YACfZACbXACjYACfVACvfACDYACfaACXWACnWACnXACjjABzaA
        CbXACjXACjYACfYACfYACfYACfXACjXACjYACf/AADXACjYACfYACfYACfYACfXACjXACjYACfYACfY
        ACfYACfMADPYACfYACfYACfYACfZACbYACfYACfZACbMADPYACfYACfYACfYACfZACbYACcAAACgArq
        SAAAAPnRSTlMAE+J3Ayj6zBpP2dQR6aBs+RgI/ksfLI4JREZzLna8rGZHJwGh0pel4TpgnUJ8DQXA8a
        hpeLj9hgpWnuTTjHLCzmIAAAABYktHRACIBR1IAAAACXBIWXMAAA3XAAAN1wFCKJt4AAAAB3RJTUUH4
        gUeDwwj6vDGtgAAAH1JREFUGNNjYIACRiZmFgZkwGrHxs6BKsDJxc2IIsDKw8uHKsDALyCIKiAkLIIq
        IGonhiogziuBIiCJrAMkICUNZcvIyskrKNopQbnKKsKqauoadkAzIEDTTgtEacMFFIV1QJSugB5UQN/
        A0MjYxNTMHG6+haWVtY2tJJQHAGzhDAAfR9YmAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDE4LTA1LTMwVD
        E1OjEyOjM1KzAyOjAwnc8SpgAAACV0RVh0ZGF0ZTptb2RpZnkAMjAxOC0wNS0zMFQxNToxMjozNSswM
        jowMOySqhoAAAAZdEVYdFNvZnR3YXJlAHd3dy5pbmtzY2FwZS5vcmeb7jwaAAAAAElFTkSuQmCC
        """

        with open("stations.json") as slist:
            self.station_list = json.load(slist)

        self.stations = [x for x in self.station_list]
        print (self.stations)
        self.vlcins = vlc.Instance()
        self.vlcplayer = self.vlcins.media_player_new()
        self.vlcmedia = 0
        self.toggle_pla = 1  # play/Stop toggle

        self.title("Radio Streamer")
        self.ico = PhotoImage(data=self.ico_data)
        self.tk.call("wm", "iconphoto", self._w, self.ico)
        self.overrideredirect(True)
        self.attributes("-topmost", 1)
        self.resizable(width=False, height=False)
        self.minsize(width=207, height=53)
        self.maxsize(width=207, height=53)

        self.var = StringVar(self)
        self.var.set(self.stations[0])
        amt_of_stations = len(self.stations)
        self.opm1 = OptionMenu(self, self.var, *self.stations)
        self.opm1.grid(column=1, row=0, sticky=EW)

        self.btn01 = Button(self, text="P")
        self.btn01.config(width=1, command=lambda:
                          self.play_media(self.var.get(), self.toggle_pla))
        self.btn01.grid(column=2, row=0, sticky=W)
        self.btn02 = Button(self, text="X")
        self.btn02.config(width=1, command=lambda: self.destroy())
        self.btn02.grid(column=3, row=0, sticky=W)

        self.grip = Label(self, text="--")
        self.grip.grid(column=0, row=0, sticky=W)
        self.grip.bind("<ButtonPress-1>", self.move_start)
        self.grip.bind("<ButtonRelease-1>", self.move_stop)
        self.grip.bind("<B1-Motion>", self.move_go)

        self.mqe01 = Marquee(self, text="")
        self.mqe01.config(width=201)
        self.mqe01.grid(column=0, row=1, columnspan=4, sticky=W)

    def move_start(self, event):
        """Use to measure starting postion."""
        self.x = event.x
        self.y = event.y

    def move_stop(self, event):
        """Use to clear position data."""
        self.x = None
        self.y = None

    def move_go(self, event):
        """Use when dragging the window."""
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry("+%s+%s" % (x, y))

    def play_media(self, media, toggle_value):
        """Play media from dropdown selection of opm1."""
        if toggle_value == 1:
            self.vlcmedia = self.vlcins.media_new(self.station_list[media])
            self.vlcplayer.set_media(self.vlcmedia)
            self.vlcplayer.audio_set_volume(70)
            self.vlcplayer.play()
            self.vlcmedia.parse()
            self.toggle_pla = 0
            self.btn01.config(text="S")
            self.update_song()
        else:
            self.vlcplayer.stop()
            self.toggle_pla = 1
            self.btn01.config(text="P")

    def update_song(self):
        """Change song label on play."""
        def update_song():
            """Update song label every 1000 ms."""
            marquee_text = f"{self.var.get()} - {self.vlcmedia.get_meta(12)}"
            self.mqe01.itemconfig(self.mqe01.find_withtag("text"),
                                  text=marquee_text)
            self.mqe01.after(1000, update_song)
        update_song()


if __name__ == "__main__":
    radio = App()
    radio.mainloop()
