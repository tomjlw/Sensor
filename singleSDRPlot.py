import matplotlib.pyplot as plt
import matplotlib.dates as md
import re
import datetime as dt

list_of_dict = []
in_file = open("rtloutput1.txt", "rt") # open file lorem.txt for reading text data
contents = in_file.read()         # read the entire file into a string variable
in_file.close()                   # close the file
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
# Formatting the Unix timestamps into something readable

dates = [dt.datetime.fromtimestamp(td) for td in time_data]
datenums = md.date2num(dates)
plt.subplots_adjust(bottom=0.2)
plt.xticks( rotation=25 )
ax=plt.gca()
xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
ax.xaxis.set_major_formatter(xfmt)

# Plotting the data and saving it

plt.plot(datenums,rssi_data)
plt.title('RSSI for IRIS-SDR')
plt.savefig('123123IRIS-RSSI')

# Weird data is located between 370th-ish and 400th-ish samples:

# print(rssi_data[370:400])
# plt.plot(time_data[370:400],rssi_data[370:400])
# plt.savefig('plot2')

