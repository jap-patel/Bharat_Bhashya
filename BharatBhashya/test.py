import pyaudio
import wave
import os 
from google.cloud import speech
from google.cloud import translate_v2 as translate

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
seconds = 15
filename = "output.wav"

p = pyaudio.PyAudio()  # Create an interface to PortAudio

print('Recording')

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

frames = []  # Initialize array to store frames

# Store data in chunks for 3 seconds
for i in range(0, int(fs / chunk * seconds)):
    data = stream.read(chunk)
    frames.append(data)

# Stop and close the stream 
stream.stop_stream()
stream.close()
# Terminate the PortAudio interface
p.terminate()

print('Finished recording')

# Save the recorded data as a WAV file
wf = wave.open(filename, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()




os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'api-speech-to-text-359714-9f3f4a08633a.json'
speech_client = speech.SpeechClient()

lang_code = "en-IN"
media_file_name_wav = 'output.wav'

## Step 1 Load the media files
with open(media_file_name_wav, 'rb') as file:
    byte_data_wav = file.read()
audio_wav = speech.RecognitionAudio(content=byte_data_wav)

## Step 2 Configure media files output
config_wav = speech.RecognitionConfig(
    enable_automatic_punctuation=True,
    language_code=lang_code,
    audio_channel_count=2
)  

## Step 3 Transcribing the recognitionaudio objects
response_standard_wav = speech_client.recognize(config=config_wav,audio=audio_wav)

print(response_standard_wav.results[0].alternatives[0].transcript)
print(response_standard_wav)

output_file = 'demo-english-hindi-real-' + lang_code + ".txt"
with open(output_file,'w',encoding="utf-8") as output:
    output.write(str(response_standard_wav.results[0].alternatives[0].transcript))


# translator

#import os 

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'api-speech-to-text-359714-9f3f4a08633a.json'
translate_client = translate.Client()

lang_code = "en-IN"
target_lang = "hi-IN"
text_file = 'demo-english-hindi-real-' + lang_code +".txt" #'demo.txt'

# text = 'How are you'
with open(text_file, 'r') as file:
    text_data = file.read()

output = translate_client.translate(
    # text
    text_data,
    target_language = target_lang
)
# print(u'Translation: {}'.format(output['translatedText']))
output_data = 'Translation: {}'.format(output['translatedText'])

output_file = 'demo-real-' + target_lang + ".txt"
with open(output_file,'w',encoding="utf-8") as output:
    output.write(output_data)