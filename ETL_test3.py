from opto import Opto
import u3
import numpy as np
import time
#import serial.tools.list_ports as port_list

#ports = list(port_list.comports())
#for p in ports:
#    print (p)

# current_high = o.current_lower()
# print(current_high)
#
# current_low = o.current_lower()
# print(current_low)
#
# current_delta = current_high - current_low
# print(current_delta)
#c_range = np.linspace(current_range,current_steps)

dev = u3.U3()  # Open LJU3
dev.getCalibrationData()
dt = 100
dev.configIO(EnableCounter1 = True, TimerCounterPinOffset = 6)
# focal power range 2.05 - 3.86
fps = 15.3
top = 10
bottom = 0
steps = 2

n_planes = 2*(int((top - bottom)/steps) + 1)# total number of planes for each volume
volumes_per_s = fps/n_planes # total number of volume acquisition per volume
pulse_count = 0
i = 0
with Opto(port='COM6') as etl:
    counter = 0
    etl.current(bottom)
    old_pulse_count = 0  # to store the previous focal plane
    while pulse_count <= int(n_planes/2): # for initial trigger (first TTL pulse/first plane of the volume)
        if pulse_count > old_pulse_count and old_pulse_count <= int(n_planes/2):  # for initial trigger (first TTL pulse/first plane of the volume)
            focal_plane = float(bottom + ((pulse_count-1) * steps))
            #time.sleep(0.064)
            print('Focal plane', focal_plane)
            etl.current(focal_plane)
            print('ETL', etl.current())
            print('pulse', pulse_count)
            old_pulse_count += 1

        pulse_count = int(np.array(dev.getFeedback(u3.Counter(counter=1))))
    fp = focal_plane
    while n_planes >= pulse_count > int(n_planes / 2):

        if pulse_count > old_pulse_count and old_pulse_count <= n_planes:  # for initial trigger (first TTL pulse/first plane of the volume)
            # if pulse_count == n_planes-1:
            #    break
            print("SecondLoop")
            focal_plane = float(fp - ((counter) * steps))
            # time.sleep(delay)
            print('Focal plane', focal_plane)
            etl.current(focal_plane)
            print('ETL', etl.current())
            old_pulse_count += 1
            counter = counter + 1
        pulse_count = int(np.array(dev.getFeedback(u3.Counter(counter=1))))

