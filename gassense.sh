#!/bin/bash
cd
cd ./Desktop
sudo python sense.py -p output.txt -po /dev/ttyUSB0 -b 115200 -gb 9600 -gpo /dev/ttyACM0
