from playsound import playsound
from gtts import gTTS

with open('frases.txt','r') as f:
    frase = f.read()
    tts = gTTS(frase,lang='pt-br')
    tts.save('frase.mp3')
    playsound('frase.mp3')
