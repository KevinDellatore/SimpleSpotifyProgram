#General Python imports ------------------------------------------------------------
import json
import time
import requests
#---------------------------------------------------------------------------------------


# The imports and code below are simply the module/library imports and authization steps to allow the API's to work. 
# Both LyricsGenius and Spotify require the developer to create a app and register it into their database before they're able to access the API
# The long strings of numbers and letters are the tokens and keys.
#  
#LyricsGenius API Client Setup ---------------------------------------------------------
import lyricsgenius
genius = lyricsgenius.Genius("KyM2MSXLVwE9eshWFs1hFmaWOORT767FxbrxE3aOmRQaIcDXCkf2dlJ7ZIKOkqOb")
# --------------------------------------------------------------------------------------



#Spotify API Client Setup --------------------------------------------------------------
import spotipy
import spotipy.util as util
import spotipy.oauth2
from spotipy.oauth2 import SpotifyClientCredentials

clientID = input("Enter your Spotify Developer Client ID: ")
clientSecret = input("Enter your Spotify Developer Client Secret ID: ")
sp = spotipy.Spotify(auth_manager = SpotifyClientCredentials(client_id= clientID, client_secret= clientSecret))

auth_token = util.prompt_for_user_token('0wziiken1rg3foo686e932ske','playlist-read-private',client_id= clientID,client_secret= clientSecret ,redirect_uri='http://google.com/')

# --------------------------------------------------------------------------------------






# This function previously used the Lyrics Genius api to print out an artists top 5 most populat songs at any given time, 
# but, I figured that using the spotify API for this function would fit better as it takes listen data vs the number of people looking up
# the lyrics for a given song / artist. 
def popularSongs():
    artistInput = input("Please provide an artist to search: ")
    print('\n' + "Searching Artists discography by popularity....." + '\n')
    time.sleep(2)
    print("Top 5 Popular songs by", artistInput, '\n', "------------------------------------------")
    results = sp.search(q= artistInput, limit=5) #Spotipy search function takes artist input
    for idx, track in enumerate(results['tracks']['items']): #enumerates the results from the search and prints them to the terminal 
        print(idx+1,")", track['name'])



# This uses the LyricsGenius api to search and grab lyrics of a song. There is no way to input an incorrect artist or song name as the api will,
# assuming that its connected to the LyricsGenius server properly, always return a song. I tried with many different combinations 
# both fake and real and I always got something
def findLyrics():
    genius.verbose = False #disables the genius auto generated text.
    artistInput = input("Please provide the artist name, be exact!: ")
    print("Searching for songs by", artistInput)
    artist = genius.search_artist(artistInput, max_songs = 0) #uses genius api to search for artist 
    print("Done, artist found!")
    genius.verbose = True #reenables the genius auto generated text.
    songInput = input("Please Enter a Song Name to get lyrics: ")
    song = artist.song(songInput) #searches the artists discogrpahy for the song
    print('\n') 
    print(song.lyrics) #uses api to print the lyrics for the song


#This function use the spotify api to generate a list of reccomendations based on a desired genre or artist. It uses json (mainly cause the tutorials used it)
# but the json files query and grab the results from spotify and then print them out into the terminal nicely. These json files could later be used 
# to generate an actual playlist for the user, but since I am running this on my own account and tokens, I've decided to omit that part for my own sake.
def generateRecs():

    endpoint_url = "https://api.spotify.com/v1/recommendations?"
    recChoice = input("Would you like to generate choices by favorite Artist or Genre? ")
    limit=10
    market="US"
    uris = []

    if recChoice == "artist" or recChoice == "Artist" or recChoice == "ARTIST":
        artist_name = input("What is your favorite artist or band?")
        artist_info = sp.search(q = artist_name, limit=50, offset=0, type='artist', market='US') #uses spotipy to search for the artist
        artist_id = artist_info['artists']['items'][0]['id'] #searches through the output to get the ID of the artist 

        time.sleep(1)
        print('\n',"Generating Recommendations based on",artist_name,". . .")
        time.sleep(1)

        seed_artists = artist_id 
        #querys
        query = f'{endpoint_url}limit={limit}&market={market}&seed_artists={seed_artists}'
        response = requests.get(query,headers={"Content-Type":"application/json","Authorization":f"Bearer {auth_token}"})

        json_response = response.json() # the above few lines create a filter for the query into the spotify API, this one puts the response into a json file

        for i,j in enumerate(json_response['tracks']): #enumerates through the json file and appends the songs into a list and prints the list.
            uris.append(j['uri'])
            print(f"{i+1}) \"{j['name']}\" by {j['artists'][0]['name']}")


    elif recChoice == "genre" or recChoice == "Genre" or recChoice == "GENRE":
        genreInput = input("Whats your favorite genre? ")
        time.sleep(1)
        print('\n',"Generating Recommendations by genre. . .")
        time.sleep(1)

        query = f'{endpoint_url}limit={limit}&market={market}&seed_genres={genreInput}'
        response = requests.get(query,headers={"Content-Type":"aplication/json","Authorization":f"Bearer {auth_token}"})
        json_response = response.json() # These lines do the same as above but for genre 

        for i,j in enumerate(json_response['tracks']):
            uris.append(j['uri'])
            print(f"{i+1}) \"{j['name']}\" by {j['artists'][0]['name']}")


    else:
        print("Sorry, thats not an option, try again") #simply detects when the input is invalid
        generateRecs()

    print("\n")
    recEndinput = input("Do you want to search again or headback to the main menu? ")
    if recEndinput == "Main Menu" or recEndinput == "Menu":
        print("\n")
        MainMenu()
    elif recEndinput == "back" or recEndinput == "search again":
        print("\n")
        generateRecs()
    
 
#Simple menu function that lets the user know what options they can pick. There is also an option to quit the entire program. If an 
# invalid option is selected the user it notified and promted to try again.
def MainMenu():
    print("--------WELCOME--------")
    time.sleep(2)
    selection = input(""" 
Welcome to my Music Program! 

Select a function you would like to use!

1. Get the top Songs by an Artist

2. Find the Lyrics of a Song

3. Get song recommendations by genre or similar to your favorite artist

4. Quit

    """)
    if selection == "1":
        popularSongs() 
    elif selection == "2":
        findLyrics()
    elif selection == "3":
        generateRecs()
    elif selection == "4":
        exit
    else:
        print("Thats not a recognized input, please enter another ")
        print()
        MainMenu()


MainMenu()