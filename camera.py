import argparse
import time
import picamera


def start(file, time):
    if time != 0:
        with picamera.PiCamera() as camera:
            #camera.resolution = (1280, 720)
            #camera.start_preview()
            camera.start_recording(file)
            camera.wait_recording(time)
            camera.stop_recording()
            #camera.stop_preview()
    else:
        with picamera.PiCamera() as camera:
            #camera.resolution = (1280, 720)
            #camera.start_preview()
            camera.capture(file)
            #camera.stop_preview()
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Record vidoes or capture pictures')

    parser.add_argument('-f', dest='file', type=str, help='stored file name')
    parser.add_argument('-t', dest='time', type=float, help='recording time, put 0 for pictures')
    
    args = parser.parse_args()
    file = args.file
    time = args.time
    
    start(file, time)

