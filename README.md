# PM2.5 Sensing
## Wiring
Wirng is pretty simple, just wire the pin of orange wire of the sensor to Arduino GND Pin, purple wire pin to Arduino 5V Pin and any digital output pin(here I use the D2 pin in Arduino Nano).
Details can be found [here](https://cdn-learn.adafruit.com/downloads/pdf/pm25-air-quality-sensor.pdf)

## Configuration
clone the project in your local machine and open the terminal 

run ```pip install pySerial```
run ```cd $yourownpath/PM2.5_Sensor/``` 

Open PM2.5 Sensor.ino and customize the configuration as you want(including communication rate, serial communication rate and pin configuration). 

Then upload the program to Arduino. Now the sensing mission will keep running as long as the Arduino is charged.

## Record Data and Generate Output File
To start recording data, run the following command in the terminal
```shell
python senseRecord.py -h
python senseRecord.py -p $path -b $baud_rate -po $port -gb $GPSbadu_rate -gpo $GPSport
```
One example command:

``
python senseRecord.py -p output.txt -po /dev/ttyUSB0 -b 115200 -gb 19200 -gpo /dev/ttyACM0
``

Then it will record the sensing data and generate a output file in the path you want
  