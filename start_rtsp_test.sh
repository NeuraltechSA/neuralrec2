#!/bin/bash

# Script para iniciar streams RTSP de prueba
# Uso: ./start_rtsp_test.sh [opción]

set -e

echo "🚀 Iniciador de Streams RTSP de Prueba"
echo "======================================"

# Función para mostrar ayuda
show_help() {
    echo "Opciones disponibles:"
    echo "  1) ffmpeg     - Stream RTSP con FFmpeg (recomendado)"
    echo "  2) gstreamer  - Stream RTSP con GStreamer"
    echo "  3) docker     - Stream RTSP con Docker (MediaMTX)"
    echo "  4) test       - Probar conexión a stream existente"
    echo "  5) help       - Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  ./start_rtsp_test.sh ffmpeg"
    echo "  ./start_rtsp_test.sh gstreamer --mode camera"
    echo "  ./start_rtsp_test.sh test rtsp://127.0.0.1:8554/test"
}

# Función para verificar dependencias
check_dependencies() {
    echo "🔍 Verificando dependencias..."
    
    # Verificar FFmpeg
    if command -v ffmpeg &> /dev/null; then
        echo "✅ FFmpeg encontrado"
    else
        echo "❌ FFmpeg no encontrado. Instálalo con: sudo apt install ffmpeg"
        return 1
    fi
    
    # Verificar Python
    if command -v python3 &> /dev/null; then
        echo "✅ Python3 encontrado"
    else
        echo "❌ Python3 no encontrado"
        return 1
    fi
    
    echo "✅ Todas las dependencias están instaladas"
}

# Función para iniciar stream con FFmpeg
start_ffmpeg_stream() {
    echo "🎬 Iniciando stream RTSP con FFmpeg..."
    
    if [ ! -f "rtsp_test_server.py" ]; then
        echo "❌ Archivo rtsp_test_server.py no encontrado"
        return 1
    fi
    
    python3 rtsp_test_server.py "$@"
}

# Función para iniciar stream con GStreamer
start_gstreamer_stream() {
    echo "🎬 Iniciando stream RTSP con GStreamer..."
    
    if [ ! -f "gstreamer_rtsp_server.py" ]; then
        echo "❌ Archivo gstreamer_rtsp_server.py no encontrado"
        return 1
    fi
    
    python3 gstreamer_rtsp_server.py "$@"
}

# Función para iniciar stream con Docker
start_docker_stream() {
    echo "🐳 Iniciando stream RTSP con Docker..."
    
    if [ ! -f "docker-rtsp-test.yml" ]; then
        echo "❌ Archivo docker-rtsp-test.yml no encontrado"
        return 1
    fi
    
    echo "🚀 Iniciando contenedores Docker..."
    docker-compose -f docker-rtsp-test.yml up -d
    
    echo "✅ Servidor RTSP iniciado en Docker"
    echo "📺 URL del stream: rtsp://127.0.0.1:8554/test"
    echo "🔗 API: http://127.0.0.1:8888"
    echo ""
    echo "Para detener: docker-compose -f docker-rtsp-test.yml down"
}

# Función para probar conexión
test_connection() {
    local url="$1"
    
    if [ -z "$url" ]; then
        echo "❌ Debes especificar una URL RTSP"
        echo "Ejemplo: ./start_rtsp_test.sh test rtsp://127.0.0.1:8554/test"
        return 1
    fi
    
    echo "🔍 Probando conexión a: $url"
    
    if [ ! -f "test_rtsp_client.py" ]; then
        echo "❌ Archivo test_rtsp_client.py no encontrado"
        return 1
    fi
    
    python3 test_rtsp_client.py "$url" --test
}

# Función para mostrar streams disponibles
show_streams() {
    echo "📺 Streams RTSP disponibles:"
    echo "============================"
    echo ""
    echo "1. Stream básico:"
    echo "   URL: rtsp://127.0.0.1:8554/test"
    echo "   Comando: ./start_rtsp_test.sh ffmpeg"
    echo ""
    echo "2. Simulación de cámara:"
    echo "   URL: rtsp://127.0.0.1:8554/test"
    echo "   Comando: ./start_rtsp_test.sh ffmpeg --mode camera"
    echo ""
    echo "3. Stream con GStreamer:"
    echo "   URL: rtsp://127.0.0.1:8554/test"
    echo "   Comando: ./start_rtsp_test.sh gstreamer"
    echo ""
    echo "4. Stream con Docker:"
    echo "   URL: rtsp://127.0.0.1:8554/test"
    echo "   Comando: ./start_rtsp_test.sh docker"
    echo ""
    echo "5. Probar conexión:"
    echo "   Comando: ./start_rtsp_test.sh test rtsp://127.0.0.1:8554/test"
}

# Función principal
main() {
    local option="$1"
    shift
    
    case "$option" in
        "ffmpeg")
            check_dependencies
            start_ffmpeg_stream "$@"
            ;;
        "gstreamer")
            check_dependencies
            start_gstreamer_stream "$@"
            ;;
        "docker")
            start_docker_stream
            ;;
        "test")
            test_connection "$@"
            ;;
        "streams"|"list")
            show_streams
            ;;
        "help"|"-h"|"--help"|"")
            show_help
            ;;
        *)
            echo "❌ Opción desconocida: $option"
            show_help
            exit 1
            ;;
    esac
}

# Ejecutar función principal
main "$@" 