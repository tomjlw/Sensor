import matplotlib.pyplot as plt
import matplotlib.dates as md
import ast
import re
import numpy as np
import datetime as dt
import time
import math
from astro_geometry import *
from astro_simulator_util import *
from kmeans import *
# This is the script that to calculate error from log file not containing IQ samples

# change logs array if you want to read data from your logs
logs = ["2018_7_6_9_42_3-travel-path.log", '2018_7_6_9_52_7-travel-path.log', '2018_7_6_9_59_15-travel-path.log']
samples = [1000, 2000, 3000, 4000]
cheater_alt = 1
cheater_lat = 29.719735333
cheater_lon = -95.397867333
EARTH_RADIUS_KM = 6378.1  # Radius of the Earth in km
EARTH_RADIUS_M = 6371000  # radius of earth in m

def haversine(lat1, lon1, lat2, lon2):
   """
   Calculate the great circle distance between two points
   on the earth (specified in decimal degrees)
   """

   # convert decimal degrees to radians

   lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

   # haversine formula
   dlon = lon2 - lon1
   dlat = lat2 - lat1
   a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
   c = 2 * math.asin(math.sqrt(a))

   km = EARTH_RADIUS_KM * c
   return km * 1000


def mini(a, b):
    if a <= b:
        return a
    else:
        return b


def stddev(lst):
    """returns the standard deviation of lst"""
    variance = 0
    mn = sum(lst)/len(lst)
    for e in lst:
        variance += (e-mn)**2
    variance /= len(lst)

    if (variance == 0):
        return 1.0
    else:
        return sqrt(variance)


def readdata(file):
    # this function used to read data from the log file
    in_file = open(file, 'rt')
    contents = in_file.read()  # read the entire file into a string variable
    in_file.close()
    strs = contents

    #   Getting the strings dBm, lat, and lon values from the huge text file
    #   time_values_raw = re.findall(r"'time_stamp': '[+-]?\d+(?:\.\d+)?'", strs)
    dBm_values_raw = re.findall(r"\"dBm\": [+-]?\d+(?:\.\d+)?", strs)
    lat_values_raw = re.findall(r"\"lat\": [+-]?\d+(?:\.\d+)?", strs)
    lon_values_raw = re.findall(r"\"lon\": [+-]?\d+(?:\.\d+)?", strs)
    alt_values_raw = re.findall(r"\"alt\": [+-]?\d+(?:\.\d+)?", strs)

    #   Making the lists into giant strings
    dBm_values_raw_string = ''.join(dBm_values_raw)
    lat_values_raw_string = ''.join(lat_values_raw)
    lon_values_raw_string = ''.join(lon_values_raw)
    alt_values_raw_string = ''.join(alt_values_raw)

    #   Finding the numbers in the giant string to filter out those phrases mentioned above
    dBm = re.findall(r"[+-]?\d+(?:\.\d+)?", dBm_values_raw_string)
    lat = re.findall(r"[+-]?\d+(?:\.\d+)?", lat_values_raw_string)
    lon = re.findall(r"[+-]?\d+(?:\.\d+)?", lon_values_raw_string)
    alt = re.findall(r"[+-]?\d+(?:\.\d+)?", alt_values_raw_string)

    #   Floating all the data
    dBm_data = [float(i) for i in dBm]
    lat_data = [float(k) for k in lat]
    lon_data = [float(j) for j in lon]
    alt_data = [float(z) for z in alt]

    drone_coords_data = zip(lat_data, lon_data, alt_data, dBm_data)

    return drone_coords_data

drone1 = readdata(logs[0])
drone2 = readdata(logs[1])
drone3 = readdata(logs[2])
DataSet_MaxSize = min(len(drone1), len(drone2), len(drone3))

numIterations = 1000 # maximum number of iterations for gradient descent
numEpoch = 500 # to avoid local minimum, random initialization should be applied
threshold = 0.1
learning_rate = 0.01

