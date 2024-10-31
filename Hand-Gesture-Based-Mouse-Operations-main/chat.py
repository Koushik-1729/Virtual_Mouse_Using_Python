import eel
import os
from queue import Queue
import pyttsx3
import speech_recognition as sr
from datetime import date
import time
import webbrowser
import datetime
from pynput.keyboard import Key, Controller
import pyautogui
import sys
from os import listdir
from os.path import isfile, join
from threading import Thread

print("all imports done")

import chat as app

class ChatBot:

    started = False
    userinputQueue = Queue()

    @staticmethod
    def isUserInput():
        return not ChatBot.userinputQueue.empty()

    @staticmethod
    def popUserInput():
        return ChatBot.userinputQueue.get()

    @staticmethod
    def close_callback(route, websockets):
        exit()

    @staticmethod
    def getUserInput(msg):
        ChatBot.userinputQueue.put(msg)
        print(msg)

    @staticmethod
    def close():
        ChatBot.started = False

    @staticmethod
    def addUserMsg(msg):
        eel.addUserMsg(msg)

    @staticmethod
    def addAppMsg(msg):
        eel.addAppMsg(msg)

    @staticmethod
    def reply(audio):
        print("started audio")
        app.ChatBot.addAppMsg(audio)
        print(audio)
        engine.say(audio)
        engine.runAndWait()

    @staticmethod
    def wish():
        hour = int(datetime.datetime.now().hour)

        if hour >= 0 and hour < 12:
            ChatBot.reply("Good Morning!")
        elif hour >= 12 and hour < 18:
            ChatBot.reply("Good Afternoon!")
        else:
            ChatBot.reply("Good Evening!")

        ChatBot.reply("I am lucy, how may I help you?")

    @staticmethod
    def record_audio():
        with sr.Microphone() as source:
            r.pause_threshold = 0.5
            voice_data = ''
            print("Voice Data:", voice_data)
          
            audio = r.listen(source, phrase_time_limit=5)

            try:
                voice_data = r.recognize_google(audio)
            except sr.RequestError:
                ChatBot.reply('Sorry my Service is down. Plz check your Internet connection')
            except sr.UnknownValueError:
                print('cant recognize')
                pass
            return voice_data.lower()

    @staticmethod
    def respond(voice_data):
        global file_exp_status, files, is_awake, path
        print(voice_data)
        voice_data = voice_data.replace('Lucy', '')
        print (voice_data)
        app.eel.addUserMsg(voice_data)
        try:
            if is_awake == False:
                print("Checking wake-up condition...")
                if 'wake up' in voice_data:
                    is_awake = True
                    ChatBot.wish()
            elif 'open Google' in voice_data:
                webbrowser.open('https://www.google.com/')
                ChatBot.reply('Opening Google for you.')

            elif 'search' in voice_data:
                search_query = voice_data.split('search')[-1]
                webbrowser.open(f'https://www.google.com/search?q={search_query}')
                ChatBot.reply(f'Searching for {search_query} on Google.')

            # ... (rest of your existing code)

        except Exception as e:
            print(f"Exception: {e}")

    @staticmethod
    def start():
        path = os.path.dirname(os.path.abspath(__file__))
        eel.init(path + r'\web', allowed_extensions=['.js', '.html'])
        try:
            eel.start('index.html', mode='chrome',
                     host='localhost',
                     port=27005,
                     block=False,
                     size=(350, 480),
                     position=(10, 100),
                     disable_cache=True,
                     close_callback=ChatBot.close_callback)
            ChatBot.started = True
            while ChatBot.started:
                try:
                    eel.sleep(10.0)
                except:
                    # main thread exited
                    break
        except:
            pass
if __name__ == "__main__":
    today = date.today()
    r = sr.Recognizer()
    print(r)
    keyboard = Controller()
    engine = pyttsx3.init('sapi5')
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    file_exp_status = False
    files = []
    path = ''
    is_awake = True

    print("before the chatbot...")

    # Create an instance of ChatBot
    print("Starting the chatbot...")
    chat_bot_instance = ChatBot()

    # Start the Eel interface in a separate thread
    t1 = Thread(target=lambda: chat_bot_instance.start())
    t1.start()

    # Lock the main thread until Chatbot has started
    while not chat_bot_instance.started:
        time.sleep(0.5)

    # Greet the user
    chat_bot_instance.wish()

    voice_data = None
    while True:
        if app.ChatBot.isUserInput():
            # Take input from GUI
            voice_data = app.ChatBot.popUserInput()
        else:
            # Take input from Voice
            voice_data = chat_bot_instance.record_audio()

        # Process voice_data
        if 'proton' in voice_data:
            try:
                # Handle sys.exit()
                chat_bot_instance.respond(voice_data)
            except SystemExit:
                chat_bot_instance.reply("Exit Successful")
                break
            except Exception as e:
                # Some other exception got raised
                print(f"EXCEPTION raised while closing: {e}")
                break
