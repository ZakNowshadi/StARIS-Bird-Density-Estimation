from matplotlib import pyplot as plt

import BaseGraphGenerator


# Making the bird walk from the bottom left corner to the top right corner

# Making a bird class
class Bird:
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

    def checkWhichSensor(self):
        # Check if the bird is in the sensor zone
        # If the bird is in the sensor zone, then the sensor will be activated
        # If the sensor is activated, then the bird will be scared
        # If the bird is scared, then the bird will move away from the sensor
        # If the bird is not in the sensor zone, then the bird will move normally
        pass


def main(sizeofGraph):
    plt.ion()

    # The bird walker will start in the bottom left corner
    # Making a new bird object
    bird1 = Bird(0, 0)

    # The bird walker will move to the top right corner
    while bird1.getX() < sizeofGraph and bird1.getY() < sizeofGraph:
        plt.plot(bird1.getX(), bird1.getY(), 'bo', label='bird')
        BaseGraphGenerator.main(sizeofGraph)
        # Adding a legand to the graph on the left side:
        #   - Purple is the sensors
        #   - Red is the centre of the sensor zone
        #  - Blue is the bird walker
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
        plt.tight_layout()
        plt.draw()
        plt.pause(0.5)  # short pause
        plt.close('all')
        # Incrementing the coords of the bird
        bird1.setX(bird1.getX() + 1)
        bird1.setY(bird1.getY() + 1)
