from winsound import PlaySound
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
from playsound import playsound
from pytube import YouTube
import subprocess
# import multiprocessing

cred = credentials.Certificate("jukebox-b9a7b-firebase-adminsdk-veljx-3fb3a3b9b6.json")
default_app = firebase_admin.initialize_app(cred)

# Setup Google Cloud Key - The json file is obtained by going to
# Project Settings, Service Accounts, Create Service Account, and then
# Generate New Private Key

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "jukebox-b9a7b-firebase-adminsdk-veljx-b81c85b943.json"

# Use the application default credentials. The projectID is obtianed
# by going to Project Settings and then General.

# cred = credentials.ApplicationDefault()
# firebase_admin.initialize_app(cred, {
#  'projectId': 'testing',
# })

db = firestore.client()

def get_quote():
    data_quote = {"quote" : "#BRINGSOBEBACK", "author" : "Chris Vang"}
    return data_quote

def add_song_to_list(the_list):
    result_input = input("What song would you like to add? ")
    the_list.append(result_input)
    return the_list

def remove_song_from_list(the_list, val = 0):
    the_list.pop(val)
    return the_list

def menu():
    print("1. Add song")
    print("2. Play next queued song")
    print("3. Remove song from queue")
    print("4. Quit the Program")

def add_song(doc_list, a_new_list):
    a_new_list = add_song_to_list(a_new_list)
    doc_list.set({"list" : a_new_list})
    print(f"List with: {a_new_list} was successful!")

#2. Work on getting the youtube videos.

#playsound('sounds\level_up.wav')

# Work on Cohesion TODO
# TODO Fix hardcoding

def youtube_director(link):
    filename = save_youtube_song(link)
    convert_song(filename)
    play_youtube_song(filename + ".wav")
    delete_youtube_file(filename)

def convert_song(old_file):
    
    subprocess.call(['ffmpeg', '-i', f'{old_file}.mp3', f'{old_file}.wav'])
    # old_file = old_file + ".mp3"
    # new_file = old_file + ".wav"

def play_youtube_song(file):
    playsound(file)

def delete_youtube_file(file):

    #os.remove(file + ".wav")
    os.remove(file + ".mp3")
    

def save_youtube_song(link):
    #link = "https://www.youtube.com/watch?v=fm5kiVEklGA"

    # Short link
    # https://www.youtube.com/watch?v=QNXvE1BZu8g
    # link = input("Please add YouTube link: ")

    try: 
        # object creation using YouTube
        # which was imported in the beginning 
        yt = YouTube(link) 
    except: 
        print("Connection Error") #to handle exception 

    video = yt.streams.filter(only_audio=True).first()

    # download the file
    out_file = video.download()
    
    # save the file
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)

    print(yt.title + " has been successfully downloaded.")

    return base
  
# result of success

def main():

    a_new_list = []
    doc_list = db.collection(u"sampleData").document(u"list_stuff")
    result = doc_list.get()
    if result.exists:
        data = result.to_dict()
        a_new_list = data["list"]

    ask_menu = True
    while ask_menu:
        print(data['list'])
        menu()
        user_response = int(input("Which uption would you like: "))
        if user_response == 1:
            add_song(doc_list, a_new_list)
        elif user_response == 2:
            youtube_director(data["list"][0])
            a_new_list = remove_song_from_list(data["list"])
            doc_list.set({"list" : a_new_list})
        elif user_response == 3:
            for i in range(0, len(data["list"])):
                print(f"{i+1}. {data['list'][i]}")
            choice = int(input("Which song would you like to remove? ")) - 1
            a_new_list = remove_song_from_list(data["list"], choice)
            doc_list.set({"list" : a_new_list})
        elif user_response == 4:
            ask_menu = False


main()
# Resources:
# https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/
# https://www.geeksforgeeks.org/working-with-wav-files-in-python-using-pydub/
# https://www.geeksforgeeks.org/download-video-in-mp3-format-using-pytube/

# Future Resources:
# Firebase Cloud Storage: Python tutorial [Learn everything in 17 minutes]
# https://www.youtube.com/watch?v=zGGq3kBedR8


# Additional Personal Project Resource:
# https://www.geeksforgeeks.org/how-to-play-a-spotify-audio-with-python/