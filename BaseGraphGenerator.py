from matplotlib import pyplot as plt
from rtree import index

# Making the R-Tree index
sensorZoneIndex = index.Index()


# A sensor class
class SensorZone:
    instances = []

    def __init__(self, x, y, sizeOfGraph):
        self.x = x
        self.y = y
        self.radius = sizeOfGraph / 3
        SensorZone.instances.append(self)
        # Adding the sensor into the R-Tree
        sensorZoneIndex.insert(len(SensorZone.instances) - 1,
                               (self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius))

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

    def drawSensorZone(self):
        # Plotting the sensor itself
        plt.plot(self.x, self.y, 'mp')
        # Draw a green of circle around each sensor
        circle = plt.Circle((self.x, self.y), self.radius, color='g', fill=False)
        plt.gca().add_artist(circle)

    # Returns all the currently existing sensor objects
    @classmethod
    def getInstances(cls):
        return cls.instances


def main(maxSize):
    # Making the base graph

    X = maxSize
    Y = maxSize

    # Make a graph of x by y
    # Placing a purple dot in the center to represent the sensor
    # Making the centre sensor object
    centreSensor = SensorZone(X / 2, Y / 2, maxSize)

    # Making the corner sensor objects
    upperLeftSensor = SensorZone(0, 0, maxSize)
    upperRightSensor = SensorZone(0, Y, maxSize)
    lowerLeftSensor = SensorZone(X, 0, maxSize)
    lowerRightSensor = SensorZone(X, Y, maxSize)

    # Drawing each sensor zone's radius
    # Draw a green of circle around each sensor
    centreSensor.drawSensorZone()
    upperLeftSensor.drawSensorZone()
    upperRightSensor.drawSensorZone()
    lowerLeftSensor.drawSensorZone()
    lowerRightSensor.drawSensorZone()
