<div>
    <p align="center">
        <a href="#readme">
            <img alt="Axibo logo" src="https://global-uploads.webflow.com/5edc12e499287365c3769453/6176cfc85658d3efc70f30b3_axlogo_white.svg">
        </a>
    </p>
    <p align="center">
        <a href="https://pypi.python.org/pypi/loguru"><img alt="Pypi version" src="https://img.shields.io/pypi/v/loguru.svg"></a>
        <a href="https://pypi.python.org/pypi/loguru"><img alt="Python versions" src="https://img.shields.io/badge/python-3.5%2B%20%7C%20PyPy-blue.svg"></a>
    </p>
    </p>
    </div>


**python-axibo** is a library used to interface with AXIBO INC hardware

The AXIBO ecosystem of hardware components can be easily controlled using this library. This library was created to allow users to extend the applications of Axibo hardware beyond what is avalible in the application.

This library can be used to connect AXIBO to virtual production tools as well as writing custom applications for AI, motion detect and tracking, stop motion animation and anything else a user may want to use AXIBO for. Features are exposed so that they can be used for out-of-the-box creative expression. A slider can be used to much more than a slider with this library. 

Installation
------------
```bash
git clone https://github.com/axiboai/python-axibo.git
cd python-axibo
pip install . 
```

Simple Usage
------------
Make sure your AXIBO controller is connected to the network. Once connected you will be able to import and initialize the module. Check out the samples for more details.
```python
from axibo import Axibo

my_axibo = Axibo("192.168.1.2") #make sure to change this to your AXIBO!

my_axibo.camera.capture_image_to_file("test_image.jpg")

my_axibo.pan.move_absolute(angle=10.00, speed=5.00)
my_axibo.pan.move_absolute(angle=5.00, speed=2.50)
my_axibo.update()
```

Supported Hardware
--------
* `PT4 Pan Unit`
* `PT4 Tilt Unit`
* `PT4 Controller`
* `PT4 Slider High Speed`
* `PT4 Slider High Torque`
* `FZ1 Focus & Zoom Motor`
* `J1 Universal Joint`

Features
--------

* `Interface with multiple AXIBO controllers`
* `Control absolute movements of any Axis connected to and AXIBO controller`
* `Capture images to python or a file for post processing`
* `Launch tracking services`
* `Get outputs from AXIBO's AI Engine`

