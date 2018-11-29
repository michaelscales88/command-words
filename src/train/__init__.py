import time
import os
from .recorder import Recorder

SPHINX_WAV_DIR = "src/train/wavs"
os.makedirs(SPHINX_WAV_DIR, exist_ok=True)

def record_wav(text):
    print("Repeat the following text: {}".format(text))
    rec = Recorder()
    wav = os.path.join(SPHINX_WAV_DIR, '{}.wav'.format(text))
    with rec.open(wav, 'wb') as recfile2:
        recfile2.start_recording()
        while True:
            if input("q") == 'q':
                recfile2.stop_recording()
