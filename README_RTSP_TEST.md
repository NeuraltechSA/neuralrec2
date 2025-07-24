# 🎬 Streams RTSP de Prueba para Grabación

Este conjunto de herramientas te permite crear streams RTSP de prueba para testear tu sistema de grabación de video.

## 📋 Requisitos

### Dependencias básicas
```bash
# FFmpeg (para streams de prueba)
sudo apt update
sudo apt install ffmpeg

# Python y dependencias
pip install opencv-python
```

### Para GStreamer (opcional)
```bash
# GStreamer y librerías RTSP
sudo apt install gstreamer1.0-tools gstreamer1.0-plugins-base gstreamer1.0-plugins-good
sudo apt install gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly
sudo apt install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
sudo apt install libgstreamer-plugins-bad1.0-dev gstreamer1.0-libav

# Python GStreamer bindings
pip install PyGObject
```

### Para Docker (opcional)
```bash
# Docker y Docker Compose
sudo apt install docker.io docker-compose
sudo usermod -aG docker $USER
```

## 🚀 Uso Rápido

### Opción 1: FFmpeg (Recomendado)
```bash
# Stream básico
./start_rtsp_test.sh ffmpeg

# Simulación de cámara IP
./start_rtsp_test.sh ffmpeg --mode camera

# Puerto personalizado
./start_rtsp_test.sh ffmpeg --port 8555 --stream mytest
```

### Opción 2: GStreamer
```bash
# Stream básico
./start_rtsp_test.sh gstreamer

# Con audio y video
./start_rtsp_test.sh gstreamer --mode audio_video

# Simulación de cámara
./start_rtsp_test.sh gstreamer --mode camera
```

### Opción 3: Docker (MediaMTX)
```bash
# Iniciar servidor RTSP con Docker
./start_rtsp_test.sh docker

# Detener
docker-compose -f docker-rtsp-test.yml down
```

### Opción 4: Probar conexión
```bash
# Probar stream existente
./start_rtsp_test.sh test rtsp://127.0.0.1:8554/test

# Mostrar stream en ventana
python3 test_rtsp_client.py rtsp://127.0.0.1:8554/test --display 30
```

## 📺 URLs de Stream Disponibles

| Método | URL | Descripción |
|--------|-----|-------------|
| FFmpeg | `rtsp://127.0.0.1:8554/test` | Stream básico de prueba |
| GStreamer | `rtsp://127.0.0.1:8554/test` | Stream con GStreamer |
| Docker | `rtsp://127.0.0.1:8554/test` | Stream con MediaMTX |

## 🔧 Configuración para tu Grabador

### Actualizar tu código de grabación
Modifica tu archivo `gstreamer.py` para usar el stream de prueba:

```python
# Cambiar esta línea:
rtsp_url = "rtsp://admin:neuraltech2025@127.0.0.1:8845"

# Por esta:
rtsp_url = "rtsp://127.0.0.1:8554/test"
```

### Probar con tu grabador
```bash
# 1. Iniciar stream de prueba
./start_rtsp_test.sh ffmpeg

# 2. En otra terminal, ejecutar tu grabador
python3 gstreamer.py

# 3. Verificar que funciona
./start_rtsp_test.sh test rtsp://127.0.0.1:8554/test
```

## 🛠️ Opciones Avanzadas

### FFmpeg con parámetros personalizados
```bash
# Stream de alta calidad
python3 rtsp_test_server.py --port 8555 --stream hq --mode camera

# Stream de baja latencia
ffmpeg -re -f lavfi -i testsrc2=duration=3600:size=1920x1080:rate=30 \
  -c:v libx264 -preset ultrafast -tune zerolatency \
  -f rtsp -rtsp_transport tcp rtsp://0.0.0.0:8554/test
```

### GStreamer con pipeline personalizado
```bash
# Pipeline personalizado
gst-launch-1.0 videotestsrc pattern=ball is-live=true ! \
  video/x-raw,width=1280,height=720,framerate=30/1 ! \
  videoconvert ! x264enc tune=zerolatency ! \
  rtph264pay ! udpsink host=127.0.0.1 port=8554
```

### Docker con configuración personalizada
```bash
# Editar rtsp-config.yml para personalizar
# Luego ejecutar:
docker-compose -f docker-rtsp-test.yml up -d
```

## 🔍 Troubleshooting

### Problema: "No se puede conectar al stream"
```bash
# 1. Verificar que el servidor esté corriendo
netstat -tlnp | grep 8554

# 2. Probar con VLC
vlc rtsp://127.0.0.1:8554/test

# 3. Verificar logs
docker-compose -f docker-rtsp-test.yml logs
```

### Problema: "FFmpeg no encontrado"
```bash
# Instalar FFmpeg
sudo apt update
sudo apt install ffmpeg

# Verificar instalación
ffmpeg -version
```

### Problema: "GStreamer no funciona"
```bash
# Instalar dependencias completas
sudo apt install gstreamer1.0-tools gstreamer1.0-plugins-base gstreamer1.0-plugins-good
sudo apt install gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly

# Verificar instalación
gst-launch-1.0 --version
```

## 📊 Monitoreo

### Verificar estado del stream
```bash
# Probar conexión
./start_rtsp_test.sh test rtsp://127.0.0.1:8554/test

# Ver estadísticas (Docker)
curl http://127.0.0.1:8888/v3/paths/list
```

### Logs en tiempo real
```bash
# FFmpeg
python3 rtsp_test_server.py 2>&1 | tee rtsp.log

# Docker
docker-compose -f docker-rtsp-test.yml logs -f
```

## 🎯 Casos de Uso

### 1. Desarrollo local
```bash
# Iniciar stream de prueba
./start_rtsp_test.sh ffmpeg

# Ejecutar tu aplicación de grabación
python3 record.py
```

### 2. Testing automatizado
```bash
# Script de prueba
#!/bin/bash
./start_rtsp_test.sh ffmpeg &
sleep 5
./start_rtsp_test.sh test rtsp://127.0.0.1:8554/test
python3 gstreamer.py
```

### 3. Simulación de cámara IP
```bash
# Stream que simula una cámara real
./start_rtsp_test.sh ffmpeg --mode camera
```

## 📝 Notas Importantes

- **Puerto por defecto**: 8554
- **Protocolo**: RTSP sobre TCP (más estable)
- **Formato**: H.264 + AAC
- **Resolución**: 1280x720 (configurable)
- **FPS**: 30 (configurable)

## 🔗 Enlaces Útiles

- [FFmpeg RTSP Documentation](https://ffmpeg.org/ffmpeg-protocols.html#rtsp)
- [GStreamer RTSP Server](https://github.com/GStreamer/gst-rtsp-server)
- [MediaMTX (Docker)](https://github.com/aler9/mediamtx)
- [OpenCV RTSP](https://docs.opencv.org/4.x/d8/dfe/classcv_1_1VideoCapture.html)

## 🤝 Contribuir

Si encuentras problemas o quieres mejorar estas herramientas:

1. Verifica que el problema no esté en la configuración
2. Revisa los logs para más detalles
3. Prueba con diferentes opciones (FFmpeg vs GStreamer vs Docker)
4. Documenta el problema y la solución

¡Happy testing! 🎬 