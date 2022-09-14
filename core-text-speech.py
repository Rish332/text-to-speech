import pandas as pd
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
import time
from gtts import gTTS
import numpy as np
import soundfile
import librosa
from pathlib import Path
df = pd.read_excel("text_speech_data.xlsx")

test_data = df["Sample data"]
path = "audio_files"

'''
# text to speech using AWS polly

# Create a client using the credentials and region defined in the [adminuser]
# section of the AWS credentials file (~/.aws/credentials).
session = Session(profile_name="default")
polly = session.client("polly")
try:
    # Request speech synthesis
    for sentence in test_data:
        response = polly.synthesize_speech(Text=sentence, OutputFormat="mp3",
                                           VoiceId="Joanna")
        # Access the audio stream from the response
        if "AudioStream" in response:
            # Note: Closing the stream is important because the service throttles on the
            # number of parallel connections. Here we are using contextlib.closing to
            # ensure the close method of the stream object will be called automatically
            # at the end of the with statement's scope.
            with closing(response["AudioStream"]) as stream:
                if not os.path.exists(path):
                    os.makedirs(path)
                output = os.path.join(path, "speech.mp3")

                try:
                    # Open a file for writing the output as a binary stream
                    with open(output, "wb") as file:
                        file.write(stream.read())
                except IOError as error:
                    # Could not write to file, exit gracefully
                    print(error)
                    sys.exit(-1)

        else:
            # The response didn't contain audio data, exit gracefully
            print("Could not stream audio")
            sys.exit(-1)

        # Play the audio using the platform's default player
        if sys.platform == "win32":
            os.startfile(output)
        else:
            # The following works on macOS and Linux. (Darwin = mac, xdg-open = linux).
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, output])

        time.sleep(5)

except (BotoCoreError, ClientError) as error:
    # The service returned an error, exit gracefully
    print(error)
    sys.exit(-1)
'''

# text to speech using google text to speech open source library gTTS which is used in Google Translate

for sentence in test_data:
    response = gTTS(text=sentence, lang='en')
    if not os.path.exists(path):
        os.makedirs(path)
    output = os.path.join(path, "speech.wav")
    response.save(output)
    # tried adding noise using librosa library

    # STD_n = 0.001
    # signal, sr = librosa.load(output, sr=16000)
    # noise = np.random.normal(0, STD_n, signal.shape[0])
    # soundfile.write(output, noise, 16000)

    # Play the audio using the platform's default player
    if sys.platform == "win32":
        os.startfile(output)
    else:
        # The following works on macOS and Linux. (Darwin = mac, xdg-open = linux).
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, output])

    time.sleep(5)
