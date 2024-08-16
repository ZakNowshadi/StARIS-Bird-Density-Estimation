from matplotlib import pyplot as plt
from rtree import index

# Making the R-Tree index
sensorZoneIndex = index.Index()


# A sensor class
class SensorZone:
    instances = []

    def __init__(self, x, y, sizeOfGraph, radius):
        self.radius = radius
        self.x = max(self.radius, min(x, sizeOfGraph - self.radius))
        self.y = max(self.radius, min(y, sizeOfGraph - self.radius))
        SensorZone.instances.append(self)
        # Adding the sensor into the R-Tree
        # Making a bounding box around the sensor
        # With the distance from the sensor to the edge of the box being the radius of the sensor
        # In effect the true sensor zone circle is contained within the box being created here
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

    def drawSensorZone(self, ax):
        # Plotting the sensor itself
        plt.plot(self.x, self.y, 'mp')
        # Draw a green of circle around each sensor
        circle = plt.Circle((self.x, self.y), self.radius, color='g', fill=False)
        ax.add_artist(circle)


def isPointInSideTheMask(x, y, maskSize, maxSize):
    differenceBetweenMaxAndMask = maxSize - maskSize
    # Checking if the point is within the mask
    return differenceBetweenMaxAndMask < x < maskSize and differenceBetweenMaxAndMask < y < maskSize


def main(maskSize, maxSize, ax, drawGraph):
    differenceBetweenMaxAndMask = maxSize - maskSize
    radius = maskSize / 5.5


# Make a graph of x by y
    # Placing a purple dot in the center to represent the sensor
    # Making the centre sensor object
    centreSensor = SensorZone(maxSize / 2, maxSize / 2, maskSize, radius)

    # Making the corner sensor objects fully within the mask
    upperLeftSensor = SensorZone(differenceBetweenMaxAndMask + radius, differenceBetweenMaxAndMask + radius, maskSize, radius)
    upperRightSensor = SensorZone(maskSize - radius, differenceBetweenMaxAndMask + radius, maskSize, radius)
    lowerLeftSensor = SensorZone(differenceBetweenMaxAndMask + radius, maskSize - radius, maskSize, radius)
    lowerRightSensor = SensorZone(maskSize - radius, maskSize - radius, maskSize, radius)

    # Drawing a blue box around the mask
    plt.plot([differenceBetweenMaxAndMask, maskSize], [differenceBetweenMaxAndMask, differenceBetweenMaxAndMask], 'b')
    plt.plot([differenceBetweenMaxAndMask, maskSize], [maskSize, maskSize], 'b')
    plt.plot([differenceBetweenMaxAndMask, differenceBetweenMaxAndMask], [differenceBetweenMaxAndMask, maskSize], 'b')
    plt.plot([maskSize, maskSize], [differenceBetweenMaxAndMask, maskSize], 'b')

    # But ensuring the graph is drawn of maxSize size
    # Drawing the graph
    plt.xlim(0, maxSize)

    if drawGraph:
        # Drawing each sensor zone's radius
        # Draw a green of circle around each sensor

        centreSensor.drawSensorZone(ax)
        upperLeftSensor.drawSensorZone(ax)
        upperRightSensor.drawSensorZone(ax)
        lowerLeftSensor.drawSensorZone(ax)
        lowerRightSensor.drawSensorZone(ax)