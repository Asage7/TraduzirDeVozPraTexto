# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 13:11:33 2021

@author: USUARIO
"""

import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS

def speak(text):
    tts = gTTS(text=text, lang="pt-BR")
    filename="C:\\Users\\USUARIO\\voice.mp3"
    if not os.path.exists(filename):
        tts.save(filename)
    else:
        os.remove(filename)
        tts.save(filename)
    playsound.playsound(filename)

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said="Sem retorno"
        try:
            r.recognize_google(audio)
            said=r.recognize_google(audio,None,"pt-BR")
            print(said)
        except Exception as e:
            print("Exceptio: "+ str(e))
        return said

def mp3_to_text(filename):
    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = r.listen(source)
        said="Sem retorno"
        try:
            r.recognize_google(audio)
            said=r.recognize_google(audio,None,"pt-BR")
            text_file = open("Output.txt", "w")
            text_file.write(said)
            text_file.close()
            print(said)

        except Exception as e:
            print("Exceptio: "+ str(e))
        return said
    
    
#speak("Olá Mundo")
mp3_to_text(r"C:\Users\USUARIO\Desktop\audio2.wav")