BatchSize_min = 1000
BatchSize_max = DataSet_MaxSize
BatchSize_step = 1000

# numberBatch = np.int(np.floor((BatchSize_max-BatchSize_min)/BatchSize_step)+1)
numberBatch = 1
maxRun = 30

data_drone1 = np.zeros(shape=(DataSet_MaxSize,4))
data_drone2 = np.zeros(shape=(DataSet_MaxSize,4))
data_drone3 = np.zeros(shape=(DataSet_MaxSize,4))

for i in range(0, DataSet_MaxSize):
    data_drone1[i][0] = drone1[i][0]
    data_drone1[i][1] = drone1[i][1]
    data_drone1[i][2] = drone1[i][2]
    data_drone1[i][3] = drone1[i][3]

    data_drone2[i][0] = drone2[i][0]
    data_drone2[i][1] = drone2[i][1]
    data_drone2[i][2] = drone2[i][2]
    data_drone2[i][3] = drone2[i][3]

    data_drone3[i][0] = drone3[i][0]
    data_drone3[i][1] = drone3[i][1]
    data_drone3[i][2] = drone3[i][2]
    data_drone3[i][3] = drone3[i][3]

error_3drones = []


def error(data_drone1, data_drone2, data_drone3):
    for i in range(0, maxRun):
        #########3DRONEs

        # estimate RSSI model from drones 3 DRONES
        [alpha1, epsilon1] = RSSI_Loc_BatchedGD_5par(data_drone1[0:BatchSize_min], numEpoch, numIterations, threshold, learning_rate)[1]
        [alpha2, epsilon2] = RSSI_Loc_BatchedGD_5par(data_drone2[0:BatchSize_min], numEpoch, numIterations, threshold, learning_rate)[1]
        [alpha3, epsilon3] = RSSI_Loc_BatchedGD_5par(data_drone3[0:BatchSize_min], numEpoch, numIterations, threshold, learning_rate)[1]

        alpha = (alpha1+alpha2+alpha3)/3
        epsilon = (epsilon1+epsilon2+epsilon3)/3

        alpha1 = alpha
        epsilon1 = epsilon
        alpha2 = alpha
        epsilon2 = epsilon
        alpha3 = alpha
        epsilon3 = epsilon

        centers = []
        errorsBlackBox_2d = []

        [x1_org, y1_org, z1_org, zone_number, zone_letter] = GPS2UTM(data_drone1[:,0:3])
        [x2_org, y2_org, z2_org, zone_number, zone_letter] = GPS2UTM(data_drone2[:,0:3])
        [x3_org, y3_org, z3_org, zone_number, zone_letter] = GPS2UTM(data_drone3[:,0:3])

        for i_batch in range(0, numberBatch):

            data_drone1_test = data_drone1[np.int(i_batch*BatchSize_step):np.int(i_batch*BatchSize_step+BatchSize_min)]
            data_drone2_test = data_drone2[np.int(i_batch*BatchSize_step):np.int(i_batch*BatchSize_step+BatchSize_min)]
            data_drone3_test = data_drone3[np.int(i_batch*BatchSize_step):np.int(i_batch*BatchSize_step+BatchSize_min)]

            # convert GPS to UTM coordinate
            [x1, y1, z1, zone_number, zone_letter] = GPS2UTM(data_drone1_test)
            [x2, y2, z2, zone_number, zone_letter] = GPS2UTM(data_drone2_test)
            [x3, y3, z3, zone_number, zone_letter] = GPS2UTM(data_drone3_test)

            # move origin
            xx1 = x1 - x1_org[0]
            yy1 = y1 - y1_org[0]

            xx2 = x2 - x2_org[0]
            yy2 = y2 - y2_org[0]

            xx3 = x3 - x3_org[0]
            yy3 = y3 - y3_org[0]

            result = []

            for i in range(0, len(data_drone1_test)):
                result_sub = []

                r1 = 10**((data_drone1_test[i][3]-epsilon)/alpha)
                r2 = 10**((data_drone2_test[i][3]-epsilon)/alpha)
                r3 = 10**((data_drone3_test[i][3]-epsilon)/alpha)

                sol1 = IntersectPoints(complex(xx1[i], yy1[i]), complex(xx2[i], yy2[i]), r1, r2)
                sol2 = IntersectPoints(complex(xx2[i], yy2[i]), complex(xx3[i], yy3[i]), r2, r3)
                sol3 = IntersectPoints(complex(xx1[i], yy1[i]), complex(xx3[i], yy3[i]), r1, r3)

                if sol1 is True:
                    pass
                elif sol1 is False:
                    pass
                else:
                    result_sub.append((sol1[0].real, sol1[0].imag))
                    result_sub.append((sol1[1].real, sol1[1].imag))

                if sol2 is True:
                    pass
                elif sol2 is False:
                    pass
                else:
                    result_sub.append((sol2[0].real, sol2[0].imag))
                    result_sub.append((sol2[1].real, sol2[1].imag))

                if sol3 is True:
                    pass
                elif sol3 is False:
                    pass
                else:
                    result_sub.append((sol3[0].real, sol3[0].imag))
                    result_sub.append((sol3[1].real, sol3[1].imag))

                if result_sub:
                    temp = closestpair(result_sub)
                    result.append([(temp[0][0]+temp[1][0])/2, (temp[0][1]+temp[1][1])/2])

            if result:
                kmeans = KMeans(n_clusters=3)
                kmeans.fit(result)
                centers.append(kmeans.cluster_centers_)
            else:
                centers.append(centers[-1])

            result_latlonalt = np.zeros(shape = (len(centers), 3))

            x_org = (x1_org[0] + x2_org[0] + x3_org[0])/3
            y_org = (y1_org[0] + y2_org[0] + y3_org[0])/3

            for i in range(0, len(centers)):
                [result_latlonalt[i][0], result_latlonalt[i][1]]  =  utm.to_latlon(centers[i][0][0]+x_org,
                                                                                   centers[i][0][1]+y_org,
                                                                                   zone_number, zone_letter)

                errorsBlackBox_2d.append(getDistance(result_latlonalt[i][0], result_latlonalt[i][1], cheater_alt, cheater_lat,
                                                     cheater_lon, cheater_alt)[0])
            error_3drones.append(sum(errorsBlackBox_2d)/len(errorsBlackBox_2d))
            return stddev(error_3drones)
        #####END 3 DRONES


