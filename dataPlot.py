import ast
import matplotlib.pyplot as plt
import matplotlib.dates as md
import datetime as dt

linelist = []
file = open('gasoutput0601.txt', 'r')
for line in file.readlines():
    linelist.append(line)

PM0_3 = []
PM0_5 = []
PM1_0 = []
PM2_5 = []
PM5_0 = []
PM50  = []
time_stamp = []

for i in range(0, len(linelist), 10):
    linelist[i] = ast.literal_eval(linelist[i])
    PM0_3.append(linelist[i]['PM0.3'])
    PM0_5.append(linelist[i]['PM0.5'])
    PM1_0.append(linelist[i]['PM1.0'])
    PM2_5.append(linelist[i]['PM2.5'])
    PM5_0.append(linelist[i]['PM5.0'])
    PM50.append(linelist[i]['PM50.0'])
    time_stamp.append(float(linelist[i]['time_stamp']))

print(time_stamp)
def mysubplot(yaxis, stryaxis):

    '''
    Used to setup the property for subplot, for x-axis, it will transfer unix timestamp to readable time
    :param yaxis: y-axis label
    :param stryaxis: string representation of y-axis
    :return: plot for different sizes of particles with time_stamp
    '''

    dates = [dt.datetime.fromtimestamp(ts) for ts in time_stamp]
    datenums = md.date2num(dates)
    plt.subplots_adjust(bottom=0.2)
    plt.xticks(rotation=25)
    ax = plt.gca()
    xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)
    plt.plot(datenums, yaxis, 'b')
    plt.title(stryaxis)
    plt.ylabel('concentration(ug/0.1L)')
    plt.xlabel('time_stamp')

plt.figure(figsize=(16, 10))
plt.subplot(3, 2, 1)
mysubplot(PM0_3, 'PM0.3')

plt.subplot(3, 2, 2)
mysubplot(PM0_5, 'PM0.5')

plt.subplot(3, 2, 3)
mysubplot(PM1_0, 'PM1.0')

plt.subplot(3, 2, 4)
mysubplot(PM2_5, 'PM2.5')

plt.subplot(3, 2, 5)
mysubplot(PM5_0, 'PM5.0')

plt.subplot(3, 2, 6)
mysubplot(PM50, 'PM50')

plt.suptitle('Particle Concentrations at 09523 W 2943 N', fontsize=15)
plt.tight_layout()
plt.savefig('Gas.png')


