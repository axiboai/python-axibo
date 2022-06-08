import requests
import json
import websocket
from threading import Thread
import time
from PIL import Image
import io

from axibo.devices import pan
from axibo.devices import tilt
from axibo.devices import slide
from axibo.devices import camera
from axibo.devices import focus


class AxiboWebSocketHardwareStream:
    def __init__(self, ip):
        self.stop_thread = False
        self.status_message = {}
        self.device_status_message = {}
        websocket.enableTrace(False)
        self.ws = websocket.WebSocketApp("ws://{}:2100/ws".format(ip),
                                on_message = self.on_message,
                                on_error = self.on_error,
                                on_close = self.on_close)
        #self.ws.on_open = self.on_open
        def async_ws_event_loop():
            self.ws.run_forever()

        ws_thread = Thread(target=async_ws_event_loop)
        ws_thread.daemon = True
        ws_thread.start()
        self.is_live = False

    def parse_message(self, message):
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

    def on_open(ws):
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

    def load_action(self,action_type='req_put', data=None):
        if action_type == 'req_put':
            self.load_api_request(data)

    def load_api_request(self, data):
        action_key = list(data.keys())[0]
        if action_key not in self.actions.keys():
            self.actions.update({action_key : {'type' : 'req_put', 'data' : {}}})
        self.actions[action_key]['data'].update(data[action_key])
        
    def execute_api_requests(self):
        for action in list(self.actions.keys()):
            this_action = self.actions[action]
            if this_action['type'] == 'req_put':
                data = this_action['data']
                self.request_put(action, data)
        self.actions = {}

    def request_put(self, uri, data, params=None):
        url = "http://{}:2200/v1/".format(self.ip) + uri
        headers = {'Content-type': 'application/json'}
        ret = requests.put(
            url, timeout=self.timeout, data=json.dumps(data), params=params, headers=headers).json()
        return ret

    def request_get(self, uri, params=None):
        url = "http://{}:2200/v1/".format(self.ip) + uri
        ret = requests.get(
            url, timeout=self.timeout, params=params)
        return ret

    def request_get_image(self, uri, params=None):
        url = "http://{}:2200/v1/".format(self.ip) + uri
        ret = requests.get(url)
        return ret
        

class Axibo:

    def __init__(self, ip):
        self.dev = AxiboDeviceParameters(ip)
        self.pan = pan.Pan(self.dev)
        self.tilt = tilt.Tilt(self.dev)
        self.focus = focus.Focus(self.dev)
        self.slide = slide.Slide(self.dev)
        self.camera = camera.Camera(self.dev)

    def update(self):
        self.dev.execute_api_requests()
        
    def stop(self):
        self.dev.request_put('direct-control/stop-motion', {})

    def connected(self):
        try:
            data = self.dev.request_get('system/status')
            return True
        except:
            return False
    
    def version(self):
        data = self.dev.request_get('system/info')
        return data['version']


