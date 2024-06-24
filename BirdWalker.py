from matplotlib import pyplot as plt
import matplotlib.image as mpimg

import AudioManipulator
import BaseGraphGenerator


# Making the bird walk from the bottom left corner to the top right corner

# Making a bird class
class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = mpimg.imread('Images/robin.png')
        # Will be null if in no sensor zone
        # Needs to be know so know which sensor to play the sound to as
        # Under current implementation only one sensor should hear a bird at a time
        self.currentSensorZone = None
        self.distanceFromSensor = 0

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

    def draw(self):
        plt.imshow(self.image, extent=[self.x, self.x + 1, self.y, self.y + 1])

    def sensorZoneCheck(self):
        # Checking if the bird is in a sensor zone
        # For each of thew sensor zone objects

        # Finding the distance from each sensor
        for sensorZone in BaseGraphGenerator.SensorZone.getInstances():
            # Using the distance formula
            distance = ((self.x - sensorZone.getX()) ** 2 + (self.y - sensorZone.getY()) ** 2) ** 0.5
            # If the distance is less than the radius of the sensor zone
            if distance <= sensorZone.radius:
                # If the bird is in a sensor zone
                self.currentSensorZone = sensorZone
                self.distanceFromSensor = distance
                return True
        # If the bird is not in a sensor zone
        self.currentSensorZone = None
        self.distanceFromSensor = 0
        return False


def main(sizeofGraph):
    plt.ion()

    # The bird walker will start in the bottom left corner
    # Making a new bird object
    bird1 = Bird(0, 0)

    # The bird walker will move to the top right corner
    while bird1.getX() <= sizeofGraph and bird1.getY() <= sizeofGraph:
        # Drawing the bird
        bird1.draw()
        BaseGraphGenerator.main(sizeofGraph)
        plt.tight_layout()
        plt.draw()
        plt.pause(0.5)  # short pause
        plt.close('all')
        # Printing the current coords of the sensor zone it is in
        print("Bird is at: ", bird1.getX(), bird1.getY())
        # Checking if the bird is in a sensor zone
        print("\n--------------------")
        if bird1.sensorZoneCheck():
            print("Bird is in a sensor zone")
            print("Distance from sensor: ", bird1.distanceFromSensor)
            print("Sensor zone coords: ", bird1.currentSensorZone.getX(), bird1.currentSensorZone.getY())
        else:
            print("Bird is NOT in a sensor zone")

        # Passing the bird to the AudioManipulator
        AudioManipulator.main(bird1)

        # Incrementing the coords of the bird
        bird1.setX(bird1.getX() + 1)
        bird1.setY(bird1.getY() + 1)
