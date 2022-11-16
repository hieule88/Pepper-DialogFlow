#!/usr/bin/python
# encoding: utf-8
import subprocess
import os
import argparse
import random
import string
from google.cloud import dialogflow
from google.api_core.exceptions import InvalidArgument
from google.cloud import texttospeech

DIALOGFLOW_PROJECT_ID = 'testproject-363201'
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/hieulepc/Pepper-Controller/testproject-363201-117b75239eed.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/hieule/Pepper-DialogFlow/testproject-363201-117b75239eed.json'
def synthesize_text(text, dir):
    """Synthesizes speech from the input string of text."""

    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="vi-VN",
        name="vi-VN-Wavenet-A",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    audio_config = texttospeech.AudioConfig(pitch=2,
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    # The response's audio_content is binary.
    fname = os.getcwd() + '/tts-temp' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)) + '.mp3'
    # The response's audio_content is binary.
    out = open(fname, 'wb')
    # Write the response to the output file.
    out.write(response.audio_content)
    #print('Audio content written to file ' + fname)
    out.close()

    return fname

def detect_intent_texts(session_id, text, language_code='vi-VN'):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    try:    
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:    
        raise
    if response.query_result.fulfillment_text != "" :
        return synthesize_text(response.query_result.fulfillment_text)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--text', action='store', type=str, default='')

    args = parser.parse_args()
    text = args.text

    mp3_file = detect_intent_texts('user-session', text)
    print(mp3_file)