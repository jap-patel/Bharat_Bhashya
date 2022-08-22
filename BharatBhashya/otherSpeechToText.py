
# ------- for batch translate speech to text----------------------------
# import speech_recognition as sr
#
# r = sr.Recognizer()
#
# with sr.AudioFile("demo-speech-hindi1.wav") as source:
#     r.adjust_for_ambient_noise(source)
#     print("Speak Anything :")
#     audio=r.record(source,offset=10)
#     # audio = r.listen(source)
#
# try:
#     text = r.recognize_google(audio,language="hi-IN")
#     print("You said : {}".format(text))
# except:
#     print("Sorry could not recognize what you said")
#
# with open("demo1-hi.txt", "w", encoding="utf-8") as f:
#     f.write(text)

# ------- for stream translate speech to text----------------------------

import speech_recognition as sr

def speech_to_text(language):
    text = ""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Speak Anything :")
        # audio=r.record(source,offset=10)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language = language)
        print("You said : {}".format(text))
    except:
        print("Sorry could not recognize what you said")

    with open("speech_to_text_" + str(language) + ".txt", "w", encoding="utf-8") as f:
        f.write(text)
    return text