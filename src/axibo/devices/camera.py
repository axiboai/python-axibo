from PIL import Image
from io import BytesIO
import requests
import cv2
import numpy as np

class Camera():

    def __init__(self, dev):
        self.dev = dev
        self.stream_url ='http://{}:2101/mjpeg'.format(self.dev.ip)

    def capture_image_to_file(self, file_name='axibo_image.jpg'):
        response = self.dev.request_get_image(uri='imaging/cam')
        with open(file_name, 'wb') as f:
            f.write(response.content)

    def capture_pil_image(self):
        response = self.dev.request_get_image(uri='imaging/cam')
        return Image.open(BytesIO(response.content))

    def set_resolution(self, width=720, height=640):
        data = { "imgWidth": int(width), "imgheight": int(height)}
        ret = self.dev.request_put(uri='imaging/config', data=data)
        
    def read(self):
        r = requests.get(self.stream_url, stream=True)
        if(r.status_code == 200):
            bytes = b""
            for chunk in r.iter_content(chunk_size=1024):
                bytes += chunk
                a = bytes.find(b'\xff\xd8')
                b = bytes.find(b'\xff\xd9')
                if a != -1 and b != -1:
                    jpg = bytes[a:b+2]
                    bytes = bytes[b+2:]
                    i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    return i
        else:
            raise ValueError("Received unexpected status code {}".format(r.status_code))