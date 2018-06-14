import time
from skysense.camera import ImageClient

camera = ImageClient()
mode = 'o'
interval = 5000     # this equals to time.sleep(interval/1000)
name='foo.jpg'
camera.directory = './'

if __name__ == '__main__':
    if (mode == 'c'):
        camera.start(interval=interval)
        print('capture starting: ')
        camera.stop()
        camera.close()
            
    elif (mode == 'o'):
        camera.capture_single_image(name)
        camera.stop()
        camera.close()
        
    

