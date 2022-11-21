import shutil
from pytube import YouTube, Playlist
import moviepy.editor
import os
import pandas as pd
import sys
import time


def download_multiple_playlist():
    # try to load list of playlists
    try:
        df = pd.read_csv('playlists.csv', header=None)
    except FileNotFoundError:
        print('File not found')
        time.sleep(5)
        sys.exit()

    # iterate over rows in list
    for index, row in df.iterrows():
        playlist = Playlist(row[0])

        # check if playlist title exists as folder and create it if not
        if not os.path.exists(playlist.title):
            os.mkdir(playlist.title)

        for video in playlist.videos:
            try:
                filename = video.streams.get_audio_only().download()

                mp3_filename = convert_mp4_to_mp3(filename=filename)

                # move file to folder
                shutil.move(mp3_filename, os.path.join(playlist.title, os.path.basename(mp3_filename)))
            except:
                continue


def download_playlist(url: str):
    playlist = Playlist(url)
    for video in playlist.videos:
        filename = video.streams.get_audio_only()

        convert_mp4_to_mp3(filename=filename)


def download_single_video(url: str):
    music = YouTube(url)
    filename = music.streams.get_audio_only().download()

    convert_mp4_to_mp3(filename=filename)


def convert_mp4_to_mp3(filename: str):
    clip = moviepy.editor.AudioFileClip(filename)

    # rename file from mp4 to mp3
    name, _ = os.path.splitext(filename)
    new_filename = name + '.mp3'

    clip.write_audiofile(new_filename)
    clip.close()

    # delete unneeded mp4 file
    os.remove(filename)

    return new_filename


if __name__ == '__main__':
    # choose if one video or a playlist
    decision = int(input("If you want to download a single video, enter 0 \n"
                         "If you want to download a whole playlist, enter 1 \n"
                         "If you want to download multiple playlists, enter 9 \n"))
    if decision != 9:
        url = input("Enter URL here: ")

    # match input to correct download function
    match decision:
        case 0:  # single video
            download_single_video(url=url)
        case 1:  # playlist
            download_playlist(url=url)
        case 9:
            download_multiple_playlist()
        case _:
            print('Invalid input')
