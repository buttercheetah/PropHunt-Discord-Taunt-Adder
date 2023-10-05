import io, ffmpeg, re, os, requests
import moviepy.editor as mp

def extract_extension(title):
    title = title.split('.')
    return title[-1]

def cleantitle(title):
    title = title.lower()
    title = title.replace(" ", "-")
    title = title.encode("ascii", "ignore")
    title = title.decode()
    return title

def extracttitle(title):
    title = title.split('.')
    return cleantitle(title[0])

def extract_audio_to_wav(video,title):
    tempfile = f'temp.{extract_extension(title)}'
    with open(tempfile, 'wb') as f:
        f.write(video)
    clip = mp.VideoFileClip(tempfile)
    clip.audio.write_audiofile(f"temp.wav")
    with open('temp.wav', 'rb') as f:
        audio = f.read()
    os.remove(tempfile)
    os.remove('temp.wav')
    return audio

