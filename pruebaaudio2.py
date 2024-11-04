import speech_recognition as sr
import pyttsx3
import spacy

# Inicializar el reconocedor de voz y el modelo NLP
recognizer = sr.Recognizer()
nlp = spacy.load("es_core_news_sm")

# Función para convertir texto a voz
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Función para procesar texto y verificar intención
def check_intent(text):
    doc = nlp(text)
    # Buscar palabras clave para temperatura y humedad
    if "la temperatura y la humedad" in text.lower():
        response = "La temperatura actual es de 25 grados Celsius y la humedad del 58 por ciento."
        print("Intención: Solicitud de temperatura y humedad.")
    elif "dime la temperatura" in text.lower():
        response = "La Temperatura actual es del 28 grados celsius."
        print("Intención: Solicitud de temperatura.")   
    elif "dime la humedad" in text.lower():
        response = "La humedad actual es del 60%."
        print("Intención: Solicitud de humedad.")
    else:
        response = "No se solicitó información específica."
    speak_text(response)
    return None

# Función para analizar un archivo de audio WAV
def analizar_archivo_wav(ruta_archivo):
    with sr.AudioFile(ruta_archivo) as source:
        audio = recognizer.record(source)  # Cargar el audio del archivo
        try:
            text = recognizer.recognize_google(audio, language="es-ES")
            print("Texto capturado:", text)
            check_intent(text)
        except sr.UnknownValueError:
            print("No se pudo entender el audio.")
        except sr.RequestError as e:
            print(f"Error al conectarse al servicio de reconocimiento: {e}")

# Ruta del archivo de audio WAV
ruta_archivo = "servicio-audio/audio_received.wav"  # Reemplaza con la ruta del archivo .wav

# Llamada a la función para analizar el archivo
analizar_archivo_wav(ruta_archivo)
