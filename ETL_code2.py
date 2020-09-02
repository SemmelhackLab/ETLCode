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

fps = 15.3
top = 5
bottom = 0
steps = 1

n_planes = int((top - bottom)/steps) + 1 # total number of planes for each volume
total_n_planes = n_planes * 3
volumes_per_s = fps/n_planes # total number of volume acquisition per volume
pulse_count = 0
fp = 0

with Opto(port='COM6') as etl:
    while True:
        etl.current(bottom)
        pulse_count = int(np.array(dev.getFeedback(u3.Counter(counter=1))))
        #print('Reset',pulse_count)
        if pulse_count > 0: # for initial trigger (first TTL pulse/first plane of the volume)
            print('ETL', etl.current())
            print('ini', pulse_count)
            old_pulse_count = 0 # to store the previous focal plane
            while pulse_count < total_n_planes:
                pulse_count = int(np.array(dev.getFeedback(u3.Counter(counter=1))))
                fp += 1
                if pulse_count > old_pulse_count:  # for initial trigger (first TTL pulse/first plane of the volume)
                    focal_plane = float(bottom + (fp * steps))
                    etl.current(focal_plane)
                    old_pulse_count += 1
                    if fp % 5:
                        fp = 0
