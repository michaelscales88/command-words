# Adapted from examples on https://realpython.com/python-speech-recognition/
import os
import random
import time

import speech_recognition as sr
from .train import threeseccountdown

SPHINX_DATA_DIR = os.getenv("SPHINX_DATA_DIR", "data")

 
def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        print("Please wait. Calibrating microphone...")  
        recognizer.adjust_for_ambient_noise(source, duration=3)
        threeseccountdown()
        print("** Listening **")
        audio = recognizer.listen(source)
        print("** Processing... Please wait... **")

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }
    
    # custom model information
    model_path = {
        'hmm': os.path.join(SPHINX_DATA_DIR, 'en-us-adapt'),
        'lm': os.path.join(SPHINX_DATA_DIR, 'en-us.lm.bin'),
        'dict': os.path.join(SPHINX_DATA_DIR, 'cmudict-en-us.dict')
    }
    
    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_sphinx(
            audio, language=(
                model_path['hmm'], model_path['lm'], model_path['dict']
            )
        )
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

