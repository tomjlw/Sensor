import serial
import argparse
import time
import os


def time_record():
    """
    Record the time stamp for each sense and return a string to display the time
    """
    os.environ['TZ'] = 'US/Central'
    time.tzset()
    localtime = time.localtime(time.time())
    strftime = time.strftime("%a, %d %b %Y %H:%M:%S ", localtime)
    strftime = str(strftime)
    return strftime

def aqi_evaluation(PM):
    """
    Give evaluation on air quality based on the concentration of PM2.5
    :param PM: Concentration of PM2.5
    :return: Evaluation of air quality
    """
    if PM <= 15:
        return 'Good'
    elif PM <= 40:
        return 'Moderate'
    elif PM <= 65:
        return 'Unhealthy for Sensitive Group'
    elif PM <= 150:
        return 'Unhealthy'
    elif PM <= 250:
        return 'Very Unhealthy'
    elif PM > 250:
        return 'Hazardous'


def sense_record(port, path, baud, gbaud, gport):
    """
    :param port: port for Arduino
    :param path: path for the file that stores data
    :param baud: baud rate for the communication between Arduino and Serial
    :param gbaud: baud rate for the communication between GPS and Serial
    :param gport: port for GPS
    :return:
    """
    serial_port = port
    baud_rate = baud  # In Arduino, Serial.begin(baud_rate)
    write_to_file_path = path
    ser = serial.Serial(serial_port, baud_rate)
    line = ser.readline()
    line = line.decode("utf-8", 'ignore')
    data1 = line.split(',')
    evaluation = aqi_evaluation(int(data1[3]))

    gps = serial.Serial(gport, baudrate=gbaud)
    data = gps.readline().split(',')    # read GPS data from receiver
    print(data1, data)
    with open(write_to_file_path, "a") as output_file:
        if data[0] == '$GPRMC':
           # print(data1[0:6], data)
           if data[2] == 'A':
               latitude = data[3:5]
               longitude = data[5:7]

               measure_data = {'time_stamp': str(time_record()), 'longitude': longitude, 'latitude': latitude,
                               'PM0.3': int(data1[0]), 'PM0.5': int(data1[1]),
                               'PM1.0': int(data1[2]), 'PM2.5': int(data1[3]),
                               'PM5.0': int(data1[4]), 'PM50.0': int(data1[5]), 'evaluation': evaluation}
               numbermap={'time_stamp': 1, 'longitude': 2, 'latitude': 3, 'PM0.3': 4, 'PM0.5': 5, 'PM1.0': 6,
                          'PM2.5': 7, 'PM5.0': 8, 'PM50.0': 9, 'evaluation': 10}
               sorted(measure_data, key=numbermap.__getitem__)
               output_file.write(str(measure_data) + '\n')
        else:
            measure_data = {'time_stamp': str(time_record()),
                            'PM0.3': int(data1[0]), 'PM0.5': int(data1[1]),
                            'PM1.0': int(data1[2]), 'PM2.5': int(data1[3]),
                            'PM5.0': int(data1[4]), 'PM50.0': int(data1[5]), 'evaluation': evaluation}
            numbermap = {'time_stamp': 1, 'PM0.3': 2, 'PM0.5': 3, 'PM1.0': 4,
                         'PM2.5': 5, 'PM5.0': 6, 'PM50.0': 7, 'evaluation': 8}
            sorted(measure_data, key=numbermap.__getitem__)
            output_file.write(str(measure_data) + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Read data from PM2.5 sensor and write to a designated file')

    parser.add_argument('-p', dest='path', type=str,
                        help='Path used to store the output file with format as desktop/project/sensor/output.txt'
                        )
    parser.add_argument('-po', dest='port', type=str, help='Port for Arduino')
    parser.add_argument('-b', dest='baud', type=int, help='Baud rate used to communicate between Arduino and serial')
    parser.add_argument('-gpo', dest='gport', type=str, help='Port for GPS Receiver')
    parser.add_argument('-gb', dest='gbaud', type=int, help='Baud rate used to communicate between GPS and serial')

    args = parser.parse_args()
    baud = args.baud
    port = args.port
    gbaud = args.gbaud
    gport = args.gport
    path = args.path
    print('Sensing start')
    print('Concentration Unit: um/0.1L')
    while True:
        sense_record(port, path, baud, gbaud, gport)
