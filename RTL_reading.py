import numpy as np
import time
import serial
from pylab import *
from rtlsdr import RtlSdr


sdr = RtlSdr()
sdr.sample_rate = 2.048e6  # Hz
sdr.center_freq = 500e6     # Hz
sdr.freq_correction = 60   # PPM
sdr.gain = 'auto'

count = 0

while True:
	count += 1
	index = 'test' + str(count)
	samples =sdr.read_samples(512)
        write_to_file_path = 'rtloutput1.log'
	rssi = 10 * np.log10(np.mean(np.power(np.abs(samples - np.mean(samples)), 2)))
	time_stamp = str(time.time())

        gps = serial.Serial('/dev/ttyACM0', baudrate=9600)
        data = gps.readline().split(',')    # read GPS data from receiver

        with open(write_to_file_path, "a") as output_file:
          if data[0] == '$GPRMC':
          # print(data1[0:6], data)
            if data[2] == 'A':
              latitude = data[3:5]
              longitude = data[5:7]
              log = {'index':index, 'time_stamp':time_stamp, 'sample': samples, 
		      'rssi':rssi, 'longitude':longitude, 'latitude':latitude}
              output_file.write(str(log) + '\n')
            else:
              log = {'index':index, 'time_stamp':time_stamp, 'sample': samples, 'rssi':rssi}
              output_file.write(str(log) + '\n')


