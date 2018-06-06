import matplotlib.pyplot as plt
import matplotlib.dates as md
import re
import datetime as dt

rtlpath = 'rtloutput1.txt'
irispath = 'irisoutput10601.txt'


def extractData(path):
    list_of_dict = []
    in_file = open(path, "rt")  # open file lorem.txt for reading text data
    contents = in_file.read()  # read the entire file into a string variable
    in_file.close()  # close the file
    strs = contents

    # Getting the strings time stamps and rssi values from the huge text file

    time_values_raw = re.findall(r"'time_stamp': '[+-]?\d+(?:\.\d+)?'", strs)
    rssi_values_raw = re.findall(r"'rssi': [+-]?\d+(?:\.\d+)?", strs)

    # Making the lists into giant strings (time_values_raw and rssi_values_raw still
    # contain phrases 'time_stamp': and 'rssi':)

    time_values_raw_string = ''.join(time_values_raw)
    rssi_values_raw_string = ''.join(rssi_values_raw)

    # Finding the numbers in the giant string to filter out those phrases mentioned above

    time = re.findall(r"[+-]?\d+(?:\.\d+)?", time_values_raw_string)
    rssi = re.findall(r"[+-]?\d+(?:\.\d+)?", rssi_values_raw_string)

    # Floating all the data

    time_data = [float(i) for i in time]
    rssi_data = [float(k) for k in rssi]

    return time_data, rssi_data

time_data_rtl, rssi_data_rtl = extractData(rtlpath)
time_data_iris, rssi_data_iris = extractData(irispath)
# print(len(rssi_data_rtl))
# print(len(time_data_rtl))
# print(len(rssi_data_iris))
# print(len(time_data_iris))

# adjust the number of sample used to plot
time_data_rtl = time_data_rtl[0:796]
time_data_iris = time_data_iris[0:796]
rssi_data_rtl = rssi_data_rtl[0:796]
rssi_data_iris = rssi_data_iris[0:796]


def mysubplot(yaxis, stryaxis, linetype, label, time_data):

    '''
    Used to setup the property for subplot, for x-axis, it will transfer unix timestamp to readable time
    :param yaxis: y-axis value
    :param stryaxis: string representation of y-axis
    :param linetype: line properties
    :param label:   label of the line used to form legend
    :param time_data: time_stamp
    :return: plot for different sizes of particles with time_stamp
    '''

    dates = [dt.datetime.fromtimestamp(ts) for ts in time_data]
    datenums = md.date2num(dates)
    plt.subplots_adjust(bottom=0.2)
    plt.xticks(rotation=25)
    ax = plt.gca()
    xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)
    plt.plot(datenums, yaxis, linetype, label=label)
    plt.title(stryaxis)
    plt.ylabel('concentration(ug/0.1L)')
    plt.xlabel('time_stamp')

# Plotting the data and saving it
plt.figure(figsize=(10, 16))
plt.subplot(3, 1, 1)

mysubplot(rssi_data_rtl, 'RSSI for RTL-SDR', 'r', 'RTL', time_data_rtl)

plt.subplot(3, 1, 2)
mysubplot(rssi_data_iris, 'RSSI for IRIS-SDR', 'b', 'IRIS', time_data_iris)

plt.subplot(3, 1, 3)
mysubplot(rssi_data_iris, 'RSSI for IRIS-SDR', 'b', 'IRIS', time_data_iris)
mysubplot(rssi_data_rtl, 'RSSI for RTL-SDR', 'r', 'RTL', time_data_rtl)
plt.legend(loc='upper right')

plt.title('RSSI Comparision')
plt.tight_layout()
plt.savefig('Comparision-RSSI')

# Weird data is located between 370th-ish and 400th-ish samples:

# print(rssi_data[370:400])
# plt.plot(time_data[370:400],rssi_data[370:400])
# plt.savefig('plot2')

