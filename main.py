from matplotlib import pyplot as plt

x = 10
y = 10

# Make a graph of x by y
# Placing a purple dot in the center to represent the sensor
plt.plot(x/2, y/2, 'mo')

# Placing a red dot in each corner
plt.plot(0, 0, 'mo')
plt.plot(0, y, 'mo')
plt.plot(x, 0, 'mo')
plt.plot(x, y, 'mo')

plt.show()