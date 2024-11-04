
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
    if "dime la temperatura y la humedad" in text.lower():
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


def escuchar_palabra_clave():
    """Escucha continuamente hasta oír la palabra 'asistente'."""
    with sr.Microphone() as source:
        print("Diga 'asistente' para activar la grabación.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        while True:
            try:
                audio = recognizer.listen(source, timeout=5)
                texto = recognizer.recognize_google(audio, language="es-ES").lower()
                print("Escuchado:", texto)
                if "asistente" in texto:
                    return True  # Pasamos a la grabación completa
            except sr.UnknownValueError:
                print("No se pudo entender el audio.")
            except sr.RequestError as e:
                print(f"Error en el servicio de reconocimiento: {e}")

print("Presiona 'Ctrl+C' para detener el programa.")

try:
    while True:
        if(escuchar_palabra_clave()):
            with sr.Microphone() as source:
                try:
                    recognizer.adjust_for_ambient_noise(source)
                    recognizer.pause_threshold = 0.8
                    print("Palabra clave detectada. Comenzando grabación...")
                    audio = recognizer.listen(source)
                    text = recognizer.recognize_google(audio, language="es-ES")
                    print("Texto capturado:", text)
                    check_intent(text) 
                except sr.UnknownValueError:
                    print("No se pudo entender el audio.")
                except sr.RequestError as e:
                    print(f"Error al conectarse al servicio de reconocimiento: {e}")
except KeyboardInterrupt:
    print("\nPrograma detenido.")



