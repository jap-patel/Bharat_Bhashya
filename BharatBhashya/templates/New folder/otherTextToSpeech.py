import time

import pyttsx3
#
# # def change_voice(engine, language, gender='VoiceGenderFemale'):
# #     for voice in engine.getProperty('voices'):
# #         if language in voice.languages and gender == voice.gender:
# #             engine.setProperty('voice', voice.id)
# #             return True
# #
# #     raise RuntimeError("Language '{}' for gender '{}' not found".format(language, gender))
#
# def main():
text_speech = pyttsx3.init()
#     # change_voice(text_speech, "", "VoiceGenderFemale")
#     f = open("temp123", "rb", encoding="utf-8")
#     if f.mode == "r":
#         contents = f.read();
#         f.close()
#         print(contents)
# stream = text_speech.say("temp123.wav")
# print(stream)
# text_speech.runAndWait()
#
# if __name__ == '__main__':
#     main()

# with open("demo-textToSpeech-en.wav", "wb") as file:
#     file.write(stream)
#     file.close()
# language  : en_US, de_DE, ...
# gender    : VoiceGenderFemale, VoiceGenderMale

# voices = text_speech.getProperty('voices')
# for voice in voices:
#     print("Voice: %s" % voice.name)
#     print(" - ID: %s" % voice.id)
#     print(" - Languages: %s" % voice.languages)


# from gtts import gTTS
# import winsound

from gtts import gTTS
from io import BytesIO
import pygame
f=open("demo1-en.txt","r",encoding="utf-8")
if f.mode=="r":
    contents=f.read();
    f.close()
print(contents)
language = 'en'
mp3_fo = BytesIO()
myobj = gTTS(text=contents, lang=language, slow=False)
myobj.write_to_fp(mp3_fo)
# # # save to local folder:
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(mp3_fo, 'mp3')
pygame.mixer.music.play()
time.sleep(120)
# myobj.save("temp123-hindi.wav")

