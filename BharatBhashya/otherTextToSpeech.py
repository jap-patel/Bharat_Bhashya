import time
from gtts import gTTS
from io import BytesIO
import pygame

# f=open("demo1-en.txt","r",encoding="utf-8")
# if f.mode=="r":
#     contents=f.read();
#     f.close()
def hear_the_audio(content, language):
    # contents = "મારું નામ દિવ્યેશ છે હું બીજી સી માં ભણું છું મારા મિત્રો તથા કુંતાનું જયો વિશાલ અને જ છે"
    # print(contents)
    # language = 'gu'
    print("reached: ", content)
    mp3_fo = BytesIO()
    myobj = gTTS(text=content, lang=language, slow=False)
    myobj.write_to_fp(mp3_fo)
    # # # save to local folder:
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_fo, 'mp3')
    pygame.mixer.music.play()
    time.sleep(10)
    myobj.save("temp123-hindi.wav")

    return content