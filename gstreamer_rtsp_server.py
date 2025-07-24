#!/usr/bin/env python3
"""
Servidor RTSP usando GStreamer para testear grabación
"""
import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')

from gi.repository import Gst, GstRtspServer, GLib
import sys
import time

class GStreamerRTSPServer:
    def __init__(self, port=8554):
        self.port = port
        self.server = None
        self.mainloop = None
        
    def create_media_factory(self):
        """Crea un factory para el stream de prueba"""
        factory = GstRtspServer.RTSPMediaFactory()
        
        # Pipeline para generar video de prueba
        pipeline_str = (
            "( videotestsrc pattern=ball is-live=true ! "
            "video/x-raw,width=1280,height=720,framerate=30/1 ! "
            "videoconvert ! x264enc tune=zerolatency ! "
            "rtph264pay name=pay0 pt=96 )"
        )
        
        factory.set_launch(pipeline_str)
        factory.set_shared(True)
        
        return factory
    
    def create_audio_video_factory(self):
        """Crea un factory con audio y video"""
        factory = GstRtspServer.RTSPMediaFactory()
        
        pipeline_str = (
            "( videotestsrc pattern=ball is-live=true ! "
            "video/x-raw,width=1280,height=720,framerate=25/1 ! "
            "videoconvert ! x264enc tune=zerolatency ! "
            "rtph264pay name=pay0 pt=96 "
            "audiotestsrc wave=sine is-live=true ! "
            "audio/x-raw,rate=44100 ! "
            "audioconvert ! avenc_aac ! "
            "rtpmp4apay name=pay1 pt=97 )"
        )
        
        factory.set_launch(pipeline_str)
        factory.set_shared(True)
        
        return factory
    
    def create_camera_simulation_factory(self):
        """Simula una cámara IP real"""
        factory = GstRtspServer.RTSPMediaFactory()
        
        pipeline_str = (
            "( videotestsrc pattern=smpte is-live=true ! "
            "video/x-raw,width=1920,height=1080,framerate=25/1 ! "
            "videoconvert ! "
            "textoverlay text='CAMERA SIMULATION' font-desc='Sans 24' "
            "valignment=top halignment=left ! "
            "x264enc tune=zerolatency bitrate=2000 ! "
            "rtph264pay name=pay0 pt=96 "
            "audiotestsrc wave=sine frequency=800 is-live=true ! "
            "audio/x-raw,rate=44100 ! "
            "audioconvert ! avenc_aac ! "
            "rtpmp4apay name=pay1 pt=97 )"
        )
        
        factory.set_launch(pipeline_str)
        factory.set_shared(True)
        
        return factory
    
    def start_server(self, mode="basic"):
        """Inicia el servidor RTSP"""
        Gst.init(None)
        
        # Crear servidor RTSP
        self.server = GstRtspServer.RTSPServer()
        
        # Configurar puerto
        self.server.set_service(str(self.port))
        
        # Crear factory según el modo
        if mode == "camera":
            factory = self.create_camera_simulation_factory()
        elif mode == "audio_video":
            factory = self.create_audio_video_factory()
        else:
            factory = self.create_media_factory()
        
        # Agregar factory al servidor
        mount_points = self.server.get_mount_points()
        mount_points.add_factory("/test", factory)
        
        # Adjuntar servidor al mainloop
        self.server.attach(None)
        
        print(f"🚀 Servidor RTSP iniciado en puerto {self.port}")
        print(f"📺 URL del stream: rtsp://127.0.0.1:{self.port}/test")
        print(f"🎥 Modo: {mode}")
        print("⏹️  Presiona Ctrl+C para detener")
        
        # Crear y ejecutar mainloop
        self.mainloop = GLib.MainLoop()
        try:
            self.mainloop.run()
        except KeyboardInterrupt:
            print("\n🛑 Deteniendo servidor RTSP...")
            self.stop()
    
    def stop(self):
        """Detiene el servidor RTSP"""
        if self.mainloop:
            self.mainloop.quit()
        print("✅ Servidor RTSP detenido")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Servidor RTSP con GStreamer")
    parser.add_argument("--port", type=int, default=8554, help="Puerto RTSP (default: 8554)")
    parser.add_argument("--mode", choices=["basic", "audio_video", "camera"], 
                       default="basic", help="Modo del stream")
    
    args = parser.parse_args()
    
    server = GStreamerRTSPServer(args.port)
    
    try:
        server.start_server(args.mode)
    except KeyboardInterrupt:
        print("\n👋 ¡Hasta luego!")
        server.stop()

if __name__ == "__main__":
    main() 