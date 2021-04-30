# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 13:11:33 2021

@author: USUARIO
"""
from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
import time
import playsound
import pyttsx3
import speech_recognition as sr
from gtts import gTTS
import pytz
import subprocess

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MESES = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
DIAS_DA_SEMANA = ['domingo','segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado']
DIAS_DA_SEMANA_EXT=['segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira']
DIA_EXT = ['primeiro','segundo','terceiro']
CALENDARIO_STRS=["o que eu tenho","estou ocupado","tenho planos"]
NOTE_STRS=["faça uma nota","lembre disso","anote isso"]
WAKE_WORD=["olá marta"]


def speak(text):
    """
    engine=pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    """
    tts = gTTS(text=text, lang="pt-BR")
    filename="C:\\Users\\USUARIO\\voice.mp3"
    if not os.path.exists(filename):
        tts.save(filename)
    else:
        os.remove(filename)
        tts.save(filename)
    playsound.playsound(filename)
    print(text)
    

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
    

def authenticate_Google():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    
    return service

def get_events(dia,service):

    # Call the Calendar API
    data=datetime.datetime.combine(dia,datetime.datetime.min.time())
    data_fim=datetime.datetime.combine(dia,datetime.datetime.max.time())
    utc=pytz.UTC
    data=data.astimezone(utc)
    data_fim=data_fim.astimezone(utc)
    
    events_result = service.events().list(calendarId='primary', timeMin=data.isoformat(), 
                                         timeMax=data_fim.isoformat(),
                                         singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        speak("Nenhum evento encontrado.")
    for event in events:
        speak(f"Existem {len(events)} eventos nesse dia.")
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
        Evento_Tempo=str(start.split("T")[1].split("-")[0])
        if int(Evento_Tempo.split(":")[0])<12:
            Evento_Tempo=Evento_Tempo+" da manhã."
        else:
            Evento_Tempo=str(int(Evento_Tempo.split(":")[0])-12)+":"+ Evento_Tempo.split(":")[1]
            Evento_Tempo=Evento_Tempo + " da tarde."
    speak(event["summary"] + " as "+Evento_Tempo)

def get_data(texto):
    texto=texto.lower()
    hoje=datetime.date.today()
    
    if texto.count("hoje")>0:
        return hoje
    
    dia =-1
    dia_da_semana=-1
    mes =-1
    ano=hoje.year
    
    for palavra in texto.split():
        if palavra in MESES:
            mes= MESES.index(palavra)+1
        elif palavra in DIAS_DA_SEMANA:
            dia_da_semana=DIAS_DA_SEMANA.index(palavra)
        elif palavra in DIAS_DA_SEMANA_EXT:
            dia_da_semana=DIAS_DA_SEMANA_EXT.index(palavra)+1
        elif palavra in DIA_EXT:
            dia=DIA_EXT.index(palavra)+1
        elif palavra.isdigit():
            dia=int(palavra)
    
    if mes<hoje.month and mes!=-1:
        ano=ano+1
        
    if dia<hoje.day and mes==-1 and dia!=-1:
        mes=hoje.month+1
         
    if mes==-1 and dia==-1 and dia_da_semana!=-1:
        dia_atual=hoje.weekday()
        dif=dia_da_semana-dia_atual
        
        if texto.count("próxima")>=1 or texto.count("próximo")>=1 :
            dif+=7
            
        if dif<0:
            dif+=7

        return hoje+datetime.timedelta(dif)
    
    return datetime.date(day=dia,month=mes,year=ano)

def Anotar(texto):
    data=datetime.datetime.now()
    file_name=str(data).replace(":","-")+"-note.txt"
    with open(file_name,"w")as f:
        f.write(texto)
    subprocess.Popen(["notepad.exe", file_name])


#text=get_audio()
#print(get_data(text))
service=authenticate_Google()
print("Start!")

while(True):
    print("Ouvindo")
    text=get_audio().lower()
    if text.count(WAKE_WORD[0])>0:
        speak("Hey! Como posso ajudar?")    
        text=get_audio()
        for frase in CALENDARIO_STRS:
            if frase in text.lower():
                data=get_data(text)
                if data:
                    get_events(data,service)
                else:
                    speak("Não entendi,fale a data com mais clareza.")
        for frase in NOTE_STRS:
            if frase in text.lower():
                    speak("O que você gostaria de anotar?")
                    note=get_audio().lower()
                    Anotar(note)
                    speak("Eu fiz uma nota!")
            
            
