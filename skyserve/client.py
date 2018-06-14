import base64
import os
import threading
import time
from multiprocessing import Value

import picamera

from skysense.base_client import BaseClient


class ImageClient(BaseClient):
    """
    Client to capture and save images from the Pi camera.
    """

    def __init__(self, directory='', resolution=(640, 480)):
        """
        Create an ImageClient instance.

        :param directory: directory to store images in
        :param resolution: resolution of images to capture
        """
        self.camera = picamera.PiCamera()
        self.camera.resolution = resolution
        self.directory = directory
        self.recording_flag = Value('i', False)

    def start(self, interval=5000):
        """
        Begin periodic capture of images at the specified interval.

        :param interval: interval (in ms) between snapshots
        """
        if not self.recording_flag.value:
            self.recording_flag.value = True

            def async_run():
                while self.recording_flag.value:
                    self.capture_single_image()
                    time.sleep(interval / 1000.)

            thread = threading.Thread(target=async_run, args=())
            thread.daemon = True
            thread.start()

    def read(self):
        """
        Read an image from the camera as a base64-encoded image string.

        :return: String representing the base64-encoded contents of the image.
        """
        temp_filename = 'single-capture.jpg'

        self.capture_single_image(name=temp_filename)

        image = open(temp_filename)
        contents = base64.b64encode(image.read())
        image.close()
        os.remove(os.path.join(self.directory, temp_filename))

        return contents

    def stop(self):
        """
        Stop periodic capture of images.
        """
        self.recording_flag.value = False

    def capture_single_image(self, name=''):
        """
        Capture a single image to a file.

        :param name: name of file to save
        """
        filename = name or time.strftime('%Y-%m-%d_%H-%M-%S.jpg')
        self.camera.capture(os.path.join(self.directory, filename))

    def close(self):
        """
        Close Picamera instance and release camera resources
        """
        self.camera.close()


class VideoClient(BaseClient):
    """
    Client to record video from the Pi camera.
    """

    def __init__(self, directory='', resolution=(320, 240), framerate=32):
        """
        Create a VideoClient instance.

        :param directory: directory to store videos in
        :param resolution: resolution of video to capture
        :param framerate: framerate of video to capture
        """
        self.camera = picamera.PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.directory = directory

    def start(self, name=None):
        """
        Begin video capture.

        :param name: Optional name of the file to save, with a valid extension. Default is
                     current timestamp with h264 extension.
        """
        time.sleep(0.1)     # camera warmup time

        if not self.camera.recording:
            filename = name or time.strftime('%Y-%m-%d_%H-%M-%S.h264')
            self.camera.start_recording(os.path.join(self.directory, filename))

    def stop(self):
        """
        Stop video capture.
        """
        if self.camera.recording:
            self.camera.stop_recording()

    def close(self):
        """
        Close Picamera instance and release camera resources
        """
        self.camera.close()
