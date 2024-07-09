import requests
import json
import websocket
from threading import Thread
import time
import requests

from axibo.tools import camera
from axibo.tools import utilities
from axibo.tools import ai
from axibo.tools import waypoint
from axibo.tools import motion
from axibo.tools import system


class AxiboWebSocketHardwareStream:
    def __init__(self, ip):
        self.stop_thread = False
        self.status_message = {}
        self.device_status_message = {}
        self.connected_axis=[]
        websocket.enableTrace(False)
        self.ws = websocket.WebSocketApp("ws://{}:2100/ws".format(ip),
                                on_message = self.on_message,
                                on_error = self.on_error,
                                on_close = self.on_close)
        self.ws.on_open = self.on_open
        def async_ws_event_loop():
            self.ws.run_forever()

        ws_thread = Thread(target=async_ws_event_loop)
        ws_thread.daemon = True
        ws_thread.start()
        self.is_live = False

    def parse_message(self, message):
        self.connected_axis=message['axies']
        # print(self.connected_axis)
        for device in message['data']:
            self.device_status_message[device['axis']] = device

    def on_message(self, ws, message):
        self.is_live = True
        temp = json.loads(message)
        self.parse_message(json.loads(temp['data']))

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, error, message):
        pass

    def on_open(self, ws):
        def run(*args):
            for i in range(3):
                time.sleep(1)
                ws.send("f %d" % i)
            time.sleep(1)
            ws.close()
            print("thread terminating...")
        ws_thread = Thread(target=run)
        ws_thread.start()
    
class AxiboDeviceParameters:
    def __init__(self, ip):
       
        self.ip = ip
        self.actions = {}
        self.stream = AxiboWebSocketHardwareStream(self.ip)
        start_time = time.time()
        while 1:
            if time.time()-start_time > 2.0:
                raise Exception("Axibo not connected")
            if self.stream.is_live == True:
                break
        self.timeout = 1000
        
class Axibo:

    def __init__(self, ip="none"):
        if(ip=="none"):
            ip=utilities.find_axibos()
            if(ip=="none"):
                raise Exception("Axibo not connected")
            
        self.dev = AxiboDeviceParameters(ip)
        self.camera = camera.Camera(self.dev)
        self.ai = ai.AI(self.dev)
        self.waypoint = waypoint.Waypoint(self.dev)
        self.motion = motion.MotionRoute(self.dev)
        self.system = system.System(self.dev)


