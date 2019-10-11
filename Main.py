import tkinter as tk #Changing the reference to tk.Label instead of Label
import os, sys, re
try:
    import requests, imageio, pafy
    from lxml import html
    import lxml.html.clean 
    from bs4 import BeautifulSoup
    print ("All Files found")
except ImportError: #Goes through the pip installer for each module since once is missing
    os.system("cmd /c pip install requests")
    os.system("cmd /c pip install lxml")
    os.system("cmd /c pip install beautifulsoup4")
    os.system("cmd /c pip install pafy")
    os.system("cmd /c sudo pip install youtube-dl")
    os.system("cmd /c pip install imageio")
    import requests, pafy, sys, imageio
    from lxml import html
    import lxml.html.clean 
    from bs4 import BeautifulSoup
    print ("Missing Libraries Installed")

class app():
    def __init__(self):
        self.root = tk.Tk()
        self.root.configure(bg = 'white')
        self.full_Width, self.full_Height  = self.root.winfo_screenwidth(), self.root.winfo_screenheight() # Settings general widths and heights for 16:9 and 16:10 screens
        self.root.geometry('%dx%d+0+0' % (self.full_Width, self.full_Height)) 
        self.width1, self.height1 = int(round((self.root.winfo_screenwidth() / 15))), int(round((self.root.winfo_screenheight() / 15))) #General widths and heights to be used for widgets
        self.width2, self.height2 = int(round((self.root.winfo_screenwidth() / 20))), int(round((self.root.winfo_screenheight() / 20))) 
        self.width3, self.height3 = int(round((self.root.winfo_screenwidth() / 25))), int(round((self.root.winfo_screenheight() / 25))) 
        self.width4, self.height4 = int(round((self.root.winfo_screenwidth() / 30))), int(round((self.root.winfo_screenheight() / 30)))
        self.width5, self.height5 = int(round((self.root.winfo_screenwidth() / 45))), int(round((self.root.winfo_screenheight() / 45)))
        self.frame = tk.Frame(self.root, bg = 'white')
        self.frame.pack()
        self.Main()

    def Main(self):
        self.frame.pack_forget() #Resets the frame to be used again
        self.frame = tk.Frame(self.root, bg = 'white')
        self.frame.pack()
        tk.Label(self.frame, font=("", self.height1),text="Project Python Search Engine", bg='white').pack()
        tk.Label(self.frame, font=("", self.height1),text="", bg='white').pack()
        tk.Label(self.frame, font=("", self.height2),text="Song", bg='white').pack()
        tk.Label(self.frame, font=("", self.height4),text="", bg='white').pack()
        t = tk.Entry(self.frame, font=("", self.height3), bg='white', width = 50)
        t.pack()
        tk.Label(self.frame, font=("", self.height4),text="", bg='white').pack()
        tk.Button(self.frame, text='Search', font = ("Helvetica", self.height4), command= lambda:self.Retrieve_Input(t)).pack()
        tk.Button(self.frame, text="Latest Popular Songs", font = ("Helvetica", self.height4), command=lambda:self.Popular_Songs()).pack(pady = self.height4) #Line 210 onwards
        self.root.bind('<Return>', lambda x: self.Retrieve_Input(t)) #Binds the return button

    def MyScrollControl(self, canvas, width, height): #Canvas Scroll Controller
        canvas.configure(scrollregion=canvas.bbox("all"),width=width, height = height) #Allows Scrolling for multiple sized canvases
        canvas.update() 

    def Retrieve_Input(self, t):
        self.page = requests.get("https://www.google.com/search?q=" + t.get() + ":genius")
        soup = BeautifulSoup(self.page.content,features="lxml")
        links =  soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")) #Grabs all links
        self.finalList = []
        for link in links:
            if "genius.com" in re.split(":(?=http)",link["href"].replace("/url?q=",""))[0]:
                self.finalList.append(str(re.split(":(?=http)",link["href"].replace("/url?q=","")))) #Splits any remaining html such as href

        try: #Trys to open the lyrics page if found
            if self.finalList[0].split("&")[0][2:] == "https://genius.com/":
                self.error_box(t)
            elif "https://genius.com/artists/" in self.finalList[0].split("&")[0][2:]: #If the search was an artist
                self.page = self.finalList[0].split("&")[0][2:]
                self.Artist_Return()
            else:
                self.Lyric_Return()
        except IndexError: #No song / artitst found in the search
            self.error_box(t)
            
    def Artist_Return(self):
        url = self.page
        page = requests.get(self.page)
        webpage = html.fromstring(page.content)
        links = []
        links.append(str(webpage.xpath('//a/@href'))) #Grabs external links, in this case it's the artist's songs
        popular_songs = []
        final_songs = []
        for x in links:
            popular_songs.extend(x.split(","))
        popular_songs = popular_songs[:-35] #Removes the first few links such as www.genius.com and www.genius.com/#featured-stories etc
        for x in popular_songs:
            if "lyrics" in x: #Grabs songs associated with the artist
                final_songs.append(x.replace(" ","").replace("'",""))
        soup = BeautifulSoup(page.text,features="lxml")
        artist_info = []
        for p in soup.find_all('p'): #Grabs the information about the artist
            artist_info.append(p.text)
        soup = BeautifulSoup(page.text, 'html.parser')
        img_tags = soup.find_all('img')
        urls = [img['src'] for img in img_tags] #Grabs the album cover's image source link
        self.Download(urls, 4)
        final_songs = final_songs[:11] #Grabs the first 10 songs (Most popular)
        self.frame.pack_forget()
        self.frame = tk.Frame(self.root, bg = 'white')
        self.frame.pack()
        return_frame = tk.Frame(self.frame, bg='white')
        return_frame.pack(side=tk.BOTTOM)
        tk.Label(self.frame, text = url.replace("_"," ").replace("https://genius.com/artists/","").title(), font=("Helvetica", self.height3), bg= 'white').pack()
        tk.Label(self.frame, text = "", font=("Helvetica", int(self.height4/5)), bg = 'white').pack()
        play_song_frame = tk.Frame(self.frame, bg='white')
        play_song_frame.pack(side = tk.RIGHT)
        tk.Label(play_song_frame, text = "", font=("Helvetica", int(self.height4)), bg = 'white', fg = 'white').pack()
        for x in final_songs:
            tk.Label(play_song_frame, text = "", font=("Helvetica", int(self.height4/5)), bg = 'white').pack()
            tk.Button(play_song_frame, text = "▶ Play Song", font=("Helvetica", int(self.height4/2.25)), width = 12, command = lambda song = x: self.Play_Reroute(song)).pack()
        popular_song_frame = tk.Frame(self.frame, bg='white')
        popular_song_frame.pack(side = tk.RIGHT)
        tk.Label(popular_song_frame, text = "Popular Songs", font=("Helvetica", int(self.height4)), bg = 'white').pack()
        for x in final_songs:
            tk.Label(popular_song_frame, text = "", font=("Helvetica", int(self.height4/5)), bg = 'white').pack()
            tk.Label(popular_song_frame, text = x.replace("https://genius.com/","").replace("-", " ").replace("lyrics","").title(), font=("Helvetica", int(self.height4/2.25)),
                    width = int(self.width4/1.5), bg = 'white').pack(padx =((self.width4/6), (self.width4/6)), pady = (0, (self.width4/6)))
        width, height =self.root.winfo_screenwidth()/1.60, int(self.full_Height/1.4)
        artist_info_frame = tk.Frame(self.frame, bg='white')
        artist_info_frame.pack(side=tk.LEFT)                           
        scroll_frame = tk.Frame(artist_info_frame, bg = 'white')
        scroll_frame.pack(side=tk.LEFT)    
        convoCanvas=tk.Canvas(scroll_frame, bg='white')
        convoframe=tk.Frame(convoCanvas, bg='white')
        myscrollbar=tk.Scrollbar(scroll_frame, orient="vertical",command=convoCanvas.yview)
        convoCanvas.configure(yscrollcommand=myscrollbar.set)
        myscrollbar.pack(side="right",fill="y")
        convoCanvas.pack(side=tk.LEFT)
        convoCanvas.create_window((0,0),window=convoframe, anchor='nw')
        convoframe.bind("<Configure>", lambda event, canvas=convoCanvas:self.MyScrollControl(convoCanvas, width, height))
        cover_art_frame = tk.Frame(convoframe, bg = "white")
        cover_art_frame.pack()
        tk.Label(cover_art_frame, text = "Album Cover Arts", font = ("Helvetica", int(self.height4)), bg = 'white').pack()
        tk.Label(cover_art_frame, text = "", font=("Helvetica", int(self.height4/5)), bg = 'white').pack()
        images = []
        for x in range(1, 4): #Changes the images to a gif because jpg isn't support by tk.Label unless you install another external library (PIL)
            images.append(imageio.imread("temp" + str(x) + ".jpg"))
            imageio.mimsave("temp" + str(x) + '.gif', images)
            os.remove("temp" + str(x) + ".jpg")
            images = []
            photo = tk.PhotoImage(file="temp" + str(x) + '.gif')
            label = tk.Label(cover_art_frame, image=photo)
            label.image = photo # keeps a reference of the image so it isn't removed during garbage collection
            label.pack(side=tk.LEFT, padx = self.width4)
        tk.Message(convoframe, text = "\nArtist Info \n\n" + str(artist_info).replace("[","").replace("]","").replace("'",''),
                   bg = "white", font = ("Helvetica", int(self.height4 / 2)), width = self.root.winfo_screenwidth()/1.85).pack()
        tk.Label(convoframe, text = "", font=("Helvetica", int(self.height4/5)), bg = 'white').pack()
        tk.Button(return_frame, text = "Return", bg = "white", font = ("", int(self.height4 / 1.5)), width = 12, command = lambda:self.Main()).pack(pady = self.height4)

    def Download(self, urls, limit):
        file_name  = "temp/temp.jpg"
        counter = 1
        for x in range(0, limit):
            get_response = requests.get(urls[x],stream=True)
            with open("./temp" + str(counter) + ".jpg", 'wb') as f:
                for chunk in get_response.iter_content(chunk_size=1024):
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
            counter  = counter  + 1

    def Play_Reroute(self, song): #Allows me to reuse the Lyirc_Return function without having to another function that does the same thing
        self.finalList = []
        self.finalList.append(song.replace("-"," "))
        self.Play_Song()
        
    def Lyric_Reroute(self, song): #Allows me to reuse the Lyirc_Return function without having to another function that does the same thing
        self.finalList = []
        self.finalList.append(" " + song)
        self.Lyric_Return()

    def Lyric_Return(self):
        page = requests.get(self.finalList[0].split("&")[0][2:]) #search is a song
        soup = BeautifulSoup(page.content,features="lxml")
        temp = lxml.html.clean.clean_html(str(soup.p))
        self.lyrics = re.sub('<.*?>', '', temp)
        self.frame.pack_forget()
        self.frame = tk.Frame(self.root, bg = 'white')
        self.frame.pack()
        width, height = self.root.winfo_screenwidth()/1.01, int(self.full_Height/1.30)
        scroll_frame = tk.Frame(self.frame, bg = 'white') #Creating a Scrollable frame
        scroll_frame.pack(side=tk.TOP)    
        convoCanvas=tk.Canvas(scroll_frame, bg='white')
        convoframe=tk.Frame(convoCanvas, bg='white')
        myscrollbar=tk.Scrollbar(scroll_frame, orient="vertical",command=convoCanvas.yview)
        convoCanvas.configure(yscrollcommand=myscrollbar.set)
        myscrollbar.pack(side="right",fill="y")
        convoCanvas.pack(side=tk.TOP)
        convoCanvas.create_window((0,0),window=convoframe, anchor='nw')
        convoframe.bind("<Configure>", lambda event, canvas=convoCanvas:self.MyScrollControl(convoCanvas, width, height))
        tk.Message(convoframe, text = self.lyrics, bg = "white", font = ("", int(self.height4 / 2))).pack() #Lyrics place into the scroll frame
        tk.Button(self.frame, text = "▶ Play Song", bg = "white", font = ("", int(self.height4 / 2)), command = lambda:self.Play_Song()).pack(side=tk.TOP)
        tk.Label(self.frame, text =self.finalList[0].split("&")[0][2:][19:].replace("-"," ").replace("lyrics",""), bg = "white", font = ("", self.height4)).pack(side=tk.TOP)
        tk.Button(self.frame, text = "Return", bg = "white", font = ("", int(self.height4 / 2)), command = lambda:self.Main()).pack(side=tk.TOP)
        tk.Label(self.frame, font=("", int(self.height4 / 4)),text="", bg='white').pack(side=tk.BOTTOM)

    def Play_Song(self):
        page = requests.get("https://www.youtube.com/results?search_query=" + self.finalList[0].split("&")[0][2:][19:]) #Searching youtube for the song requested
        soup = BeautifulSoup(page.content,features="lxml")
        links =  soup.find_all("a")
        youtubeList = []
        for link in links:
            if "/watch?v=" in re.split(":(?=http)",link["href"].replace("/url?q=",""))[0]:
                youtubeList.append(str(re.split(":(?=http)",link["href"].replace("/url?q=",""))))
        url = "https://www.youtube.com" + youtubeList[0].replace('"', "").replace("[","").replace("]","").replace("'","")
        video = pafy.new(url) #Creates an object pafy can use
        best = video.getbest() #Gets for the best resoloution of the video
        playurl = best.url
        os.startfile(playurl)

    def error_box(self, t):
        errorBox =  tk.Toplevel(bg = 'white')
        errorBox.wm_title("Error")
        tk.Label(errorBox, text = "'" + t.get().title() + "' not found please try different keywords", font = ("", self.height5), fg = 'red', bg = 'white').pack(pady = self.height4)
        tk.Button(errorBox, text = "Return", bg = 'white', font = ("", self.height5), command = lambda:errorBox.destroy()).pack()
                  
my_gui = app()
