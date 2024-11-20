
import sys
import wave
import json
from vosk import Model, KaldiRecognizer
import pyttsx3
from collections import defaultdict  # Para agrupar respuestas similares
import influxdb_client
from influxdb_client import InfluxDBClient

# Configuración de InfluxDB
bucket = "kytiandata"
org = "kytian"
url = "http://localhost:8086"
token = "f_PMdLFj6yLPUnnan2ICh3shyWPCH5wowrIy7DsVTC4YigDFyU_6fhpaC0G4zHK4L1v8CII2HTMmiez8Ls5oUg=="
client = InfluxDBClient(url=url, token=token, org=org)
query_api = client.query_api()

queryh = 'from(bucket:"kytiandata")\
|> range(start: -1m)\
|> filter(fn:(r) => r._measurement == "Porcentaje DHT22")\
|> filter(fn:(r) => r._field == "value")'
queryt = 'from(bucket:"kytiandata")\
|> range(start: -1m)\
|> filter(fn:(r) => r._measurement == "celsius SHT3X")\
|> filter(fn:(r) => r._field == "value")'

# Diccionario de intenciones y respuestas
intenciones = defaultdict(list)
intenciones["temperatura"].append("La temperatura actual es de {} grados Celsius.")
intenciones["humedad"].append("La humedad actual es del {}%.")
intenciones["ambas"].append("La temperatura actual es de {} grados Celsius y la humedad del {}%.")

# Función para convertir texto a voz
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Función para procesar texto y verificar intención
def check_intent(text):
    text = text.lower()
    if "temperatura y la humedad" in text:
        intencion = "ambas"
    elif "humedad" in text:
        intencion = "humedad"
    elif "temperatura" in text:
        intencion = "temperatura"
    else:
        intencion = "desconocida"

    if intencion in intenciones:
        resulth = query_api.query(org=org, query=queryh)
        resultsh = [record.get_value() for table in resulth for record in table.records]
        
        resultt = query_api.query(org=org, query=queryt)
        resultst = [record.get_value() for table in resultt for record in table.records]

        respuesta = intenciones[intencion][0].format(resultst[0], resultsh[0])  # Valores de ejemplo
        print(f"Intención: {intencion}")
        print(resultst[0])
        print(resultsh[0])
        speak_text(respuesta)
    else:
        print("Intención desconocida.")
        speak_text("No entiendo tu pregunta.")

# Función para analizar un archivo de audio WAV usando Vosk
def analizar_archivo_wav(ruta_archivo):
    model = Model("model")  # Asegúrate de descargar un modelo Vosk compatible y descomprimirlo en la carpeta "model"
    with wave.open(ruta_archivo, "rb") as wf:
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [8000, 16000]:
            print("El archivo de audio debe ser mono WAV con frecuencia de muestreo de 8000 o 16000 Hz.")
            return

        rec = KaldiRecognizer(model, wf.getframerate())
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                print("Texto capturado:", text)
                check_intent(text)

# Verificar si el archivo de audio se pasa como argumento
if len(sys.argv) > 1:
    ruta_archivo = sys.argv[1]  # Obtener la ruta del archivo desde el argumento
    analizar_archivo_wav(ruta_archivo)
else:
    print("Se debe pasar la ruta del archivo de audio WAV como argumento.")

