import ast
import matplotlib.pyplot as plt
import matplotlib.dates as md
import datetime as dt

calength = 146      # length used to fit several lines in the same plot, must be smaller or equal than the smallest
                    # length of any list that stores the measured list

# Dataset at Rice University
PM0_3 = []
PM0_5 = []
PM1_0 = []
PM2_5 = []
PM5_0 = []
PM50  = []
time_stamp = []

# Dataset at CharlesH Park
PM0_3_1 = []
PM0_5_1 = []
PM1_0_1 = []
PM2_5_1 = []
PM5_0_1 = []
PM50_1  = []
time_stamp_1 = []

# Dataset at Peiser Park
PM0_3_2 = []
PM0_5_2 = []
PM1_0_2 = []
PM2_5_2 = []
PM5_0_2 = []
PM50_2  = []
time_stamp_2 = []

# Dataset at Mason Park
PM0_3_3 = []
PM0_5_3 = []
PM1_0_3 = []
PM2_5_3 = []
PM5_0_3 = []
PM50_3  = []
time_stamp_3 = []


def data_collect(path, step, PM0_3, PM0_5, PM1_0, PM2_5, PM5_0, PM50, timestamp):
    '''
    The function is used to collect data from different datasets
    :param path: path for the file you want to read
    :param step: step value which is used to choose number of samples
    :return: seven arrays that store corresponding particle concentrations and a time_stamp array
    '''
    linelist = []
    file = open(path, 'r')
    for line in file.readlines():
        linelist.append(line)
    for i in range(0, len(linelist), step):
        linelist[i] = ast.literal_eval(linelist[i])
        PM0_3.append(linelist[i]['PM0.3'])
        PM0_5.append(linelist[i]['PM0.5'])
        PM1_0.append(linelist[i]['PM1.0'])
        PM2_5.append(linelist[i]['PM2.5'])
        PM5_0.append(linelist[i]['PM5.0'])
        PM50.append(linelist[i]['PM50.0'])
        timestamp.append(float(linelist[i]['time_stamp']))

data_collect('gasoutput0601.txt', 2, PM0_3, PM0_5, PM1_0, PM2_5, PM5_0, PM50, time_stamp)
data_collect('output.txt', 2, PM0_3_1, PM0_5_1, PM1_0_1, PM2_5_1, PM5_0_1, PM50_1, time_stamp_1)
data_collect('output2.txt', 2, PM0_3_2, PM0_5_2, PM1_0_2, PM2_5_2, PM5_0_2, PM50_2, time_stamp_2)
data_collect('output3.txt', 2, PM0_3_3, PM0_5_3, PM1_0_3, PM2_5_3, PM5_0_3, PM50_3, time_stamp_3)

def mysubplot(yaxis, stryaxis, linetype, label):

    '''
    Used to setup the property for subplot, for x-axis, it will transfer unix timestamp to readable time
    :param yaxis: y-axis label
    :param stryaxis: string representation of y-axis
    :return: plot for different sizes of particles with time_stamp
    '''

    dates = [dt.datetime.fromtimestamp(ts) for ts in time_stamp[0:calength]]
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

plt.figure(figsize=(16, 10))
plt.subplot(3, 2, 1)
mysubplot(PM0_3_1[0:calength],'PM0.3', 'r', 'CharlesH Park')
mysubplot(PM0_3_2[0:calength],'PM0.3', 'g', 'Peiser Park')
mysubplot(PM0_3_3[0:calength],'PM0.3', 'y', 'Mason Park')

mysubplot(PM0_3[0:calength], 'PM0.3', 'b', 'Rice University')
plt.legend(loc='upper right')

plt.subplot(3, 2, 2)
mysubplot(PM0_5_1[0:calength],'PM0.5', 'r', 'CharlesH Park')
mysubplot(PM0_5_2[0:calength],'PM0.5', 'g', 'Peiser Park')
mysubplot(PM0_5_3[0:calength],'PM0.5', 'y', 'Mason Park')

mysubplot(PM0_5[0:calength], 'PM0.5','b', 'Rice University')
plt.legend(loc='upper right')

plt.subplot(3, 2, 3)
mysubplot(PM1_0_1[0:calength],'PM1.0', 'r', 'CharlesH Park')
mysubplot(PM1_0_2[0:calength],'PM1.0', 'g', 'Peiser Park')
mysubplot(PM1_0_3[0:calength],'PM1.0', 'y', 'Mason Park')

mysubplot(PM1_0[0:calength], 'PM1.0', 'b', 'Rice University')
plt.legend(loc='upper right')

plt.subplot(3, 2, 4)
mysubplot(PM2_5_1[0:calength],'PM2.5', 'r', 'CharlesH Park')
mysubplot(PM2_5_2[0:calength],'PM2.5', 'g', 'Peiser Park')
mysubplot(PM2_5_3[0:calength],'PM2.5', 'y', 'Mason Park')

mysubplot(PM2_5[0:calength], 'PM2.5', 'b', 'Rice University')
plt.legend(loc='upper right')

plt.subplot(3, 2, 5)
mysubplot(PM5_0_1[0:calength],'PM5.0', 'r', 'CharlesH Park')
mysubplot(PM5_0_2[0:calength],'PM5.0', 'g', 'Peiser Park')
mysubplot(PM5_0_3[0:calength],'PM5.0', 'y', 'Mason Park')

mysubplot(PM5_0[0:calength], 'PM5.0', 'b', 'Rice University')
plt.legend(loc='upper right')

plt.subplot(3, 2, 6)
mysubplot(PM50_1[0:calength],'PM50', 'r', 'CharlesH Park')
mysubplot(PM50_2[0:calength],'PM50', 'g', 'Peiser Park')
mysubplot(PM50_3[0:calength],'PM50', 'y', 'Mason Park')

mysubplot(PM50[0:calength], 'PM50', 'b', 'Rice University')
plt.legend(loc='upper right')
plt.suptitle('Particle Concentrations Comparision between Rice and Three Parks', fontsize=15)
plt.tight_layout()
plt.savefig('Gas11.png')
