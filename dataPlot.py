import ast
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

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

for i in range(0,len(linelist)):
    linelist[i] = ast.literal_eval(linelist[i])
    PM0_3.append(linelist[i]['PM0.3'])
    PM0_5.append(linelist[i]['PM0.5'])
    PM1_0.append(linelist[i]['PM1.0'])
    PM2_5.append(linelist[i]['PM2.5'])
    PM5_0.append(linelist[i]['PM5.0'])
    PM50.append(linelist[i]['PM50.0'])
    time_stamp.append(linelist[i]['time_stamp'])

#print(linelist[0])
#print (PM0_3)
#print (PM0_5)
#print (PM1_0)
#print (PM2_5)
#print (PM5_0)
#print (PM50)
#print (time_stamp)

def mysubplot(yaxis, stryaxis):
    plt.plot(time_stamp, yaxis, 'b')
    plt.title(stryaxis)
    plt.ylabel('Concentration ug/0.1L')
    plt.xlabel('time_stamp')


plt.subplot(3, 2, 1)
mysubplot(PM0_3, 'PM0_3')

plt.subplot(3, 2, 2)
mysubplot(PM0_5, 'PM0_5')

plt.subplot(3, 2, 3)
mysubplot(PM1_0, 'PM1_0')

plt.subplot(3, 2, 4)
mysubplot(PM2_5, 'PM2_5')

plt.subplot(3, 2, 5)
mysubplot(PM5_0, 'PM5_0')

plt.subplot(3, 2, 6)
mysubplot(PM50, 'PM50')

plt.suptitle('Particle Concentrations at Duncan Hall(09523 W 2943 N)')
plt.savefig('Gas1.jpg')