plt.figure(figsize=(10,8))

real_error_tot = []
xaxis = np.arange(len(samples))
time1 = 0
time_tot = []
for num in samples:
    start_time = time.time()
    real_error = error(data_drone1[0:num], data_drone2[0:num], data_drone3[0:num])
    end_time = time.time()
    time1 = end_time - start_time
    time_tot.append(time1) # measure the run time for algorithm
    real_error_tot.append(real_error)

# Plot the bar graph of Error
plt.subplot(1, 2, 1)
plt.bar(xaxis, real_error_tot, align='center', alpha=0.5, color = 'blue')
plt.xticks(xaxis, tuple(samples))
plt.ylabel("Localization error/m", fontsize=20)
plt.xlabel("Number of Samples", fontsize=20)
plt.title('Error for running {run} times'.format(run = maxRun))

# PLot the bar graph of Time
plt.subplot(1, 2, 2)
plt.bar(xaxis, time_tot, align='center', alpha=0.5, color = 'blue')
plt.xticks(xaxis, tuple(samples))
plt.ylabel("Time/s", fontsize=20)
plt.xlabel("Number of Samples", fontsize=20)
plt.title('Time Needed for running {run} times'.format(run = maxRun))

plt.tight_layout()
plt.savefig("Time & Error.png", dpi=600)
