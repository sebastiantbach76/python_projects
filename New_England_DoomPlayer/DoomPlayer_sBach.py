# Assignment: Final Project: Completion
# Description: Write a program that demonstrates many of the Python concepts covered this semester.
# Type "python DoomPlayer_sBach.py" at a command prompt to execute the program.
# File Name: DoomPlayer_sBach.py
# Citations:
# 1. Haversine Formula in Python Using numpy: https://towardsdatascience.com/calculating-the-distance-between-two-locations-using-geocodes-1136d810e517
# 2. Severance, Charles. Python for Everybody, Chapter 12
# Author: Sebastian Bach
# Student ID: 00332111
# Course: CIS 153 - Programming for Information Technology
# Section: LT8
# Instructor: Professor Penta
# Semester: Spring 2022
# Date: 2 May 2022

import codecs
import json
import random
import re
import ssl
import tkinter.messagebox
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from tkinter import *
from tkinter.ttk import Notebook

import numpy
from PIL import ImageTk, Image
from tkintermapview import TkinterMapView


def submitFilename():   # Replaces spaces in playlist name with underscores, appends file extension, and stores as global variable.
    global playlistFileName
    userInput = filenameEntry.get()
    tempList = userInput.split(' ')
    file = '_'.join(tempList) + ".html"
    playlistFileName = file


def add_marker_event(mapcoords):  # Places marker on the New England Doom Map and passes selected map coordinates to getJSONCoords().
    print("Add marker:", mapcoords)
    new_marker = map_widget.set_marker(mapcoords[0], mapcoords[1], text="Find Bands Near Here")
    getJSONCoords(mapcoords)


def getJSONCoords(coords: tuple):
    # Prepare lists for appending to later.
    cands25 = []
    cands50 = []
    cands75 = []
    cands100 = []
    with open("./Bandcamp.json", "r") as JSONFile:  # Open Bandcamp.json file and parse it as JSON using Python json package functions.
        JSONstring = JSONFile.read()

    bcJSON = json.loads(JSONstring)
    for cand in bcJSON:  # Iterate through JSON file contents to find coordinate pairs.
        coordTuple = bcJSON[cand]['coords']
        dist = calcDistance(coords[0], coordTuple[0], coords[1], coordTuple[1])  # Call calcDistance() to calculate distances between user-selected location and band locations.
        if float(dist) <= 25.0:  # Append song URLs from bands located within various radii from the user-selected location.
            cands25.append(bcJSON[cand]['songURLs'])
        elif 25.0 < float(dist) <= 50.0:
            cands50.append(bcJSON[cand]['songURLs'])
        elif 50.0 < float(dist) <= 75.0:
            cands75.append(bcJSON[cand]['songURLs'])
        elif 75.0 < float(dist) <= 100.0:
            cands100.append(bcJSON[cand]['songURLs'])

    if len(cands25) >= 3:   # Make certain JSON query captures minimum number of hits to make playlists at least marginally diverse.
        assemblePlaylistURLs(cands25)
    elif len(cands50) >= 3:
        assemblePlaylistURLs(cands50)
    elif len(cands75) >= 3:
        assemblePlaylistURLs(cands75)
    elif len(cands100) >= 3:
        assemblePlaylistURLs(cands100)
    else:  # If application receives no hits within 100-mile radius of user-selected location, notify user and break chain of function calls with return.
        tkinter.messagebox.showwarning("Alas! DOOM!", "The location you have selected doesn't seem to have any DOOM for miles.  Please select a new location and try again.")
        return


def calcDistance(lat1, lat2, long1, long2):  # Takes two pairs of coordinates and calculates distance between the points using the haversine formula.  Inspired by https://towardsdatascience.com/calculating-the-distance-between-two-locations-using-geocodes-1136d810e517
    radius = 3950  # radius of the Earth in miles

    phi1 = numpy.radians(lat1)
    phi2 = numpy.radians(lat2)

    delta_phi = numpy.radians(lat2 - lat1)
    delta_lambda = numpy.radians(long2 - long1)

    a = numpy.sin(delta_phi / 2) ** 2 + numpy.cos(phi1) * numpy.cos(phi2) * numpy.sin(delta_lambda / 2) ** 2  # a represents half the chord length between two points.

    c = 2 * numpy.arctan2(numpy.sqrt(a), numpy.sqrt(1 - a))  # c represents the angular distance between two points (in radians).

    dist = radius * c

    return f'{dist:.2f}'


def assemblePlaylistURLs(urls: list):   # Creates final list of playlist widget URLs.
    playListURLs = []
    for url in urls:
        playListURLs.append(random.choice(url))

    assemblePlaylist(playListURLs)


def assemblePlaylist(urlsList: list):
    global playlistFileName

    widgetList = []
    for url in urlsList:  # Pass all URLs contained in urlslist 
        widgetList.append(bandcampScraper(url))

    try:
        playlistFileHandler = open(playlistFileName, 'w')
    except NameError:
        playlistFileName = "DoomPlayer_Playlist.html"
        playlistFileHandler = open(playlistFileName, 'w')

    # Format HTML for output.
    htmlString = ["<html><body bgcolor=\"#000000\"><div align=\"center\"><img src=\"./DoomPlayer_header.png\"></div><div style=\"color: #00e600; text-align: center; font-family: Impact; font-size: 40px; font-weight: 800;\">" + revertFileName(playlistFileName) + "</div>"]

    for widget in widgetList:
        if widget != "":
            htmlString.append(widget)

    htmlString.append("</body></html>")

    for item in htmlString:  # Output playlist to HTML file.
        playlistFileHandler.write(item)
    playlistFileHandler.close()

    openPlaylist = codecs.open(playlistFileName, 'r', 'utf-8')  # Open playlist in default web browser.

    webbrowser.open(playlistFileName)


