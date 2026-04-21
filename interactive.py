import json
import webbrowser
import pyttsx3
import pyaudio
from vosk import Model, KaldiRecognizer
import music_library
import time

# Initialize TTS

engine = pyttsx3.init('sapi5')
engine.setProperty('rate',170)

engine.startLoop(False) #starting non-blocking loop

#def speak(text):
# print("Stark:", text)
#try:
# engine.stop() #clear queue
# engine.say(text)
# engine.runAndWait()
#except RuntimeError:
#pass #ignore loop error safely

def speak(text):
    print("Jarvis:",text)
    engine.say(text)

# Load Vosk model
model = Model("vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)

# Setup microphone
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16,
                  channels=1,
                  rate=16000,
                  input=True,
                  frames_per_buffer=4096)

stream.start_stream()

# Command processing
def processCommand(command):
    command = command.lower()

    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "open facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "open instagram" in command:
        speak("Opening Instagram")
        webbrowser.open("https://instagram.com")

    elif "open linkedin" in command:
        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")

    elif command.startswith("play"):
        try:
            song = command.split(" ", 1)[1]
            link = music_library.music[song]
            speak(f"Playing {song}")
            webbrowser.open(link)
        except:
            speak("Song not found")

    else:
        speak("Command not recognized")

# Main loop with wake word
print("Say 'jarvis' to activate...")
speak("Initializing jarvis")

active = False
active_time=0

while True:
    data = stream.read(2048, exception_on_overflow=False)
    engine.iterate() #keep TTS alive
    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        text = result.get("text", "")

        if text:
            print("You said:", text)

        # Wake word
        if "jarvis" in text:
            active = True
            speak("Yes")
            time.sleep(1)
            recognizer.Reset()
            active_time = time.time()
        #Process command
        elif active and time.time()-active_time < 8:
            processCommand(text)
            active = False
