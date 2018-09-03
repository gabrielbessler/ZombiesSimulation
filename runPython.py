import matplotlib.pyplot as plt
import numpy as np


#------------------ Loading Data ------------------
x = []
y = []

with open('C:\\Users\\Gabe\\Desktop\\Programming\\data.txt') as file:
    count = 0
    for line in file:
        if count == 0:
            x = line
        else:
            y = line
        count += 1

#-----------------Calculate Regression Using Numpy --------------------
x = eval(x)
y = eval(y)
time = list(range(0, len(x)))
p1 = np.polyfit(time, y, deg=3)
fit_fn = np.poly1d(p1)
p2 = np.polyfit(time, x, deg=3)
fit_fn2 = np.poly1d(p2)

#-------------------Plot Using PyPlot ----------------------------------
plt.plot(time, y, 'r', label="Regular Fish")
plt.plot(time, x, 'b', label="Zombie Fish")
plt.plot(time, fit_fn(time), '--k', label="Linear Regression")
plt.plot(time, fit_fn2(time), '--k', label="Linear Regression")
plt.xlabel('Time')
plt.ylabel('Number of Fish')
plt.title("Population of Fish Over Time")
plt.legend(framealpha=0.3, loc=2)
plt.show()
