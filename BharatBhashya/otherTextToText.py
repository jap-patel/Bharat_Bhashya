from googletrans import Translator
# from google_trans_new import google_translator

# translator = google_translator()
def text_to_text(language, contents):
    outputText = ""
    translater=Translator()
    # f=open("demo.txt","r",encoding="utf-8")
    # if f.mode=="r":
    #     contents=f.read();
    #     f.close()
    try:
        # outputText=translater.translate("મારું નામ દિવ્યેશ છે હું બીજી સી માં ભણું છું મારા મિત્રો તથા કુંતાનું જયો વિશાલ અને જ છે", dest="en")
        outputText=translater.translate(contents, dest=language)
        print(outputText.text)
        with open(str(outputText.src) + "_to_" + str(language) + ".txt", "w", encoding="utf-8") as f:
            f.write(str(outputText.text))            
            f.close()
    except:
        outputText = contents + str(language) +"sorry output text can't be obtained"
        print("sorry output text can't be obtained")    
        return outputText

    return outputText.text

# if __name__=="__main__":
#     text_to_text("મારું નામ દિવ્યેશ છે હું બીજી સી માં ભણું છું મારા મિત્રો તથા કુંતાનું જયો વિશાલ અને જ છે","hi")