#!/usr/bin/env python3
"""
Script para crear un stream RTSP de prueba para testear la grabación
"""
import subprocess
import time
import signal
import sys
import os

class RTSPTestServer:
    def __init__(self, port=8554, stream_name="test"):
        self.port = port
        self.stream_name = stream_name
        self.process = None
        self.rtsp_url = f"rtsp://127.0.0.1:{port}/{stream_name}"
        
    def start_test_stream(self):
        """Inicia un stream RTSP de prueba usando FFmpeg"""
        print(f"🚀 Iniciando stream RTSP de prueba...")
        print(f"📺 URL del stream: {self.rtsp_url}")
        print(f"🎥 Puerto: {self.port}")
        print(f"📝 Nombre del stream: {self.stream_name}")
        print("=" * 50)
        
        # Comando FFmpeg para crear un stream RTSP de prueba
        # Genera un patrón de prueba con texto y colores
        cmd = [
            "ffmpeg",
            "-re",  # Leer a velocidad real
            "-f", "lavfi",
            "-i", "testsrc2=duration=3600:size=1280x720:rate=30",  # Patrón de prueba por 1 hora
            "-f", "lavfi",
            "-i", "sine=frequency=1000:duration=3600",  # Tono de audio
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-tune", "zerolatency",
            "-c:a", "aac",
            "-f", "rtsp",
            "-rtsp_transport", "tcp",
            f"rtsp://0.0.0.0:{self.port}/{self.stream_name}"
        ]
        
        try:
            print("🔄 Ejecutando FFmpeg...")
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            print("✅ Stream RTSP iniciado correctamente")
            print(f"🔗 Conecta tu grabador a: {self.rtsp_url}")
            print("⏹️  Presiona Ctrl+C para detener")
            
            # Mantener el proceso vivo
            self.process.wait()
            
        except KeyboardInterrupt:
            print("\n🛑 Deteniendo stream RTSP...")
            self.stop()
        except Exception as e:
            print(f"❌ Error al iniciar stream: {e}")
            self.stop()
    
    def start_camera_simulation(self):
        """Simula una cámara IP con movimiento"""
        print(f"📹 Iniciando simulación de cámara IP...")
        print(f"📺 URL del stream: {self.rtsp_url}")
        
        # Comando FFmpeg con patrón más realista
        cmd = [
            "ffmpeg",
            "-re",
            "-f", "lavfi",
            "-i", "testsrc2=duration=3600:size=1920x1080:rate=25",
            "-f", "lavfi", 
            "-i", "sine=frequency=800:duration=3600",
            "-filter_complex", 
            "[0:v]drawtext=text='CAMERA TEST %{pts\\:hms}':fontsize=60:fontcolor=white:x=50:y=50:box=1:boxcolor=black@0.5[v]",
            "-map", "[v]",
            "-map", "1:a",
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-tune", "zerolatency",
            "-b:v", "2000k",
            "-c:a", "aac",
            "-b:a", "128k",
            "-f", "rtsp",
            "-rtsp_transport", "tcp",
            f"rtsp://0.0.0.0:{self.port}/{self.stream_name}"
        ]
        
        try:
            self.process = subprocess.Popen(cmd)
            print("✅ Simulación de cámara iniciada")
            print("⏹️  Presiona Ctrl+C para detener")
            self.process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Deteniendo simulación...")
            self.stop()
    
    def stop(self):
        """Detiene el stream RTSP"""
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            print("✅ Stream RTSP detenido")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Servidor RTSP de prueba para grabación")
    parser.add_argument("--port", type=int, default=8554, help="Puerto RTSP (default: 8554)")
    parser.add_argument("--stream", default="test", help="Nombre del stream (default: test)")
    parser.add_argument("--mode", choices=["basic", "camera"], default="basic", 
                       help="Modo de stream: basic o camera simulation")
    
    args = parser.parse_args()
    
    server = RTSPTestServer(args.port, args.stream)
    
    try:
        if args.mode == "camera":
            server.start_camera_simulation()
        else:
            server.start_test_stream()
    except KeyboardInterrupt:
        print("\n👋 ¡Hasta luego!")
        server.stop()

if __name__ == "__main__":
    main() 