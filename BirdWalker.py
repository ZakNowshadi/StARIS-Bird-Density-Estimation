from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from matplotlib.animation import FuncAnimation
import AudioManipulator
import BaseGraphGenerator


# Making the bird walk from the bottom left corner to the top right corner

# Making a bird class
class Bird:
    def __init__(self, x, y, imagePath, speed):
        self.x = x
        self.y = y
        self.image = mpimg.imread(imagePath)
        # Will be null if in no sensor zone
        # Needs to be know so know which sensor to play the sound to as
        # Under current implementation only one sensor should hear a bird at a time
        self.currentSensorZone = None
        self.distanceFromSensor = 0
        self.speed = speed
        # The artist object for the bird
        self.artist = None

    # Getter for x
    def getX(self):
        return self.x

    # Getter for y
    def getY(self):
        return self.y

    def draw(self, ax):
        extent = [self.x, self.x + 1, self.y, self.y + 1]
        # To fix the problem of the original bird freezing while another moves
        if self.artist is not None:
            self.artist.remove()
        self.artist = ax.imshow(self.image, extent=extent)

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
                print("Bird is in a sensor zone")
                print("Sensor zone coords: ", sensorZone.getX(), sensorZone.getY())
                print("Distance from sensor: ", distance)
                return True
        # If the bird is not in a sensor zone
        self.currentSensorZone = None
        self.distanceFromSensor = 0
        print("Bird is NOT in a sensor zone")
        return False

    def updatePosition(self, x, y, sizeofGraph):
        self.x = (x + self.speed) % sizeofGraph
        self.y = (y + self.speed) % sizeofGraph


def update(frame, bird, ax, sizeofGraph):
    # Incrementing the coords of the bird
    bird.updatePosition(bird.getX(), bird.getY(), sizeofGraph)
    # Printing current coords of the bird
    print("\n-----------------------")
    print("Bird is at: ", bird.getX(), bird.getY())

    bird.draw(ax)
    if bird.sensorZoneCheck():
        # Passing the bird to the AudioManipulator
        # Where the frame acts as the count
        AudioManipulator.main(bird, frame)

    # The comma at the end is to unpack the tuple, so it can be passed as expected into caller
    return bird.artist,


def main(sizeofGraph):
    # Setting up the plot
    fig, ax = plt.subplots()
    ax.set_xlim(0, sizeofGraph)
    ax.set_ylim(0, sizeofGraph)

    # The bird walker will start in the bottom left corner
    # Making a new bird object
    speedOfBird = 0.5
    bird1 = Bird(0, 0, 'Images/robin.png', speedOfBird)
    # Drawing the static background only once
    BaseGraphGenerator.main(sizeofGraph)

    bird1.draw(ax)

    plt.draw()
    plt.pause(0.01)
    # Running the animation - ensuring that the garbage collector does not delete the animation object
    ani = FuncAnimation(fig, update, fargs=(bird1, ax, sizeofGraph), frames=range(sizeofGraph), blit=True)

    plt.show()
