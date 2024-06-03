import json
import random
from textblob import TextBlob
from googletrans import Translator
import tkinter as tk
from tkinter import scrolledtext

# Se utiliza el traductor de Google debido a que el modelo solo entiende en ingles por defecto
traductor = Translator()

# Cargar datos de respuesta predeterminados en el intents
with open('intents.json', 'r', encoding='utf-8') as archivo:
    intenciones = json.load(archivo)

# Función para analizar sentimientos usando TextBlob y realizando la traducción
def analizar_sentimiento(texto):
    # Traducir el texto a inglés
    traducido = traductor.translate(texto, src='es', dest='en')
    texto_en = traducido.text

    # Analizar el sentimiento en inglés
    blob = TextBlob(texto_en)
    polaridad_sentimiento = blob.sentiment.polarity

    # Categorizar el sentimiento dependiendo de su valor 
    sentimiento = 'NEUTRAL'
    if polaridad_sentimiento > 0:
        sentimiento = 'POSITIVO'
    elif polaridad_sentimiento < 0:
        sentimiento = 'NEGATIVO'
    return sentimiento, polaridad_sentimiento

# Función para obtener una respuesta simple del chatbot con los intents
def obtener_respuesta(entrada_usuario):
    etiqueta = None
    for intencion in intenciones['intents']:
        for patron in intencion['patterns']:
            if patron.lower() in entrada_usuario.lower():
                etiqueta = intencion['tag']
                break
        if etiqueta:
            break

    if etiqueta:
# Aqui se selecciona una respuesta random dentro de las predeterminadas especificas para que el
# bot no siempre responda lo mismo pero si se quede dentro de las limitaciones.
        respuesta_bot = random.choice(intencion['responses'])
    else:
        respuesta_bot = "Lo siento, no entiendo tu pregunta."

    sentimiento, confianza = analizar_sentimiento(entrada_usuario)
    return respuesta_bot, sentimiento, confianza

# Función para enviar mensajes a la interfaz de tkinter
def enviar_mensaje():
    entrada_usuario = entrada_texto.get()
    if entrada_usuario.strip():
        ventana_chat.configure(state='normal')
        ventana_chat.insert(tk.END, f"Tú: {entrada_usuario}\n")
        respuesta, sentimiento, confianza = obtener_respuesta(entrada_usuario)
        ventana_chat.insert(tk.END, f"Bot: {respuesta}\n")
        ventana_chat.insert(tk.END, f"Sentimiento: {sentimiento} (confianza: {confianza:.2f})\n\n")
        ventana_chat.configure(state='disabled')
        entrada_texto.delete(0, tk.END)
        ventana_chat.yview(tk.END)

# Configurar la ventana principal con el Tkinter
raiz = tk.Tk()
raiz.title("Chatbot con Análisis de Sentimientos")

# Crear la ventana de chat
ventana_chat = scrolledtext.ScrolledText(raiz, state='disabled', wrap='word')
ventana_chat.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Crear el input de texto para el usuario
entrada_texto = tk.Entry(raiz)
entrada_texto.pack(padx=10, pady=10, fill=tk.X)
entrada_texto.bind("<Return>", lambda event: enviar_mensaje())

# Crear el botón de submit o enviar el mensaje
boton_enviar = tk.Button(raiz, text="Enviar", command=enviar_mensaje)
boton_enviar.pack(padx=10, pady=10)

# Iniciar el bucle para que constantemente esté funcionando y recibiendo mensajes, igual que el de imágenes anterior
raiz.mainloop()
