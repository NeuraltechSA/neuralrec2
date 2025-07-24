#!/usr/bin/env python3
import sys
import os
import time
import gi


gi.require_version('GLib', '2.0') 
gi.require_version('GObject', '2.0')
gi.require_version('Gst', '1.0')

from gi.repository import Gst, GObject, GLib 



def on_bus_message(bus, message, loop):
        print("A")
        t = message.type
        if t == Gst.MessageType.EOS:
            print("End-of-stream\n")
            loop.quit()
        elif t==Gst.MessageType.WARNING:
            err, debug = message.parse_warning()
            print("Warning: %s: %s\n" % (err, debug))
        elif t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print("Error: %s: %s\n" % (err, debug))
            loop.quit()
        return True









pipeline = None
bus = None

# initialize GStreamer
Gst.init(None)

# URL del stream RTSP
rtsp_url = "rtsp://admin:neuraltech2025@127.0.0.1:8845" #"rtsp://127.0.0.1:8554/mystream"

# Nombre del archivo de salida
output_file = "video_grabado.mkv"

cells = "2:6,2:7,2:8,3:3,3:4,3:5,3:6,3:7,4:1,4:2,4:3,4:4,4:5,4:6,5:0,5:1,5:2,5:3,5:4,5:5,6:0,6:1,6:2,6:3,6:4,7:0,7:1,7:2,7:3,7:4,8:0,8:1,8:2,8:3,9:0,9:1,9:2"
# build the pipeline para guardar sin recodificar
pipeline = Gst.parse_launch(
    #f"rtspsrc location={rtsp_url} latency=0 ! rtph264depay ! h264parse ! matroskamux ! filesink location={output_file}"
    #f"rtspsrc location={rtsp_url} latency=0 ! rtph264depay  ! h264parse ! splitmuxsink location=video%02d.mkv muxer-factory=matroskamux max-size-time=10000000000"
    f"rtspsrc location={rtsp_url} latency=0 !  rtph264depay ! h264parse ! avdec_h264 ! video/x-raw ! videoconvert ! motioncells sensitivity=0.4 gridx=20 gridy=20 gap=2 motionmaskcellspos={cells} datafile=/app/motion ! videoconvert ! x264enc ! splitmuxsink location=video%02d.mkv muxer-factory=matroskamux max-size-time=10000000000"
    #xvimagesink splitmuxsink location=video%02d.mkv muxer-factory=matroskamux max-size-time=10000000000
)
#  motioncells calculatemotion=false !

def on_muxer_added(splitmuxsink, fragment_id, user_data):
    print(fragment_id)

splitmuxsink = pipeline.get_by_name("splitmuxsink0")
#splitmuxsink.connect("format-location", on_muxer_added, None)


#loop = GLib.MainLoop()
bus = pipeline.get_bus()
bus.add_signal_watch()
bus.connect("message", on_bus_message, None)

# start playing
print(f"Grabando video desde {rtsp_url} a {output_file}")
print("Presiona Ctrl+C para detener la grabación...")

pipeline.set_state(Gst.State.PLAYING)



#loop.run()
#pipeline.set_state(Gst.State.NULL)

while True:
    pass
    #print("Esperando...")
    #print(loop.is_running())
    #time.sleep(1)
