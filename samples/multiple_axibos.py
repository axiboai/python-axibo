from axibo import Axibo
import time

if __name__ == '__main__':
    import random
    ax1 = Axibo("192.168.2.39")
    ax2 = Axibo("192.168.2.101")
    
    ax1.camera.set_resolution(640, 480)
    ax2.camera.set_resolution(1920, 1080)
    time.sleep(2)
    ax1.camera.capture_image_to_file("axibo_1.jpg")
    print("grabbed image from Axibo #1")
    ax2.camera.capture_image_to_file("axibo_2.jpg")
    print("grabbed image from Axibo #2")