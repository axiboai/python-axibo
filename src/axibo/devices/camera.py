from PIL import Image
from io import BytesIO

class Camera():

    def __init__(self, dev):
        self.dev = dev

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