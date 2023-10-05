import io, ffmpeg, moviepy
def extract_audio_to_wav(video):
    # Open the video file in binary mode
    with open('video.mp4', 'rb') as video_file:

        # Create a BytesIO object
        audio_bytes = io.BytesIO()

        # Create an FFmpeg object
        ffmpeg_object = ffmpeg.FFmpeg()

        # Extract the audio from the video
        ffmpeg_object.input(video_file).output(audio_bytes, format='mp3').run()

        # Get the audio bytes from the BytesIO object
        audio_bytes.seek(0)
        audio_bytes_data = audio_bytes.read()

        # Save the audio bytes to a file
        with open('audio.mp3', 'wb') as audio_file:
            audio_file.write(audio_bytes_data)