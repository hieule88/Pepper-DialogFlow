#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

import re
import sys
import os

from google.cloud import speech
from google.api_core.exceptions import OutOfRange
from MicrophoneStream import MicrophoneStream
from GTTS import GTTS
from dialogflow import DF_intents
import time

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getcwd() + "/testproject-363201-117b75239eed.json"


class ListenLoop:

    def __init__(self, project_id, df_action, lang, device=0, rate=16000):

        self.RATE = 48000
        self.CHUNK = 1024# int(rate / 10)  # 100ms
        self.client = speech.SpeechClient()

        self.tts = GTTS()
        self.lang = lang
        self.df = DF_intents(project_id, project_id + "1", df_action, debug=True)
        self.stream = object()
        self.device = device

    def listen_loop(self,responses):
        """Iterates through server responses and prints them.
        The responses passed is a generator that will block until a response
        is provided by the server.
        Each response may contain multiple results, and each result may contain
        multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
        print only the transcription for the top alternative of the top result.
        In this case, responses are provided for interim results as well. If the
        response is an interim one, print a line feed at the end of it, to allow
        the next result to overwrite it, until the response is a final one. For the
        final one, print a newline to preserve the finalized transcription.
        """
        num_chars_printed = 0
        for response in responses:
            if not response.results:
                continue

            # The `results` list is consecutive. For streaming, we only care about
            # the first result being considered, since once it's `is_final`, it
            # moves on to considering the next utterance.
            result = response.results[0]
            if not result.alternatives:
                continue

            # Display the transcription of the top alternative.
            transcript = result.alternatives[0].transcript

            # Display interim results, but with a carriage return at the end of the
            # line, so subsequent lines will overwrite them.
            #
            # If the previous result was longer than this one, we need to print
            # some extra spaces to overwrite the previous result
            overwrite_chars = ' ' * (num_chars_printed - len(transcript))

            if not result.is_final:
                sys.stdout.write(transcript + overwrite_chars + '\r')
                sys.stdout.flush()

                num_chars_printed = len(transcript)

            else:
                print(transcript + overwrite_chars)
                self.df.detect_intent_texts([transcript], self.lang.lang)


                num_chars_printed = 0

    def run(self):
        #main 'listen and recognition' function

        try:

            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=self.RATE,
                language_code=self.lang.lang,
                speech_contexts=[
                    speech.SpeechContext(phrases=self.lang.phrases)
                ]
            )

            streaming_config = speech.StreamingRecognitionConfig(
                config=config,
                interim_results=True)

            with MicrophoneStream(self.RATE, self.CHUNK, self.device) as self.stream:
                audio_generator = self.stream.generator()
                requests = (speech.StreamingRecognizeRequest(audio_content=content)
                            for content in audio_generator)

                responses = self.client.streaming_recognize(streaming_config, requests)

                # Now, put the transcription responses to use.
                self.listen_loop(responses)

        except OutOfRange:
            print("Stream restart")
            self.stream.stop()


    def change_lang(self, lang):
        self.lang = lang
        self.stream.stop()


class LangParams:
    def __init__(self, lang, locale, phrases, start_phrase):
        self.lang = lang
        self.locale = locale
        self.phrases = phrases
        self.start_phrase = start_phrase



