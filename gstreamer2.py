#!/usr/bin/env python3
import sys
import os
import time
import gi


gi.require_version('GLib', '2.0') 
gi.require_version('GObject', '2.0')
gi.require_version('Gst', '1.0')

from gi.repository import Gst, GObject, GLib 





rtsp_url = "rtsp://admin:neuraltech2025@127.0.0.1:8845" #"rtsp://127.0.0.1:8554/mystream"
output_file = "video_grabado.mkv"
cells = "1:1"
#
Gst.init(None)

'''
f"""
        rtspsrc location={rtsp_url} latency=0  !
        rtph264depay !
        h264parse !
        avdec_h264 !
        video/x-raw !
        videoconvert !
        tee name=t
            t. ! queue ! motioncells name=motion postallmotion=true motionmaskcellspos={cells} ! xvimagesink
            t. ! queue ! valve name=recorder drop=false !
            videoconvert ! x264enc!
            mp4mux ! filesink location={output_file}
        """
'''


pipeline = Gst.parse_launch(
    f"""
        rtspsrc location={rtsp_url} latency=0  !
        rtph264depay !
        h264parse !
        avdec_h264 !
        video/x-raw !
        videoconvert !
        tee name=t
            t. ! queue ! motioncells gap=5 sensitivity=0.5 gridx=20 gridy=20 ! videoconvert ! fakesink async=false     
            t. ! queue ! valve name=display drop=true drop-mode=transform-to-gap ! videoconvert ! x264enc ! matroskamux ! filesink sync=false location={output_file}
        """
    # autovideosink sync=false
    #f"rtspsrc location={rtsp_url} latency=0 ! rtph264depay ! h264parse ! avdec_h264 ! video/x-raw ! tee name=t t. ! queue ! motioncells sensitivity=0.4 gridx=20 gridy=20 gap=2 postallmotion=true motionmaskcellspos={cells} ! fakesink ! t. ! queue ! valve name=recorder drop=true ! videoconvert ! x264enc ! splitmuxsink location=video%02d.mkv muxer-factory=matroskamux max-size-time=10000000000"
    #xvimagesink splitmuxsink location=video%02d.mkv muxer-factory=matroskamux max-size-time=10000000000
)


#  t. ! queue ! valve name=recorder drop=false ! xvimagesink

loop = GLib.MainLoop()
valve = pipeline.get_by_name("display")


def on_bus_message(bus, message):
    """Manejar mensajes del bus"""
    if message.get_structure():
        if message.get_structure().has_field("motion_begin"):
            valve.set_property("drop",False)
        if message.get_structure().has_field("motion_finished"):
            valve.set_property("drop",True)
        #struct_name = message.get_structure().get_name()
        #if struct_name == "motion":
        #    print(message.get_structure(),message.get_structure().has_field("motion_begin"))
            
        #if struct_name == "motion":
        #    # Movimiento detectado
        #    self.on_motion_detected(message)
        #elif struct_name == "gst-element-no-motion":
        #    # No hay movimiento
        #    self.on_no_motion()
    return True


bus = pipeline.get_bus()
bus.add_signal_watch()
bus.connect("message", on_bus_message)

pipeline.set_state(Gst.State.PLAYING)

loop.run()

