import os
import subprocess
import random
import speech_recognition as sr
import time
from pocketsphinx import LiveSpeech, get_model_path

from .transcribe import recognize_speech_from_mic
from .train import record_wav, update_adaptation_corpus

SPHINX_DATA_DIR = os.getenv("SPHINX_DATA_DIR", "data")


def add_training_data():
    folder = name = str(input("What do you want to name this training data?"))
    c = 1
    while True:
        a_info = {
            "f_name": "{name}_{num}".format(
                name=name, num=str(c).zfill(4)
            ),
            "text": str(input("\n\nType the next line to train with. (-1 to quit)\n"))
        }

        if not a_info['text']:
            print("Please enter a line or -1 to quit.")
            continue

        # Exit condition for recording training data
        if a_info['text'] == '-1':
            print("Exiting...")
            return "Success!"

        record_wav(
            folder, a_info['f_name'], a_info['text']
        )
        update_adaptation_corpus(
            folder, name, a_info['f_name'], a_info['text']
        )
        c += 1


def generate_acoustic_features():
    folder = str(input("Which data do you want to generate features for?"))
    feature_file = "{dir}/en-us/feat.params".format(dir=SPHINX_DATA_DIR)
    acoustic_file_dir= "{dir}/{set}".format(dir=SPHINX_DATA_DIR, set=folder)
    if os.path.isdir(acoustic_file_dir):
        acoustic_fileid_file = "{dir}/{set}.fileids".format(
            dir=acoustic_file_dir, set=folder
        )
        args = [
            "sphinx_fe", 
            "-argfile", feature_file,
            "-samprate", "16000", 
            "-c", acoustic_fileid_file,
            "-di", acoustic_file_dir,
            "-do", acoustic_file_dir,
            "-ei", "wav",
            "-eo", "mfc",
            "-mswav", "yes"
        ]
        output = subprocess.check_output(args)
        print(output)
        return folder
    else:
        print("Data does not exist. Please select a valid data set.")


def accum_obs_counts(data_name):
    en_us = "{dir}/en-us".format(dir=SPHINX_DATA_DIR)
    data_path = "{dir}/{set}".format(dir=SPHINX_DATA_DIR, set=data_name)
    args = [
        "{dir}/bw".format(dir=SPHINX_DATA_DIR),
        "-hmmdir", en_us,
        "-moddeffn", "{dir}/mdef.txt".format(dir=en_us),
        "-ts2cbfn", ".ptm.",
        "-feat", "1s_c_d_dd",
        "-svspec", "0-12/13-25/26-38",
        "-cepdir", data_path,
        # "-ts2cbfn", ".cont.",   # For the continuous model
        # "-lda", "feature_transform",    # for en-us continuous model
        "-cmn", "current",
        "-agc", "none",
        "-dictfn", "{dir}/cmudict-en-us.dict".format(dir=SPHINX_DATA_DIR),
        "-ctlfn", "{path}/{set}.fileids".format(
            path=data_path, set=data_name
        ), 
        "-lsnfn", "{path}/{set}.transcription".format(
            path=data_path, set=data_name
        ),
        "-accumdir", data_path
    ]
    output = subprocess.check_output(args)
    print(output)


def create_mllr_transformation(data_name):
    en_us = "{dir}/en-us".format(dir=SPHINX_DATA_DIR)
    data_path = "{dir}/{set}".format(dir=SPHINX_DATA_DIR, set=data_name)
    args = [
        "/usr/local/libexec/sphinxtrain/mllr_solve",
        "-meanfn", "{dir}/means".format(dir=en_us),
        "-varfn", "{dir}/variances".format(dir=en_us),
        "-outmllrfn", "{dir}/mllr_matrix".format(dir=data_path),
        "-accumdir", data_path
    ]
    output = subprocess.check_output(args)
    print(output)


def map_update_model(data_name):
    en_us = "{dir}/en-us".format(dir=SPHINX_DATA_DIR)
    en_adapt = "{dir}/en-us-adapt".format(dir=SPHINX_DATA_DIR)
    data_path = "{dir}/{set}".format(dir=SPHINX_DATA_DIR, set=data_name)
    args = [
        "{dir}/map_adapt".format(dir=SPHINX_DATA_DIR),
        "-moddeffn", "{dir}/mdef.txt".format(dir=en_us),
        "-ts2cbfn", ".ptm.",
        "-meanfn", "{dir}/means".format(dir=en_us),
        "-varfn", "{dir}/variances".format(dir=en_us),
        "-mixwfn", "{dir}/mixture_weights".format(dir=en_us),
        "-tmatfn", "{dir}/transition_matrices".format(dir=en_us),
        "-accumdir", data_path,
        "-mapmeanfn", "{dir}/means".format(dir=en_adapt),
        "-mapvarfn", "{dir}/variances".format(dir=en_adapt),
        "-mapmixwfn", "{dir}/mixture_weights".format(dir=en_adapt),
        "-maptmatfn", "{dir}/transition_matrices".format(dir=en_adapt)
    ]
    output = subprocess.check_output(args)
    print(output)


def test_speech_recognition():
    # set the list of words, maxnumber of guesses, and prompt limit
    WORDS = [
        "strafe", "pitch", "throttle", "left", "right", 
        "up", "down", "forward", "back"
    ]
    NUM_GUESSES = 3
    PROMPT_LIMIT = 5

    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # get a random word from the list
    word = random.choice(WORDS)

    # format the instructions string
    instructions = (
        "I'm thinking of one of these words:\n"
        "{words}\n"
        "You have {n} tries to guess which one.\n"
    ).format(words=', '.join(WORDS), n=NUM_GUESSES)

    # show instructions and wait 3 seconds before starting the game
    print(instructions)
    time.sleep(3)

    for i in range(NUM_GUESSES):
        # get the guess from the user
        # if a transcription is returned, break out of the loop and
        #     continue
        # if no transcription returned and API request failed, break
        #     loop and continue
        # if API request succeeded but no transcription was returned,
        #     re-prompt the user to say their guess again. Do this up
        #     to PROMPT_LIMIT times
        for j in range(PROMPT_LIMIT):
            print('Guess {}. Speak!'.format(i+1))
            guess = recognize_speech_from_mic(recognizer, microphone)
            if guess["transcription"]:
                break
            if not guess["success"]:
                break
            print("I didn't catch that. What did you say?\n")

        # if there was an error, stop the game
        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
            break

        # show the user the transcription
        print("You said: {}".format(guess["transcription"]))

        # determine if guess is correct and if any attempts remain
        guess_is_correct = guess["transcription"].lower() == word.lower()
        user_has_more_attempts = i < NUM_GUESSES - 1

        # determine if the user has won the game
        # if not, repeat the loop if user has more attempts
        # if no attempts left, the user loses the game
        if guess_is_correct:
            print("Correct! You win!")
            break
        elif user_has_more_attempts:
            print("Incorrect. Try again.\n")
        else:
            print("Sorry, you lose!\nI was thinking of '{}'.".format(word))
            break
