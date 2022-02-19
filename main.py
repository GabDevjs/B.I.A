#Iciniando codigo
import argparse
from asyncio import streams
import os
import queue
import sounddevice as sd
import vosk
import sys
import pyttsx3
import json
 
engine = pyttsx3.init()# Init da função de voz
#definição da voz

q = queue.Queue()


# ----------------------------

#definição da voz
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[-2].id)

#fução de fala de voz
def speak(text):
    engine.say(text)
    engine.runAndWait()

def int_or_str(text):
    """Função auxiliar para análise de argumentos."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """
    Isso é chamado (de um thread separado) para cada bloco de áudio.
    """
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    '-f', '--filename', type=str, metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-m', '--model', type=str, metavar='MODEL_PATH',
    help='Path to the model')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
args = parser.parse_args(remaining)

try:
    if args.model is None:
        args.model = "model"
    if not os.path.exists(args.model):
        print ('model')
        parser.exit(0)
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info['default_samplerate'])

    model = vosk.Model(args.model)

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None

    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device, dtype='int16',
                            channels=1, callback=callback):
            print('#' * 80)
            print('Press Ctrl+C to stop the recording')
            print('#' * 80)

            rec = vosk.KaldiRecognizer(model, args.samplerate)
            ''' while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = rec.Result()
                    result = json.loads(result)
                    
                    print(result)
                    
                else:
                    print(rec.PartialResult())
                if dump_fn is not None:
                    dump_fn.write(data) '''
                    
            while True:
                data = q.get(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    result = rec.Result()
                    result = json.loads(result)
                       
                    text = result['text']
                    
                    print(text)
                    speak(text)

except KeyboardInterrupt:
    print('\nDone')
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
