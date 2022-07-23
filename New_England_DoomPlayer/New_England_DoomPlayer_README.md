**Final Project Title: “New England DoomPlayer”**

**Final Project Demonstration Video:**
<https://www.dropbox.com/s/zvk0de05p8c3mbo/DoomPlayer-Demo.mp4?dl=0>

*Instructions*

How to Meet Your Doom:

-   Users may implement this application to select a location from the New
    England Doom Map on the second tab. The application will search for bands
    within a 25-mile radius, increasing that radius as necessary to find a
    sufficient number of artists. Finally, the program will output a custom
    playlist of local artists appearing on Bandcamp.com and display it in the
    user’s default web browser.

1.  To begin, the user should enter a name for a new playlist in the first tab
    and click on the Submit button. (Users who fail to do so will receive the
    default title of “DoomPlayer Playlist.”)

2.  The user should then click on the “New England Doom Map” tab and right-click
    on any geographic location within the New England area depicted in the
    Google Maps interface provided by the program.

3.  The user should select the “Find Bands Near Here” option from the context
    menu.

4.  The user should wait a few seconds as the program queries static JSON data,
    performs complex distance calculations, and sends requests to Bandcamp.com.

5.  Finally, the program will save the playlist to an HTML file (using either
    the user-provided or default filename) and open that file in the user’s
    default web browser.

6.  The playlist file will allow the user to sample tracks from artists located
    near the selected geographic location. To play each file, the user should
    left-click on the appropriate play button next to each track in the
    playlist.

7.  The user may repeat this search-and-generate-playlist process ad infinitum.

*Python Modules/Program Dependencies and Other Resources*

Bandcamp.json:

-   A static file prepared by the program author and accessed by the program to
    simulate the dynamic retrieval of JSON data via the Bandcamp API in the
    absence of necessary Bandcamp API features.

codecs: <https://docs.python.org/3/library/codecs.html>

-   This module allows the program to decode bytes to text when opening an HTML
    file in the user’s default web browser.

json: <https://docs.python.org/3/library/json.html>

-   This module allows the program to parse and query the Bandcamp.json file.

numpy: <https://numpy.org/doc/stable/>

-   This module is necessary to do complex calculations of distance using
    longitude and latitude coordinates returned by the TkinterMapView object
    accessing the Google Maps API.

PIL (Python Imaging Library):
<https://www.omz-software.com/pythonista/docs/ios/PIL.html>

-   This library provides additional support for handling images and image
    formats in Python, e.g., the Portable Network Graphics (png) format.

random: <https://docs.python.org/3/library/random.html>

-   This module is required to perform pseudo-random number operations.

re: <https://docs.python.org/3/library/re.html>

-   This module is required to perform queries using regular expressions.

ssl: <https://docs.python.org/3/library/ssl.html>

-   This module is required to perform secure HTTP requests to Bandcamp.com for
    webscraping purposes.

tkinter: <https://docs.python.org/3/library/tkinter.html>

-   This module provides many of the widgets necessary to construct the
    program’s GUI.

tkinter.messagebox: <https://docs.python.org/3/library/tkinter.messagebox.html>

-   This module provides a template class for producing pop-up messages in
    Python.

tkinter.ttk: <https://docs.python.org/3/library/tkinter.ttk.html>

-   This resource provides support for themed Tkinter widgets, specifically,
    Notebooks.

tkintermapview: <https://github.com/TomSchimansky/TkinterMapView>

-   This resource provides a widget for displaying and interacting with Google
    Maps in a Tkinter GUI.

urllib.error: <https://docs.python.org/3/library/urllib.error.html>

-   This library provides exception classes that may result due to
    urllib.request operations.

urllib.parse: <https://docs.python.org/3/library/urllib.parse.html>

-   This library analyzes URLs and breaks them down into their components.

urllib.request: <https://docs.python.org/3/library/urllib.request.html>

-   This library provides Python functionality for opening URLs.

webbrowser: <https://docs.python.org/3/library/webbrowser.html>

-   This library provides support for controlling external web browsers in
    Python.

  
*Future Work*

First and foremost, any future work on this type of application would be greatly
enhanced by the availability of a more public, more robust API from
Bandcamp.com. As of this writing, the author is forced to make use of static
JSON and webscraping methods to extract the information necessary to produce
playlists with embedded player (widget) functionality. Communication from a
Bandcamp.com representative alluded to the availability of that API access at
some unspecified future time. Moreover, accessing the Bandcamp API directly
might help alleviate any synchronous request problems the application currently
experiences on an inconsistent basis. Alternatively, I could pursue the
functionality that the aiohttp and asyncio Python libraries afford to perform
HTTP/S requests asynchronously.

The GUI for the program is relatively basic. I could foresee serious
improvements in the user’s interface, including possibly using a completely
different GUI package. Making those improvements would allow users greater ease
of use with, e.g., the Google maps interface facilitated by tkintermapview. For
instance, I would like to make it possible for users to clear all markers placed
on the map. As of this writing, I have not determined the best way to make this
happen.

I could also foresee expanding the scope of the program to include more musical
genres/subgenres. Finding local artists of any stripe can be equally
challenging, so there may prove to be a need for the program to adopt a broader
purview. Of course, this type of increased granularity would be facilitated by
access to the Bandcamp API.

Should I decide to feature this application in a programming portfolio, I might
consider rewriting it in other languages (e.g., Java, JavaScript) to improve its
portability and marketability. Because it makes demands on Bandcamp.com
resources, perhaps the most responsible implementation of New England DoomPlayer
would be as a web-hosted application that uses its own API key and makes
requests from a consistent IP address instead of encouraging numerous users to
download individual client versions of the program.
