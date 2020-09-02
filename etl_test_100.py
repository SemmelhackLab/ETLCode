from opto import Opto
import numpy as np
import time
from opto import Opto
import u3
import numpy as np
import serial.tools.list_ports as port_list
import matplotlib.pyplot as plt

ports = list(port_list.comports())
for p in ports:
    print (p)

dev = u3.U3()  # Open LJU3
dev.getCalibrationData()
dt = 100
dev.configIO(EnableCounter1 = True, TimerCounterPinOffset = 6)

fps = 15.3
top = 10
bottom = 0
steps = 5

n_planes = 2 * (int((top - bottom)/steps) +1) # total number of planes for each volume
volumes_per_s = fps/n_planes # total number of volume acquisition per volume
pulse_count = 0
delay = 0.075
listdata=[]
listtime=[]
freq = 15.0
bottom = 0
top = 5
step = 5
with Opto(port='COM6') as o:
    o.current(0)
    old = 0
    while True:
        pulse_count = int(np.array(dev.getFeedback(u3.Counter(counter=1))))
        if pulse_count > old:
            for i in np.linspace(0, 2*np.pi, 1000):
                o.current(bottom + (np.sin(i*0.25) * step))
            old+=1
            o.current(0)
