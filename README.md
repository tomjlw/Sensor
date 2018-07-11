
# PM2.5 Sensing
## Wiring
Wirng is pretty simple, just wire the pin of orange wire of the sensor to Arduino GND Pin, purple wire pin to Arduino 5V Pin and any digital output pin(here I use the D2 pin in Arduino Nano).
Details can be found [here](https://cdn-learn.adafruit.com/downloads/pdf/pm25-air-quality-sensor.pdf). Also, connect GM1-86 GPS receiver(if you have) to Raspberry Pi/Laptop.

## Configuration
clone the project in your local machine and open the terminal 

run ```pip install pySerial```

run ```pip install matplotlib```

run ```cd $yourownpath/GAS/PM2.5_Sensor/``` 

Open PM2.5 Sensor.ino and customize the configuration as you want(including communication rate, serial communication rate and pin configuration). 

Then upload the program to Arduino. Now the sensing mission will keep running as long as the Arduino is charged.

## Record Data and Generate Output File
To start recording data, run the following command in the terminal
```shell
python sense.py -h
python sense.py -p $path -b $baud_rate -po $port -gb $GPSbadu_rate -gpo $GPSport
```
One example command:

``
python sense.py -p output.txt -po /dev/ttyUSB0 -b 115200 -gb 19200 -gpo /dev/ttyACM0
``

Then it will record the sensing data and generate a output file in the path you want

Output file should look like:
``
{'PM0.5': 991, 'PM50.0': 0, 'PM2.5': 12, 'PM0.3': 3357, 'time_stamp': '1527803157.44', 'evaluation': 'Good', 'PM5.0': 3, 'PM1.0': 189}
{'PM0.5': 991, 'PM50.0': 0, 'PM2.5': 12, 'PM1.0': 189, 'PM0.3': 3357, 'latitude': ['2943.19061', 'N'], 'time_stamp': '1527803159.81', 'evaluation': 'Good', 'PM5.0': 3, 'longitude': ['09523.93542', 'W']}
`` 
## Plot and Analyze data 
### dataPlot.py
dataPlot.py is used to plot data from the log file. To run it, you need to first change some parameters by doing following things:

run ```sudo nano /$yourpath/GAS/PM2.5_Sensor/dataPlot.py```

change the path for log file: ```file = open('$yourpath', 'r')```

change the path for picture storage: ```plt.savefig('$yourpath')```

change the sample number: ```for i in range(0, len(linelist), $samplenumber): ```

After the configuration, you can simply run the script by using:
```python dataPlot.py```

Notice: If you have more than a thousand of data, running will take about 20 minutes

### multiPlot.py
multiPlot.py is used to plot data from several different places into one graph in order to compare.

## Update: Configured for Automation
If you want to execute the script on RaspberryPi automatically from the startup, you can do the following configuration:

run ```sudo chmod +x $yourpath/GAS/PM2.5_Sensor/gassense.sh```
 
run ```nano ~/.config/lxsession/LXDE-pi/autostart``` 

add
> @/$yourpath/gassense.sh 

in the end of script

save and exit

reboot the raspberrypi and now every time it reboots, it will automatically run the script and generate a log file as long as all the hardwares are set up. If you want to stop, just unplug the Arduino. But if you want to start sensing again, you need either reboot or execute the sense.py from command lines as shown above.
.
├── dataPlot
│   ├── dBmVsDistance
│   ├── dBmVsTime
│   ├── errortimeVsSamples
│   ├── errorVsDrones
│   ├── logs
│   ├── pictures
│   └── util

