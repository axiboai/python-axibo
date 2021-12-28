from axibo import Axibo
import time

if __name__ == '__main__':
    import random
    x = Axibo("192.168.2.39")
    
    x.camera.set_resolution(640, 480)
    print("Set camera resolution, waiting for autoexpsure to adjust")
    time.sleep(2)
    x.camera.capture_image_to_file("test_image.jpg")
    print("Captured image from Axibo")

