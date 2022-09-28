from axibo import Axibo
import time

if __name__ == '__main__':    
    #Change for you Axibos IP Address
    x = Axibo("10.42.0.1")

    # x.camera.set_resolution(640,480)

    time.sleep(1)

    #Uncomment for live view.
    x.camera.camera_view()

    #uncomment for capture to file
    #x.camera.capture_image_to_file("example.jpg")