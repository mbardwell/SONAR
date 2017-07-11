#http://playground.arduino.cc/interfacing/python
import matplotlib.pyplot as plt
import numpy as np
import Adafruit_BBIO.PWM as PWM

#PWM.start(channel, duty, freq=2000, polarity=0)
#duty values are valid 0 (off) to 100 (on)
PWM.start("P9_14", 50, 2000, 0) #P9_14 is EHRPWM1A, P9_16 is EHRPWM1B
#PWM.set_duty_cycle("P9_14", 25.5)
#PWM.set_frequency("P9_14", 10)

PWM.stop("P9_14")
PWM.cleanup()

#set polarity to 1 on start:
PWM.start("P9_14", 50, 2000, 1)