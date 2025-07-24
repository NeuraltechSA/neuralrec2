#!/usr/bin/env python3
"""
Cliente de prueba para verificar streams RTSP
"""
import cv2
import time
import argparse
import sys

class RTSPTestClient:
    def __init__(self, rtsp_url):
        self.rtsp_url = rtsp_url
        self.cap = None
        
    def test_connection(self):
        """Prueba la conexión al stream RTSP"""
        print(f"🔍 Probando conexión a: {self.rtsp_url}")
        
        try:
            # Configurar captura RTSP
            self.cap = cv2.VideoCapture(self.rtsp_url)
            
            # Configurar buffer para RTSP
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            
            if not self.cap.isOpened():
                print("❌ No se pudo abrir el stream RTSP")
                return False
            
            print("✅ Conexión RTSP establecida")
            
            # Leer algunos frames para verificar
            frame_count = 0
            start_time = time.time()
            
            while frame_count < 30:  # Leer 30 frames
                ret, frame = self.cap.read()
                if not ret:
                    print(f"❌ Error al leer frame {frame_count}")
                    break
                
                frame_count += 1
                if frame_count % 10 == 0:
                    print(f"📹 Frames leídos: {frame_count}")
            
            elapsed_time = time.time() - start_time
            fps = frame_count / elapsed_time if elapsed_time > 0 else 0
            
            print(f"✅ Stream funcionando correctamente")
            print(f"📊 Frames leídos: {frame_count}")
            print(f"⏱️  Tiempo: {elapsed_time:.2f}s")
            print(f"🎬 FPS estimado: {fps:.2f}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error al conectar: {e}")
            return False
        finally:
            if self.cap:
                self.cap.release()
    
    def display_stream(self, duration=10):
        """Muestra el stream en una ventana"""
        print(f"📺 Mostrando stream por {duration} segundos...")
        
        try:
            self.cap = cv2.VideoCapture(self.rtsp_url)
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            
            if not self.cap.isOpened():
                print("❌ No se pudo abrir el stream")
                return
            
            start_time = time.time()
            frame_count = 0
            
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("❌ Error al leer frame")
                    break
                
                # Mostrar frame
                cv2.imshow('RTSP Test Stream', frame)
                
                frame_count += 1
                
                # Salir con 'q' o después del tiempo especificado
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
                if time.time() - start_time > duration:
                    break
            
            elapsed_time = time.time() - start_time
            fps = frame_count / elapsed_time if elapsed_time > 0 else 0
            
            print(f"📊 Frames mostrados: {frame_count}")
            print(f"⏱️  Tiempo: {elapsed_time:.2f}s")
            print(f"🎬 FPS: {fps:.2f}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            if self.cap:
                self.cap.release()
            cv2.destroyAllWindows()

def main():
    parser = argparse.ArgumentParser(description="Cliente de prueba RTSP")
    parser.add_argument("url", help="URL del stream RTSP")
    parser.add_argument("--test", action="store_true", help="Solo probar conexión")
    parser.add_argument("--display", type=int, default=10, help="Mostrar stream por N segundos")
    
    args = parser.parse_args()
    
    client = RTSPTestClient(args.url)
    
    if args.test:
        success = client.test_connection()
        sys.exit(0 if success else 1)
    else:
        client.display_stream(args.display)

if __name__ == "__main__":
    main() 