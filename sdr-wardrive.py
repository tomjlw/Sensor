import math
import argparse
import time
import numpy as np
import gmplot as gp
import matplotlib.pyplot as plt 

from rtlsdr import RtlSdr
from skyengine.drone import DroneController
from skyengine.exceptions import FlightAbortedException
from skylog.logger import DirectLogger
from skylog.message import BaseMessage
from skymission.concurrency import tick
from skymission.mission import Mission
from skymission.mission import callback
from skymission.mission import panic
from mapsplotlib import mapsplot as mplt

b = 0.9
a= 0
TURN = 3
Xdistance = 0.000009009
Ydistance = 0.000008983
#WIESS2 = (29.714898, -95.401886)

def direction(index, TXGPS):
  distance = b*2*math.pi*(1+index//4)
  if index % 4 == 0:    
    TX_X = TXGPS[1] + distance*Xdistance
    return TXGPS[0], TX_X
  elif index % 4 == 1:
    TX_Y = TXGPS[0] + distance*Ydistance
    return TX_Y, TXGPS[1]
  elif index % 4 == 2:
    TX_X = TXGPS[1] - distance*Xdistance
    return TXGPS[0], TX_X
  else:
    TX_Y = TXGPS[0] - distance*Ydistance
    return TX_Y, TXGPS[1]	
 				
class Waypoint:
    def __init__(self, lat, lon, alt):
        self.lat = lat
        self.lon = lon
        self.alt = alt


class LocationMessage(BaseMessage):
    """
    Message for the drone's current location.
    """

    def __init__(self, timestamp, lat, lon, alt, dBm):
        self.timestamp = timestamp
        self.lat = lat
        self.lon = lon
        self.alt = alt
	self.dBm = dBm
    
    def serialize(self):
        return {
            'timestamp': self.timestamp,
            'location':{
	      'lat': self.lat,
              'lon': self.lon,
              'alt': self.alt
            },
            'dBm': self.dBm
        }


class sdrwardriveMission(Mission):

    port = 4002
    mission_id = 'sdr-sdrwardrive'

    def __init__(self, fc_addr, log_file):
        """
        Create a sdrwardrive Mission and start the mission server.

        :param fc_addr: MAVProxy address of the flight controller.
        :param log_file: Name of the log file for location data.
        """
        self.enable_disk_event_logging()

        self.dc = DroneController(fc_addr)
        self.location_logger = DirectLogger(path=log_file)
        self.log.debug('Drone controller and logger initialized successfully')

        self.log.info('sdr-measure mission initialization complete')
        self.sdr = RtlSdr()
        self.log.debug('Configuring RTL-SDR sensor.')
        self.sdr.sample_rate = 2.048e6  # Hz
        self.sdr.center_freq = 563e6     # Hz
        self.freq_correction = 60   # PPM
        self.sdr.gain = 30	
	self.start_location_log()

        self.start_server()

    @tick(interval=0.5)
    def start_location_log(self):
        """
        Start periodically logging the drone GPS location and dBm to disk.
        """
	samples = self.sdr.read_samples(16384)
        dBm = 10 * np.log10(np.mean(np.power(np.abs(samples), 2)))

        location = self.dc.read_gps()
        message = LocationMessage(
            timestamp=time.time(),
            lat=location.lat,
            lon=location.lon,
            alt=location.alt,
	    dBm=dBm
        )

        self.location_logger.log(message)

    @callback(
        endpoint='/start-mission',
        description='Gives the drone a series of waypoints and starts the mission.',
        required_params=('waypoints', 'hover_duration'),
        public=True,
    )
    def start_mission(self, data, *args, **kwargs):
        """

        :param data: Required to be of the form:
                     [{
                         'lat': ...,  # Target latitude
                         'lon': ...,  # Target longitude
                         'alt': ...,  # Target altitude
                     }]
        """
	gmap = gp.GoogleMapPlotter(29.714898, -95.401886, 19)
	try:
            hover_duration = data['hover_duration']
            waypoints = [
                Waypoint(point['lat'], point['lon'], point['alt'])
                for point in data['waypoints']
            ]
            start_alt = waypoints[0].alt

            self.log.debug('Taking off to altitude: {alt}'.format(alt=start_alt))
            self.dc.take_off(start_alt)
            self.log.debug('Take off complete')
            for waypoint in waypoints:
		WPGPS = [waypoint.lat, waypoint.lon]
                self.log.debug('Navigating to waypoint: ({lat}, {lon})'.format(
                    lat=waypoint.lat,
                    lon=waypoint.lon,
                ))
                self.dc.goto(coords=(waypoint.lat, waypoint.lon), altitude=waypoint.alt, 			airspeed=5)
                self.log.debug('Navigation to waypoint complete')

                location = self.dc.read_gps()
                self.log.debug('Arrived! Current location: ({lat}, {lon})'.format(
                    lat=location.lat,
                    lon=location.lon,
                ))
		X=[]
		Y=[]
		X.append(waypoint.lon)
		Y.append(waypoint.lat)

	        for i in range(0, TURN*4):
		  self.log.debug('Navigating to waypoint: ({lat}, {lon})'.format(
	            lat=self.dc.read_gps().lat,
	            lon=self.dc.read_gps().lon,
	        ))		
		  X.append(direction(i, WPGPS)[1])
		  Y.append(direction(i, WPGPS)[0])
		  self.dc.goto(coords=(direction(i, WPGPS)[0], direction(i, WPGPS)[1]),   altitude=waypoint.alt, 			  airspeed=2) 
		  self.log.debug('Navigation to waypoint complete')

	          location = self.dc.read_gps()
	          self.log.debug('Arrived! Current location: ({lat}, {lon})'.format(
	            lat=location.lat,
	            lon=location.lon,
	        ))                
		  self.log.debug('Hovering for {hover_duration} seconds'.format(
	            hover_duration=hover_duration,
	        ))
	          time.sleep(hover_duration)
		index1 = -1
		self.log.debug('Return trip begins')
		for i in range(0, TURN*4):
  		  self.log.debug('Navigating to waypoint: ({lat}, {lon})'.format(
	          lat=self.dc.read_gps().lat,
	          lon=self.dc.read_gps().lon,
	        ))
		  self.dc.goto(coords=(Y[index1],X[index1]), altitude=(waypoint.alt+5), 			  airspeed=2) 
		  index1 -= 1
		  self.log.debug('Navigation to waypoint complete')
		  location = self.dc.read_gps()
	          self.log.debug('Arrived! Current location: ({lat}, {lon})'.format(
	            lat=location.lat,
	            lon=location.lon,
	        ))                
		  self.log.debug('Hovering for {hover_duration} seconds'.format(
	            hover_duration=hover_duration,
	        ))
	          time.sleep(hover_duration)
	
	    self.log.info('Navigation to all waypoints complete. Landing now.')
            self.dc.land()
	    gmap = gp.GoogleMapPlotter(waypoint.lat, waypoint.lon, 19)
	    gmap.scatter([Y[0]], [X[0]], 'blue', size=1, marker=False)
	    gmap.scatter(Y[1:], X[1:], 'red', size=1, marker=False)
	    gmap.plot(Y[0:2], X[0:2], 'blue', size=4, edge_width = 2.5, marker=False)
	    gmap.plot(Y[1:], X[1:], 'red', size=4, edge_width = 2.5, marker=False)
	    gmap.draw('{year}_{month}_{day}_{hour}_{min}_{sec}-sdrwardrive-path.html'.format(
        	year=time.localtime()[0],
        	month=time.localtime()[1],
        	day=time.localtime()[2],
        	hour=time.localtime()[3],
        	min=time.localtime()[4],
        	sec=time.localtime()[5],
        	),  
    )
            plt.plot(X[0:2],Y[0:2],'bo-')
	    plt.hold(True)	    
	    plt.plot(X[1:],Y[1:],'ro-')
	    plt.savefig('{year}_{month}_{day}_{hour}_{min}_{sec}-sdrwardrive-path.png'.format(
        	year=time.localtime()[0],
        	month=time.localtime()[1],
        	day=time.localtime()[2],
        	hour=time.localtime()[3],
        	min=time.localtime()[4],
        	sec=time.localtime()[5],
        	),  
    )
            self.log.info('Landed!')
        except FlightAbortedException:
            self.log.error('Flight aborted due to panic; aborting remaining tasks.')

    @panic
    def panic(self, *args, **kwargs):
        self.log.info('Mission panicked! Landing immediately.')
        self.dc.panic()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--fc-addr',
        dest='fc_addr',
        help='Address of the flight controller mavproxy messages',
        default=None,
    )
    parser.add_argument(
        '--log-file',
        dest='log_file',
        help='Path to the log file to create',
        default='{year}_{month}_{day}_{hour}_{min}_{sec}-sdr-wardrive.log'.format(
        	year=time.localtime()[0],
        	month=time.localtime()[1],
        	day=time.localtime()[2],
        	hour=time.localtime()[3],
        	min=time.localtime()[4],
        	sec=time.localtime()[5],
        	),  
    )

    args = parser.parse_args()

    sdrwardriveMission(
        fc_addr=args.fc_addr,
        log_file=args.log_file,
    )
