from config import openaiapikey
import openai
from gtts import gTTS
from vosk import Model, KaldiRecognizer
from playsound import playsound
import pyaudio
import json
import os

openai.api_key = openaiapikey

mensagens = []
msg_sistema = input("Que tipo de chatbot gostaria de criar?: ")
mensagens.append({"role": "system", "content": msg_sistema})


modelo = Model(lang = "pt")
reconhecedor = KaldiRecognizer(modelo,16000)
microfone = pyaudio.PyAudio()
reconhecer = microfone.open(format=pyaudio.paInt16, channels=1, rate = 16000, input=True, frames_per_buffer = 8192)
reconhecer.start_stream()

print("Seu novo assistente está pronto, fale a sua mensagem!")

def chatGPT():
    while True:
        dados = reconhecer.read(4096, exception_on_overflow=False)

        if reconhecedor.AcceptWaveform(dados):
            resultado = reconhecedor.Result()
            texto = json.loads(resultado)["text"].strip()  # convert JSON to string and remove leading/trailing whitespaces
            print(texto)

            if texto:  # verifica se há texto antes de enviar para o modelo
                mensagens.append({"role": "user", "content": texto})
                chat = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=mensagens)
                resposta = chat["choices"][0]["message"]["content"]
                mensagens.append({"role": "assistant", "content": resposta})

                with open('frases.txt', 'w') as f:
                    f.write(resposta)

                with open('frases.txt', 'r') as f:
                    audio = f.read()
                    tts = gTTS(audio, lang='pt-br')
                    tts.save('frase.mp3')
                    playsound('frase.mp3')
                    os.remove('frase.mp3')

                print("\n" + resposta + "\n")
                if texto.lower() == 'sair':
                    break
            else:
                print("Nenhuma frase detectada. Por favor, fale novamente.")
    
chatGPT()