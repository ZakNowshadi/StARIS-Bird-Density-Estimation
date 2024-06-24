from matplotlib import pyplot as plt


# A sensor class
class SensorZone:
    instances = []

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 3.5
        SensorZone.instances.append(self)

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
    centreSensor = SensorZone(X / 2, Y / 2)

    # Making the corner sensor objects
    upperLeftSensor = SensorZone(0, 0, )
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
