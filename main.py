#Iciniando codigo
import speech_recognition as sr
#Cria um reconhecedor 
r = sr.Recognizer()
#Seletor de idiomas 
Lv = 'pt'
#Abrir p microfone para captura
with sr.Microphone() as soure:
    while True:
        audio = r.listen(soure) #Define microfone como fonte de audio
        
        print(r.recognize_google(audio,  language=Lv))