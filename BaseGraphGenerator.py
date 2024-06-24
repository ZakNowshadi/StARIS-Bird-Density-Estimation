from matplotlib import pyplot as plt
from matplotlib.lines import Line2D


# A sensor class
class SensorZone:
    def __init__(self, x, y, isCentralSensor):
        self.x = x
        self.y = y
        self.radius = 3.5
        self.isCentralSensor = isCentralSensor
        self.centreOfZoneX = None
        self.centreOfZoneY = None
        if isCentralSensor:
            # Set the centre dot to the centre of plot
            self.centreOfZoneX = x
            self.centreOfZoneY = y
        else:
            # Set the centre dot to the halfway point between centre and its radius, for the corner sensors only
            # The dot should sit on a line between the centre sensor and the corner sensor
            self.centreOfZoneX = (x + (x / 2)) / 2
            self.centreOfZoneY = (y + (y / 2)) / 2

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

    def checkIfCentralSensor(self):
        return self.isCentralSensor

    def drawSensorZone(self):
        # Plotting the sensor itself
        plt.plot(self.x, self.y, 'mp', label='sensor')
        # Draw a green of circle around each sensor
        circle = plt.Circle((self.x, self.y), self.radius, color='g', fill=False)
        plt.gca().add_artist(circle)

        # Putting a red dot a halfway point between the centre and its radius
        plt.plot(self.centreOfZoneX, self.centreOfZoneY, 'ro', label='centre of sensor zone')


def main(maxSize):
    # Making the base graph

    X = maxSize
    Y = maxSize

    # Make a graph of x by y
    # Placing a purple dot in the center to represent the sensor
    # Making the centre sensor object
    centreSensor = SensorZone(X / 2, Y / 2, True)
    plt.plot(centreSensor.getX(), centreSensor.getY(), 'mp', label='sensor')

    # Making the corner sensor objects
    upperLeftSensor = SensorZone(0, 0, False)
    upperRightSensor = SensorZone(0, Y, False)
    lowerLeftSensor = SensorZone(X, 0, False)
    lowerRightSensor = SensorZone(X, Y, False)


    # Drawing each sensor zone's radius
    # Draw a green of circle around each sensor
    centreSensor.drawSensorZone()
    upperLeftSensor.drawSensorZone()
    upperRightSensor.drawSensorZone()
    lowerLeftSensor.drawSensorZone()
    lowerRightSensor.drawSensorZone()
