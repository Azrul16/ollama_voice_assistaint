import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from ollama import chat
import speech_recognition as sr
from datetime import date
from gtts import gTTS
from io import BytesIO
from pygame import mixer
import time
import requests
import json

# Initialize pygame mixer
mixer.init()

# Global variables
today = str(date.today())
numtext, numtts, numaudio = 0, 0, 0
messages = []

# Text-to-Speech function
def speak_text(text):
    mp3file = BytesIO()
    tts = gTTS(text, lang="en", tld='us')
    tts.write_to_fp(mp3file)
    mp3file.seek(0)
    mixer.music.load(mp3file)
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(0.1)

#Generate Response from the Llama2
def generate_response(text):
    url = "http://127.0.0.1:11434/api/generate"
    
    if any(word in text for word in ("quit", "bye", "exit", "terminate")):
        speak_text("Goodbye!")
        exit()

    text = text + " make the resposnce short."
    payload = {
        "model": "llama2",
        "prompt": text
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.post(url, data=json.dumps(payload), headers=headers, stream=True)
    speak_text("I am generating the best answer for you.")
    
    if response.status_code == 200:
        full_response = ""
        #speak_text('Please wait a little more')
        for line in response.iter_lines():
            if line:
                decoded_line = json.loads(line.decode('utf-8'))
                full_response += decoded_line.get("response", "")
                if decoded_line.get("done", False):
                    break
        
        print("Response:")
        speak_text(full_response.strip())
    else:
        print(f"Failed to connect. Status code: {response.status_code}")

# Main function
def main():
    global today, numtext, numtts, numaudio, messages
    rec = sr.Recognizer()
    mic = sr.Microphone()
    while True:
        with mic as source:
            rec.adjust_for_ambient_noise(source, duration=1)
            print("Listening ...")
            speak_text('Listening')
            
            try:
                # Capture audio input
                audio = rec.listen(source, timeout=40, phrase_time_limit=30)
                # Recognize speech using Google Web Speech API
                text = rec.recognize_google(audio, language="en-EN")

                # Print recognized text in terminal
                print(f"Recognized Text: {text}")

                # Read out the recognized text using Text-to-Speech
                #speak_text(f"{text}")
                #Generate the response from the Llama
                generate_response(text=text)


            except sr.UnknownValueError:
                print("Could not understand audio.")
            except sr.RequestError as e:
                print(f"Speech Recognition error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        mixer.music.stop()
