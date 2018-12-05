import time
import os
from .recorder import Recorder


SPHINX_DATA_DIR = os.getenv("SPHINX_DATA_DIR", "data")


def make_data_folder(folder):
    os.makedirs(folder, exist_ok=True)


make_data_folder(SPHINX_DATA_DIR)


def threeseccountdown():
    c = 3
    while c > 0:
        print("{}...".format(c))
        time.sleep(1)
        c -= 1


def update_adaptation_corpus(folder, data_name, name, text):
    # Init
    data_folder = os.path.join(SPHINX_DATA_DIR, folder)

    # Update the fid file with the new wav file
    fid_name = "{}.fileids".format(data_name)
    with open(os.path.join(data_folder, fid_name), "a") as fid_file:
        fid_file.write(name + "\n")

    # Update the transcription file with the text from the wav file
    ts_name = "{}.transcription".format(data_name)
    with open(os.path.join(data_folder, ts_name), "a") as ts_file:
        ts_file.write(
            "<s> {text} </s> ({file})\n".format(text=text, file=name)
        )



def record_wav(folder, name, text):
    rec = Recorder(rate=16000)
    data_folder = os.path.join(SPHINX_DATA_DIR, folder)
    make_data_folder(data_folder)
    with rec.open(os.path.join(data_folder, name + ".wav"), 'wb') as wav_file:
        print(
            "\n\nRepeat the following text:\n\t\t'{}'\nin...".format(text)
        )
        threeseccountdown()
        print("** Recording Start **")
        wav_file.start_recording()
        while True:
            if not input("## Press enter to stop recording ##"):
                wav_file.stop_recording()
                break
    print("** Recording Stopped **")
