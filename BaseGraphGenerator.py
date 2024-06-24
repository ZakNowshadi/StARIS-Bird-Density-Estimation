from matplotlib import pyplot as plt


# A sensor class
class SensorZone:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 3.5
        halfRadius = self.radius / 2
        self.northWestDot = (x - halfRadius, y + halfRadius)
        self.northEastDot = (x + halfRadius, y + halfRadius)
        self.southWestDot = (x - halfRadius, y - halfRadius)
        self.southEastDot = (x + halfRadius, y - halfRadius)

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

        # Drawing the dots that represent the corners of the sensor zone
        plt.plot(self.northWestDot[0], self.northWestDot[1], 'ro')
        plt.plot(self.northEastDot[0], self.northEastDot[1], 'ro')
        plt.plot(self.southWestDot[0], self.southWestDot[1], 'ro')
        plt.plot(self.southEastDot[0], self.southEastDot[1], 'ro')


def main(maxSize):
    # Making the base graph

    X = maxSize
    Y = maxSize

    # Make a graph of x by y
    # Placing a purple dot in the center to represent the sensor
    # Making the centre sensor object
    centreSensor = SensorZone(X / 2, Y / 2)

    # Making the corner sensor objects
    upperLeftSensor = SensorZone(0, 0,)
    upperRightSensor = SensorZone(0, Y)
    lowerLeftSensor = SensorZone(X, 0)
    lowerRightSensor = SensorZone(X, Y)

    # Drawing each sensor zone's radius
    # Draw a green of circle around each sensor
    centreSensor.drawSensorZone()
    upperLeftSensor.drawSensorZone()
    upperRightSensor.drawSensorZone()
    lowerLeftSensor.drawSensorZone()
    lowerRightSensor.drawSensorZone()
