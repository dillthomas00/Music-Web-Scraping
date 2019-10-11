############
#Needs Cleaning-Up
############

import tkinter as tk #Changing the reference to tk.Label instead of Label
import tkinter.ttk as ttk
import os, sys, re, json
import vlc
from Utils.tkmarquee import Marquee
##import requests, pafy
##os.system("cmd /c pip install lxml")
##from lxml import html
##import lmxl.html.clean 
##from bs4 import BeautifulSoup
##from PIL import Image, ImageTk
try:
    import requests, pafy
    from lxml import html
    import lmxl.html.clean 
    from bs4 import BeautifulSoup
    from PIL import Image, ImageTk
    print ("All Files found")
except ImportError: #Goes through the pip installer for each module since once is missing
    import requests, pafy
    from lxml import html
    import lxml.html.clean 
    from bs4 import BeautifulSoup
    from PIL import Image, ImageTk
    print ("Missing Libraries Installed")
    
class app():
    def __init__(self):
        self.root = tk.Tk()
        self.root.configure(bg = '#252525')
        self.full_Width, self.full_Height  = self.root.winfo_screenwidth(), self.root.winfo_screenheight() # Settings general widths and heights for 16:9 and 16:10 screens
        self.root.geometry('%dx%d+0+0' % (self.full_Width, self.full_Height)) 
        self.width1, self.height1 = int(round((self.root.winfo_screenwidth() / 15))), int(round((self.root.winfo_screenheight() / 15))) #General widths and heights to be used for widgets
        self.width2, self.height2 = int(round((self.root.winfo_screenwidth() / 20))), int(round((self.root.winfo_screenheight() / 20))) 
        self.width3, self.height3 = int(round((self.root.winfo_screenwidth() / 25))), int(round((self.root.winfo_screenheight() / 25))) 
        self.width4, self.height4 = int(round((self.root.winfo_screenwidth() / 30))), int(round((self.root.winfo_screenheight() / 30)))
        self.width5, self.height5 = int(round((self.root.winfo_screenwidth() / 45))), int(round((self.root.winfo_screenheight() / 45)))
        self.width6, self.height6 = int(round((self.root.winfo_screenwidth() / 60))), int(round((self.root.winfo_screenheight() / 60)))
        self.navbar_Frame = tk.Frame(self.root, bg = "#201F21", width = self.full_Width / 5)
        self.navbar_Frame.pack(anchor = tk.W, fill = tk.Y, expand = False, side = tk.LEFT)
        self.content_Frame = tk.Frame(self.root, bg = "#252525")
        self.content_Frame.pack(anchor = tk.N, fill = tk.BOTH, expand = True, side = tk.LEFT)
        tk.Label(self.navbar_Frame, bg = "#201F21").pack(pady = self.height1)
        self.home_Button = tk.Button(self.navbar_Frame, text = "Home", bg = "#201F21", fg = "white", relief = tk.FLAT, font = ("Garamond", self.height5, "bold"), command = lambda: self.ScreenClear("self.Main()")).pack(pady = self.height6, padx = self.width2)
        self.featured_Button = tk.Button(self.navbar_Frame, text = "Featured", bg = "#201F21", fg = "white", relief = tk.FLAT, font = ("Garamond", self.height5, "bold"), command = lambda: self.ScreenClear("self.Featured()")).pack(pady = self.height6, padx = self.width2)
        self.radio_Button = tk.Button(self.navbar_Frame, text = "Radio", bg = "#201F21", fg = "white", relief = tk.FLAT, font = ("Garamond", self.height5, "bold"), command = lambda:self.ScreenClear("self.Radio()")).pack(pady = self.height6, padx = self.width2) 
        self.about_Button = tk.Button(self.navbar_Frame, text = "About", bg = "#201F21", fg = "white", relief = tk.FLAT, font = ("Garamond", self.height5, "bold")).pack(pady = self.height6, padx = self.width2)
        self.ScreenClear("self.Main()")
        

    def ScreenClear(self, next_window):
        self.content_Frame.pack_forget()
        eval(next_window)

    def MyScrollControl(self, canvas, width, height): #Canvas Scroll Controller
        canvas.configure(scrollregion=canvas.bbox("all"),width=width, height = height) #Allows Scrolling for multiple sized canvases
        canvas.update() 

    ############
    #Main / Search Section
    ############
    def Main(self):
        self.content_Frame = tk.Frame(self.root, bg = "#252525")
        self.content_Frame.pack(anchor = tk.N, fill = tk.BOTH, expand = True, side = tk.LEFT)
        tk.Label(self.content_Frame, text="Project Python Spotify Engine", bg='#252525', fg = 'white', font = ("Garamond", self.height5, "bold")).pack(pady = self.height5)
        tk.Label(self.content_Frame, text="Powered by Genius", bg='#252525', fg = 'white', font = ("Garamond", self.height6, "bold")).pack(pady = self.height5)
        search_Frame = tk.Frame(self.content_Frame, bg = '#252525')
        search_Frame.pack(side = tk.TOP, pady = (0, self.height6))
        t = tk.Entry(search_Frame, font=("", self.height3), bg='white', width = self.width6)
        t.pack(side = tk.LEFT)
        search_Button = tk.Button(search_Frame, text='Search', font = ("Helvetica", self.height5), bg = "#252525", fg = "white", command= lambda:self.Retrieve_Input(t))
        search_Button.pack(side = tk.LEFT)
        try:
            with open(".//Assets//search_history.txt", 'r') as f:
                width, height = (self.full_Width / 2.25), (self.full_Height / 3)
                scroll_Canvas=tk.Canvas(self.content_Frame, bg = '#252525')
                scroll_Frame=tk.Frame(scroll_Canvas, bg = '#252525')
                scrollbar=ttk.Scrollbar(scroll_Frame, orient = "vertical", command = scroll_Canvas.yview)
                scroll_Canvas.configure(yscrollcommand = scrollbar.set)
                scrollbar.pack(side = "right", fill = "y")
                scroll_Canvas.pack()
                scroll_Canvas.create_window((0,0), window = scroll_Frame, anchor = 'nw')
                scroll_Frame.bind("<Configure>", lambda event, canvas = scroll_Canvas:self.MyScrollControl(scroll_Canvas, width, height))
                scroll_Frame_Inner = tk.Frame(scroll_Frame, bg = "#252525")
                scroll_Frame_Inner.pack()
                for line in f:
                    tk.Button(scroll_Frame_Inner, text = line, font = ("Helvetica", self.height5), bg = "#252525", fg = "white", relief = tk.FLAT, width = self.width5).pack()
        except FileNotFoundError:
            history_Frame = tk.Frame(self.content_Frame, bg = '#252525')
            history_Frame.pack()
            tk.Label(history_Frame, text = "No Recent Searches Made", font = ("Helvetica", self.height5), bg = "#252525", fg = "white", width = self.width5).pack()
            

    ############
    #Radio Section
    ############
    def Radio(self):
        self.content_Frame = tk.Frame(self.root, bg = "#252525")
        self.content_Frame.pack(side = tk.TOP)
        tk.Label(self.content_Frame, text="Project Python Spotify Engine", bg='#252525', fg = 'white', font = ("Garamond", self.height5, "bold")).pack(pady = self.height5)
        tk.Label(self.content_Frame, text="Powered by Genius", bg='#252525', fg = 'white', font = ("Garamond", self.height6, "bold")).pack(pady = self.height5)


        
        with open(".//Assets//Radio//stations.json") as slist:
            self.station_list = json.load(slist)
        self.stations = []
        for x in self.station_list:
            self.stations.append(x)
        self.vlcins = vlc.Instance()
        self.vlcplayer = self.vlcins.media_player_new()
        self.vlcmedia = 0
        self.toggle_pla = 1  # play/Stop toggle
        print (os.listdir(".//Assets//Radio//"))
        self.var = tk.StringVar()
        self.var.set(self.stations[0])
        self.cover_art_string = self.stations[0].replace(" ","_")
        
        for x in self.stations:
            tk.Button(self.content_Frame, text = x, bg = "#252525", fg = "white", relief = tk.FLAT, font = ("Garamond", self.height6, "bold"), width = 15, command=lambda var = x: self.play_media(var, self.toggle_pla)).pack()
        photo = ImageTk.PhotoImage(Image.open('.//Assets//Radio//Capital.png'))
        label = tk.Label(self.content_Frame, image=photo)
        label.image = photo
        label.pack(pady = self.height6)
        self.play_Button = tk.Button(self.content_Frame, text="Play", font = ("Garamond", self.height6, "bold"), width=5)
        self.play_Button.pack()
        self.mqe01 = Marquee(self.content_Frame, text="No Radio Selected")
        self.mqe01.config(width = self.width1 * 2)
        self.mqe01.pack(pady = self.height6)

    def play_media(self, media, toggle_value):
        self.var.set = media
        self.vlcmedia = self.vlcins.media_new(self.station_list[media])
        self.vlcplayer.set_media(self.vlcmedia)
        self.vlcplayer.audio_set_volume(70)
        self.vlcplayer.play()
        self.vlcmedia.parse()
        self.toggle_pla = 0
        self.play_Button.config(text="Stop")
        self.update_song()


    def update_song(self):
        """Change song label on play."""
        def update_song():
            """Update song label every 1000 ms."""
            marquee_text = f"{self.var.get()} - {self.vlcmedia.get_meta(12)}"
            self.mqe01.itemconfig(self.mqe01.find_withtag("text"),
                                  text=marquee_text)
            self.mqe01.after(1000, update_song)
        update_song()

























    ############
    #Needs Finishing
    ############
    def Featured(self):
        print ("Has reached here")
        page = requests.get("https://genius.com/#top-songs")
        webpage = html.fromstring(page.content)
        links = []
        links.append(str(webpage.xpath('//a/@href')))
        temp_links = []
        Songs = []
        for x in links: #Grabs all links
            temp_links.extend(x.split(","))
        temp_links = temp_links[:-35] #Removes the first few links such as www.genius.com and www.genius.com/#featured-stories etc
        counter =  0
        for x in temp_links:
            x = x.strip().replace("'","")[-6:]
            if "lyrics" in x:
                Songs.append(temp_links[counter].replace("'",""))
            counter = counter + 1
        for x in Songs:
            page = requests.get("https://www.google.co.uk/search?tbm=isch&q=" + x)
            soup = BeautifulSoup(page.content, "html.parser")
            img_tags = soup.find_all("img")
            urls = [img['src'] for img in img_tags]
            self.Download(urls, 1, ".//Assets//Featured//")
        width, height = (self.full_Width / 1.28), (self.full_Height/1.4)
        colour = ["", "#FFDF00", "#D3D3D3", "#cd7f32"] #Gold, Silver, Bronze
        counter = 1
        
        self.content_Frame = tk.Frame(self.root, bg = "#252525")
        self.content_Frame.pack(anchor = tk.N, fill = tk.BOTH, expand = True, side = tk.LEFT)
        tk.Label(self.content_Frame, text="Project Python Spotify Engine", bg='#252525', fg = 'white', font = ("Garamond", self.height5, "bold")).pack(pady = self.height5)
        tk.Label(self.content_Frame, text="Powered by Genius", bg='#252525', fg = 'white', font = ("Garamond", self.height6, "bold")).pack(pady = self.height5)        
        scroll_Canvas=tk.Canvas(self.content_Frame, bg = '#252525')
        scroll_Frame=tk.Frame(scroll_Canvas, bg = '#252525')
        scrollbar=ttk.Scrollbar(scroll_Frame, orient = "vertical", command = scroll_Canvas.yview)
        scroll_Canvas.configure(yscrollcommand = scrollbar.set)
        scrollbar.pack(side = "right", fill = "y")
        scroll_Canvas.pack(side = tk.LEFT, padx = (self.width6, 0))
        scroll_Canvas.create_window((0,0), window = scroll_Frame, anchor = 'nw')
        scroll_Frame.bind("<Configure>", lambda event, canvas = scroll_Canvas:self.MyScrollControl(scroll_Canvas, width, height))
        scroll_Frame_Inner = tk.Frame(scroll_Frame, bg = "#252525")
        scroll_Frame_Inner.pack()
        while counter != 11:
            if counter <= 3:
                tk.Label(scroll_Frame_Inner, text = "♚", bg = '#252525', fg = colour[counter], font = ("", int(self.height4 / 1.5), "bold")).grid(row = counter, column = 0, padx = (0, self.width6))
            else:
                tk.Label(scroll_Frame_Inner, text = str(counter) + ".)", fg = 'white', bg = '#252525', font = ("", int(self.height4 / 2))).grid(row = counter, column = 0, padx = (0, self.width6))
            photo = ImageTk.PhotoImage(Image.open(".//Assets//Featured//" + str(counter) + ".png"))
            label = tk.Label(scroll_Frame_Inner, image=photo)
            label.image = photo
            label.grid(row = counter, column = 1, padx = (0, self.width6))
            tk.Button(scroll_Frame_Inner, text = "⏯", fg = 'white', bg = '#252525', font = ("", int(self.height5)), command = lambda song = x: self.Play_Reroute(song), width = 2, relief = tk.FLAT).grid(row = counter, column= 2, padx = (0, self.width6))
            tk.Button(scroll_Frame_Inner, text = Songs[counter-1].replace("https://genius.com/", "").replace("-lyrics", "").replace("-", " ").title(), fg = 'white', bg = '#252525', font = ("", int(self.height6), "bold"), relief = tk.FLAT, width = self.width3, anchor = tk.W,
                      command = lambda song = x: self.Lyric_Reroute(song)).grid(row = counter, column = 3)
            counter = counter + 1

    def Download(self, urls, limit, file_Structure):
        for x in range(0, limit):
            try:
                file_num = len(os.listdir(file_Structure)) + 1
            except FileNotFoundError:
                os.mkdir(file_Structure)
                file_num = 1
            get_response = requests.get(urls[x],stream=True)
            with open(file_Structure + str(file_num) + ".png", 'wb') as f:
                for chunk in get_response.iter_content(chunk_size=1024):
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)             
            updated_image = Image.open(file_Structure + str(file_num) + ".png")
            updated_image = updated_image.resize((120, 120), Image.ANTIALIAS)
            updated_image.save(file_Structure + str(file_num) + ".png")
            

my_gui = app()
