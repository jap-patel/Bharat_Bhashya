import os 
from google.cloud import speech

def convert(source_lang, dest_lang):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'api-speech-to-text-359714-9f3f4a08633a.json'
    speech_client = speech.SpeechClient()

    lang_code = source_lang
    media_file_name_wav = 'demo-textToSpeech-' + lang_code + '.wav'

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
    response_standard_wav = speech_client.recognize(
        config=config_wav,
        audio=audio_wav
    )
    # print(response_standard_wav.results[0].alternatives[0].transcript)
    print(response_standard_wav)

    output_file = 'demo-'+source_lang+'-'+ dest_lang + ".txt"
    with open(output_file,'w',encoding="utf-8") as output:
        output.write(str(response_standard_wav.results[0].alternatives[0].transcript))


    # translator

    #import os 
    from google.cloud import translate_v2 as translate

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'api-speech-to-text-359714-9f3f4a08633a.json'
    translate_client = translate.Client()

    lang_code = source_lang
    target_lang = dest_lang
    text_file = output_file

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

    output_file = target_lang + "-"+ dest_lang + ".txt"
    with open(output_file,'w',encoding="utf-8") as output:
        output.write(output_data)