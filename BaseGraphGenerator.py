from matplotlib import pyplot as plt
from matplotlib.lines import Line2D


# A sensor class
class Sensor:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Getter for x
    def getX(self):
        return self.x

    # Getter for y
    def getY(self):
        return self.y

    # Setter for x
    def setX(self, x):
        self.x = x

    # Setter for y
    def setY(self, y):
        self.y = y


def main(maxSize):
    # Making the base graph

    X = maxSize
    Y = maxSize

    # Make a graph of x by y
    # Placing a purple dot in the center to represent the sensor
    # Making the centre sensor object
    centreSensor = Sensor(X / 2, Y / 2)
    plt.plot(centreSensor.getX(), centreSensor.getY(), 'mp', label='sensor')

    # Making the corner sensor objects
    upperLeftSensor = Sensor(0, 0)
    upperRightSensor = Sensor(0, Y)
    lowerLeftSensor = Sensor(X, 0)
    lowerRightSensor = Sensor(X, Y)

    # Placing a purple dot in the corners to represent the sensors
    plt.plot(upperLeftSensor.getX(), upperLeftSensor.getY(), 'mp')
    plt.plot(upperRightSensor.getX(), upperRightSensor.getY(), 'mp')
    plt.plot(lowerLeftSensor.getX(), lowerLeftSensor.getY(), 'mp')
    plt.plot(lowerRightSensor.getX(), lowerRightSensor.getY(), 'mp')

    # Draw a green of circle around each sensor
    radius = 3.5
    centreOfZoneDistance = radius / 2
    circle1 = plt.Circle((0, 0), radius, color='g', fill=False)
    circle2 = plt.Circle((0, Y), radius, color='g', fill=False)

    circle3 = plt.Circle((X, 0), radius, color='g', fill=False)
    circle4 = plt.Circle((X, Y), radius, color='g', fill=False)
    circle5 = plt.Circle((X / 2, Y / 2), radius, color='g', fill=False)

    plt.gca().add_artist(circle1)
    plt.gca().add_artist(circle2)
    plt.gca().add_artist(circle3)
    plt.gca().add_artist(circle4)
    plt.gca().add_artist(circle5)

    # Putting a red dot a halfway point between the centre and its radius
    plt.plot(centreOfZoneDistance, centreOfZoneDistance, 'ro', label='centre of sensor zone')
    plt.plot(centreOfZoneDistance, Y - centreOfZoneDistance, 'ro')
    plt.plot(X - centreOfZoneDistance, centreOfZoneDistance, 'ro')
    plt.plot(X - centreOfZoneDistance, Y - centreOfZoneDistance, 'ro')
