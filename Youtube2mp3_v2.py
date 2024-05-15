import shutil
from pytube import YouTube, Playlist
from pytube.exceptions import RegexMatchError
import moviepy.editor
import os


def download_playlist(url: str):
    playlist = Playlist(url)
    # check if playlist title exists as folder and create it if not
    if not os.path.exists(playlist.title):
        os.mkdir(playlist.title)

    for video in playlist.videos:
        try:
            filename = video.streams.get_audio_only().download()

            mp3_filename = convert_mp4_to_mp3(filename=filename)

            # move file to folder
            shutil.move(mp3_filename, os.path.join(
                playlist.title, os.path.basename(mp3_filename)))
        except:
            continue


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
    urls = []

    while True:
        url = input('Enter URL here: ')
        if url != "":
            urls.append(url)
        else:
            break

    for url in urls:
        try:
            download_single_video(url=url)
        except RegexMatchError:
            try:
                download_playlist(url=url)
            except:
                continue
        except:
            continue
