const express = require('express');
const morgan = require('morgan');
const fs = require('fs');
const { exec } = require('child_process');  // Importar el módulo para ejecutar comandos

const app = express();
const port = 8888;

// Configurar el middleware de registro de solicitudes con un formato personalizado
app.use(morgan('dev'));

// Middleware para el cuerpo de solicitudes
app.use(express.raw({ type: 'audio/wav', limit: '50mb' }));

// Ruta para manejar la solicitud de carga de audio
app.post('/uploadAudio', (req, res) => {
    const audioData = req.body;
    console.log(`Recibido audio con tamaño: ${audioData.length}`);

    // Guardar el archivo de audio recibido
    const audioPath = 'audio_received.wav';
    fs.writeFileSync(audioPath, audioData);

    // Ejecutar el script de Python para procesar el archivo
    //C:\Users\KYTIA\Repositorio_Proyecto_Grupal\pruebaaudio2.py
    exec(`python script.py ${audioPath}`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error ejecutando el script de Python: ${error}`);
            return res.status(500).send('Error al procesar el audio');
        }

        // Si todo va bien, enviar la salida del script de Python
        console.log(`Salida del script: ${stdout}`);
        res.send('Audio recibido y procesado con éxito');
    });
});

// Middleware de manejo de errores
app.use((err, req, res, next) => {
    console.error('Se ha producido un error:', err);
    if (err.type === 'entity.too.large') {
        return res.status(413).send('Archivo demasiado grande');
    }
    return res.status(500).send('Ocurrió un error en el servidor');
});

// Iniciar el servidor
const server = app.listen(port, () => {
    console.log(`Servidor escuchando en http://localhost:${port}`);
});

// Manejar eventos de conexión
server.on('connection', (socket) => {
    console.log('Cliente conectado');
});

// Manejar eventos de desconexión
server.on('close', () => {
    console.log('Servidor cerrado');
});

// Middleware para imprimir los detalles de la solicitud
app.use((req, res, next) => {
    console.log('Detalles de la solicitud:');
    req.on('data', (chunk) => {
        console.log(chunk.toString());
    });
    next();
});
