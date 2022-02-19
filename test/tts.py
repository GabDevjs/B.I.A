#importarção da biblioteca 
import pyttsx3
 
engine = pyttsx3.init()# Init da função de voz
#definição da voz
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[-2].id)
#Definição de sintacse de voz primaria
engine.say("Bom dia")
engine.runAndWait()