def bandcampScraper(url: str):  # Extracts hidden album and track codes by scraping relevant Bandcamp.com web page source code and returns string with properly formatted Bandcamp player widget HTML code.  Uses code supplied by Professor Charles Severance in his book, Python for Everybody, Chapter 12.
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    html = urllib.request.urlopen(url, context=ctx).read()
    album = re.findall(b'[0-9]{8,}(?=">go to album)', html)
    track = re.findall(b'(?:[0-9]){7,}(?=,&quot;tralbum)', html)

    widgetString = []
    try:
        widgetString = "<iframe style=\"border: 0; width: 100%; height: 42px;\" src=https://bandcamp.com/EmbeddedPlayer/album=" + album[0].decode() + "/size=small/bgcol=333333/linkcol=e99708/track=" + track[0].decode() + "/transparent=true/ seamless></iframe>"
    except:
        widgetString = ""

    return widgetString


def revertFileName(file: str):   # Reverses the operations performed in submitFilename() function and returns original user-submitted string.
    file = file.rstrip("html")
    file = file.rstrip('.')
    splitList = file.split('_')
    revertedFile = ' '.join(splitList)
    return revertedFile


root = Tk()  # Begin GUI assembly.
root.geometry('600x760')
root.configure(bg="#000000")
root.title("New England DoomPlayer")
root.resizable(width=False, height=False)
icon = PhotoImage(file="DoomPlayer_icon.png")
root.iconphoto(True, icon)
canvas = Canvas(root, width=600, height=160)
canvas.configure(bg="#000000")
canvas.pack()
img = ImageTk.PhotoImage(Image.open("DoomPlayer_header.png"))
canvas.create_image(0, 0, anchor=NW, image=img)
DoomMap = Notebook(root)
DoomMap.place(x=0, y=160, width=600, height=600)

tab1 = Frame(DoomMap, relief=SOLID)
tab1.configure(bg='#000000')
instructHeader = Label(tab1, width=400, height=400, bg="#000000", fg="#00e600")
instructHeader.configure(font=["Impact", 18], anchor=NW)
instructHeader.place(x=10, y=10, width=450, height=50)
instructBody = Label(tab1, width=450, height=100, bg="#000000", fg="#ffffff")
instructBody.configure(font=["Impact", 13], anchor=NW, wraplength="550", justify="left")
instructBody.place(x=10, y=50, width=550, height=300)
filenameLabel = Label(tab1, width=200, height=25, bg="#000000", fg="#ffffff")
filenameLabel.configure(font=["Impact", 13], anchor=NW, justify="left", text="Playlist Name: ")
filenameLabel.place(x=10, y=240, width=100, height=25)
filenameEntry = Entry(tab1, bg="#ffffff", fg="#000000", width=250, font="Times")
filenameEntry.place(x=120, y=240, width=250, height=25)
submitFilename = Button(tab1, text="Submit (to your Fate!)", font=["Impact", 13], bg="#9900ff", fg="#00e600", height=25, command=submitFilename)
submitFilename.configure(activebackground="#00e600", activeforeground="#9900ff")
submitFilename.place(x=380, y=240, height=25)
finalInstructs = Label(tab1, width=550, height=100, bg="#000000", fg="#ffffff")
finalInstructs.configure(font=["Impact", 13], anchor=NW, wraplength="550", justify="left", border=0, borderwidth=0)
finalInstructs.place(x=10, y=280, width=550, height=300)
tab1.place(x=0, y=0, width=600, height=600)
DoomMap.add(tab1, text="Local Artist Playlist")

tab2 = Frame(DoomMap, relief=SOLID)
tab2.configure(bg='#000000')
tab2.place(x=0, y=0, width=600, height=600)
DoomMap.add(tab2, text="New England Doom Map")

# Create map widget and add to GUI tab 2.
map_widget = TkinterMapView(tab2, width=600, height=580, corner_radius=0)
map_widget.pack(fill="x", expand=True)

# Define what happens when the user right-clicks on the map.
map_widget.add_right_click_menu_command(label="Find Bands Near Here", command=add_marker_event, pass_coords=True)

# Specify Google as the map tile server, set a center location for the map view (Portsmouth), and adjust map zoom to frame New England region.
map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", tile_size=256, max_zoom=19)
map_widget.set_address("Portsmouth, NH", marker=False)
map_widget.set_zoom(6.8)

# Initialize filename and set instruction strings as text appearing on three different labels in the GUI.
fileName = ""

instructHeaderText = "Welcome to New England DoomPlayer!"
instructHeader.configure(text=instructHeaderText)

instructBodyText = "How to Meet Your Doom:\nYou may use this application to select a location from the map on the next tab. The application will then search for bands within a 25-mile radius, increasing that radius as necessary to find a sufficient number of artists. Finally, the program will output a custom playlist of local artists appearing on Bandcamp.com and display it in your default web browser.\nTo begin, enter a name for your new playlist below and click on the Submit button."
instructBody.configure(text=instructBodyText)

finalInstructsText = "Use the \"New England Doom Map\" tab to select a geographic location by right-clicking on the map and choosing \"Search for Bands Near Here\" from the context menu. After doing so, please be patient as the program runs some complex calculations and network queries. Like all good doom metal, this program can be SLLLLLLOOOOOOOOOOOWWW..."
finalInstructs.configure(text=finalInstructsText)

root.mainloop()
