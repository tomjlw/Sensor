import serial
import argparse
import time


def time_record():
    """
    Record the time stamp for each sense and return a string to display the time
    """
    gmtime = time.gmtime(time.time())
    strftime = time.strftime("%a, %d %b %Y %H:%M:%S", gmtime)
    strftime = str(strftime)
    return strftime


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
    output_file = open(write_to_file_path, "w+")
    output_file.truncate()  # Clear the output file first
    print('sensing start')
    ser = serial.Serial(serial_port, baud_rate)
    while True:
        line = ser.readline()
        line = line.decode("utf-8", 'ignore')
        gps = serial.Serial(gport, baudrate=gbaud)
        data = gps.readline().split(',')    # read GPS data from receiver
        if data[0] == '$GPRMC':
            if data[2] == 'A':
                latitude = data[3:5]
                longitude = data[5:7]
                output_file.write(' ' + str(latitude) + str(longitude) + '   ')
                output_file.write(time_record() + '    ')
                output_file.write(line)

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

    sense_record(port, path, baud, gbaud, gport)