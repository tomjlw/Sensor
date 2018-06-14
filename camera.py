import time
from skysense.camera import VideoClient


duration = 0

class Video():
    
    def __init__(self):
        """
        Initialize some internal mission state.
        """
        self.camera = None
        self.video_start_time = None
 
    def start(self, data, *args, **kwargs):
        """
        Start recording a video. This endpoint is idempotent.
        """
        data = data or {}
        directory = data.get('directory', '')
        filename = data.get('name')
        resolution_width = data.get('width', 1920)
        resolution_height = data.get('height', 1080)
        fps = data.get('fps', 30)

        self.video_start_time = time.time()
        self.camera = VideoClient(
            directory=directory,
            resolution=(resolution_width, resolution_height),
            framerate=fps,
        )
        self.camera.start(name=filename)


    def stop(self, *args, **kwargs):
        """
        Stop recording a video. This endpoint is idempotent.
        """
        self.camera.stop()
        self.camera.close()
        self.camera = None
        self.video_start_time = None


if __name__ == '__main__':
	if duration == 0:
		camera = Video()
		camera.start()
		input=input('Video Recording, press S to stop')
		if (input == 's') or (input == 'S'):
			camera.stop()
			camera.close()
	else:
		camera = Video()
		camera.start()
		time.sleep(duration)
		camera.stop()
		camera.close()
