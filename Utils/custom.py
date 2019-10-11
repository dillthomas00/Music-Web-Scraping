from tkinter import Tk, Label, PhotoImage, Button, EW, W
from tkinter import StringVar, OptionMenu
from tkmarquee import Marquee
import vlc, json

class App(Tk):
    def __init__(self):
        Tk.__init__(self)

        with open("stations.json") as slist:
            self.station_list = json.load(slist)
        self.stations = []
        for x in self.station_list:
            self.stations.append(x)
        self.vlcins = vlc.Instance()
        self.vlcplayer = self.vlcins.media_player_new()
        self.vlcmedia = 0
        self.toggle_pla = 1  # play/Stop toggle

        self.var = StringVar(self)
        self.var.set(self.stations[0])
        self.opm1 = OptionMenu(self, self.var, *self.stations)
        self.opm1.grid(column=1, row=0, sticky=EW)

        self.play_Button = Button(self, text="P", width=1, command=lambda: self.play_media(self.var.get(), self.toggle_pla))
        self.play_Button.grid(column=2, row=0, sticky=W)
        self.mqe01 = Marquee(self, text="No Radio Selected")
        self.mqe01.config(width=150)
        self.mqe01.grid(column=0, row=1, columnspan=4, sticky=W)

    def play_media(self, media, toggle_value):
        """Play media from dropdown selection of opm1."""
        if toggle_value == 1:
            self.vlcmedia = self.vlcins.media_new(self.station_list[media])
            self.vlcplayer.set_media(self.vlcmedia)
            self.vlcplayer.audio_set_volume(70)
            self.vlcplayer.play()
            self.vlcmedia.parse()
            self.toggle_pla = 0
            self.play_Button.config(text="S")
            self.update_song()
        else:
            self.vlcplayer.stop()
            self.toggle_pla = 1
            self.play_Button.config(text="P")

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
