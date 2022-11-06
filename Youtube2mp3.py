from pytube import YouTube, Playlist
import moviepy.editor
import os


def download_playlist(url: str):
    playlist = Playlist(url)
    for video in playlist.videos:
        filename = video.streams.get_audio_only().download()

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


if __name__ == '__main__':
    # choose if one video or a playlist
    decision = int(input("If you want to download a single video, enter 0 \nIf you want to download a whole playlist, enter 1 \n"))
    url = input("Enter URL here: ")

    # match input to correct download function
    match decision:
        case 0:  # single video
            download_single_video(url=url)
        case 1:  # playlist
            download_playlist(url=url)
        case _:
            print('Invalid input')
