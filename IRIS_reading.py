#!/usr/bin/python
import SoapySDR
from SoapySDR import * #SOAPY_SDR_ constants
import numpy as np
np.set_printoptions(threshold='nan')
from optparse import OptionParser
import time
import os
import math
import sys
import datetime
import subprocess
import argparse
import subprocess
import serial

sys.path.append('../IrisBoardUtils')
#from FFTUtils import * # LogPowerFFT

serial1 = "0370"
freq_start = 563e6
freq_stop = 570e6
freq_step = 5e9
rate = 5e6
gain = 35
bw = 5e6
fft_size = 2048
numSamps = 2048
drone_IRIS_Power = -100.0

def time_record():
    """
    Record the time stamp for each sense and return a string to display the time
    """
    return str(time.time())

F = np.arange(freq_start,freq_stop,freq_step)
sampsRx = np.empty(numSamps).astype(np.complex64)
freq_resp = np.empty(len(F)).astype(np.float)

# sdr = SoapySDR.Device(dict(driver="iris", serial = serial))
sdr = SoapySDR.Device(dict(driver="remote", serial = serial1))
sdr.setMasterClockRate(rate*8)
# sdr.SoapySDR_setLogLevel(1)


for c in [0]:
    sdr.setFrequency(SOAPY_SDR_RX, 0, "RF", F[c])
    sdr.setBandwidth(SOAPY_SDR_RX, c, bw)
    sdr.setSampleRate(SOAPY_SDR_RX, c, rate)
    sdr.setGain(SOAPY_SDR_RX, 0, gain)
    sdr.setDCOffsetMode(SOAPY_SDR_RX, c, True)
    sdr.setAntenna(SOAPY_SDR_RX, c, sdr.listAntennas(SOAPY_SDR_RX, c)[0])
    # sdr.setAntenna(SOAPY_SDR_RX, c, sdr.listAntennas(SOAPY_SDR_RX, c)[1])

rxStream = sdr.setupStream(SOAPY_SDR_RX, "CF32", [0])

count=1
while True:
    for f in range(len(F)):
        # time.sleep(0.001)
        # flags = SOAPY_SDR_WAIT_TRIGGER | SOAPY_SDR_END_BURST
        flags = SOAPY_SDR_END_BURST
        sdr.activateStream(rxStream, flags, 0, numSamps)
        numRecv = 0
        sampsRx = np.empty(numSamps).astype(np.complex64)
        # sdr.writeSetting("TRIGGER_GEN","")
        while numRecv < numSamps:
            sr = sdr.readStream(rxStream, [sampsRx[numRecv:]], numSamps-numRecv, timeoutUs=long(1e6))
            if sr.ret < 0: raise Exception(str(sr))
            numRecv += sr.ret
        sampsRx = sampsRx - np.mean(sampsRx)
        freq_resp[f] = 10*np.log10(np.mean(np.power(np.abs(sampsRx),2)))

        drone_IRIS_Power = freq_resp[f]  

    index = 'test'+str(count)
    count += 1
    time_stamp = time_record()
    rssi = drone_IRIS_Power
    sample = sampsRx
    write_to_file_path = 'irisoutput1.log'
    gps = serial.Serial('/dev/ttyACM0', baudrate=9600)
    data = gps.readline().split(',')    # read GPS data from receiver
    with open(write_to_file_path, "a") as output_file:
        if data[0] == '$GPRMC':
           # print(data1[0:6], data)
           if data[2] == 'A':
               latitude = data[3:5]
               longitude = data[5:7]
               log = {'index':index, 'time_stamp':time_stamp, 'sample': sample, 
		      'rssi':rssi, 'longitude':longitude, 'latitude':latitude}
               output_file.write(str(log) + '\n')
        else:
            log = {'index':index, 'time_stamp':time_stamp, 'sample': sample, 'rssi':rssi}
            output_file.write(str(log) + '\n')

sdr.closeStream(rxStream)
