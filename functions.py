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

def cleanurl(url):
    if url[-1] == '/':
        url = url[:-1]
    match = re.match('^.*\/\/', url)
    if match == None:
        url = f'https://{url}'
    elif match.string[match.end()-4] == 's':
        pass
    else:
        print("https is recommended")
    return url

def upload(audiobytes,url,filename,serverid,directory,username,password):
    upload_file(login_to_pufferpanel(url,username,password),
    audiobytes,
    url,
    filename,
    serverid,
    directory)

def upload_file(headers,audiobytes,url,filename,serverid,directory):
    url = f"{url}/proxy/daemon/server/{serverid}/file/{directory}/{filename}"
    payload = audiobytes
    response = requests.request("PUT", url, data=payload, headers=headers)
    print(response.text)

def login_to_pufferpanel(url,username,password):
    url = f"{url}/auth/login"
    payload = {
        "email": username,
        "password": password
    }
    headers = {
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json"
    }
    response = requests.request("POST", url, json=payload, headers=headers)

    return {"authorization": f"Bearer {response.json()['session']}","cookie": f"puffer_auth={response.json()['session']}"}
print(login_to_pufferpanel('','',''))