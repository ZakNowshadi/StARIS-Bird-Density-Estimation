from math import radians

from matplotlib import pyplot as plt
from rtree import index

import GlobalConstants

# Making the R-Tree index
sensorZoneIndex = index.Index()


# A sensor class
class SensorZone:
    instances = []

    def __init__(self, x, y, sizeOfGraph, radius):
        self.radius = radius
        # Ensuring the sensor is within the bounds of the mask
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


def main(ax, drawGraph):
    maskSize = GlobalConstants.MASK_MASK_SIZE
    maxSize = GlobalConstants.MAX_GRAPH_SIZE
    differenceBetweenMaxAndMask = maxSize - maskSize
    # Finding a radius to maximise the space being sensed by the 5 sensors within the mask, without there being overlap
    radius = maskSize / 5.5

    # Making the centre sensor object
    centralInternalMaskX = maskSize / 2
    centralInternalMaskY = maskSize / 2

    actualCentralX = centralInternalMaskX + differenceBetweenMaxAndMask / 2
    actualCentralY = centralInternalMaskY + differenceBetweenMaxAndMask / 2

    centreSensor = SensorZone(actualCentralX, actualCentralY, maxSize, radius)

    # Making the corner sensor objects fully within the mask
    # Each point needs to be 1 diameter away from the center of the mask and 1 radius away from the edge of the mask
    # To not overlap with the other sensors
    upperLeftSensor = SensorZone(differenceBetweenMaxAndMask + radius, differenceBetweenMaxAndMask + radius, maxSize,
                                 radius)
    upperRightSensor = SensorZone(maskSize - radius, differenceBetweenMaxAndMask + radius, maxSize, radius)
    lowerLeftSensor = SensorZone(differenceBetweenMaxAndMask + radius, maskSize - radius, maxSize, radius)
    lowerRightSensor = SensorZone(maskSize - radius, maskSize - radius, maxSize, radius)

    # Drawing a blue box around the mask
    plt.plot([differenceBetweenMaxAndMask, maskSize], [differenceBetweenMaxAndMask, differenceBetweenMaxAndMask], 'b')
    plt.plot([differenceBetweenMaxAndMask, maskSize], [maskSize, maskSize], 'b')
    plt.plot([differenceBetweenMaxAndMask, differenceBetweenMaxAndMask], [differenceBetweenMaxAndMask, maskSize], 'b')
    plt.plot([maskSize, maskSize], [differenceBetweenMaxAndMask, maskSize], 'b')

    # But ensuring the graph is drawn of maxSize size
    # Drawing the graph
    plt.xlim(0, maxSize)
    plt.ylim(0, maxSize)

    if drawGraph:
        # Drawing each sensor zone's radius
        # Draw a green of circle around each sensor

        centreSensor.drawSensorZone(ax)
        upperLeftSensor.drawSensorZone(ax)
        upperRightSensor.drawSensorZone(ax)
        lowerLeftSensor.drawSensorZone(ax)
        lowerRightSensor.drawSensorZone(ax)
