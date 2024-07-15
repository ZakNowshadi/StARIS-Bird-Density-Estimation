from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from matplotlib.animation import FuncAnimation
import AudioManipulator
import BaseGraphGenerator
import random
from random import randint

# The size of the image will be divided by this number to make it fit the graph
# Such that the image will be the same relative size no matter the size of the graph
global imageSizeAdjustment
imageSizeAdjustment = 14


# Making the target class
class Target:
    def __init__(self, sizeofGraph):
        self.x, self.y = randint(0, sizeofGraph), randint(0, sizeofGraph)
        self.image = mpimg.imread('Images/red_target.png')
        self.sizeOfGraph = sizeofGraph
        self.artist = None

    # Getter for x
    def getX(self):
        return self.x

    # Getter for y
    def getY(self):
        return self.y

    def setNewTargetCoords(self):
        # Variable to slightly reduce the scope of the possible target coords such that
        # The target is never on the edge of the graph
        # This is to prevent the target from being partially off the graph
        slightReduction = self.sizeOfGraph * 0.1

        self.removeTarget()
        self.x, self.y = random.uniform(0, self.sizeOfGraph - slightReduction), random.uniform(0,
                                                                                               self.sizeOfGraph
                                                                                               - slightReduction)
        print("New target coords: ", self.x, self.y)

    def drawTarget(self, ax):
        # Drawing the target as a function of the size of the graph
        extent = [self.x, self.x + self.sizeOfGraph / imageSizeAdjustment, self.y,
                  self.y + self.sizeOfGraph / imageSizeAdjustment]
        # To fix the problem of the original bird freezing while another moves
        if self.artist is not None:
            self.removeTarget()
        self.artist = ax.imshow(self.image, extent=extent)

    def removeTarget(self):
        if self.artist is not None:
            self.artist.remove()
            self.artist = None


# Making a bird class
class Bird:
    def __init__(self, x, y, imagePath, species, speed, sizeofGraph):
        self.x = x
        self.y = y

        self.image = mpimg.imread(imagePath)
        self.species = species
        # Will be null if in no sensor zone
        # Needs to be know so know which sensor to play the sound to as
        # Under current implementation only one sensor should hear a bird at a time
        self.currentSensorZone = None
        self.distanceFromSensor = 0
        self.speed = speed
        # The artist object for the bird
        self.artist = None
        # Making the initial target object
        self.targetObject = Target(sizeofGraph)
        self.sizeOfGraph = sizeofGraph

    # Getter for x
    def getX(self):
        return self.x

    # Getter for y
    def getY(self):
        return self.y

    # Getter for species
    def getSpecies(self):
        return self.species

    def draw(self, ax):
        # Drawing the bird as a function of the size of the graph
        extent = [self.x, self.x + self.sizeOfGraph / imageSizeAdjustment, self.y,
                  self.y + self.sizeOfGraph / imageSizeAdjustment]
        # To fix the problem of the original bird freezing while another moves
        if self.artist is not None:
            self.artist.remove()
        self.artist = ax.imshow(self.image, extent=extent)

    def sensorZoneCheck(self):
        # Checking if the bird is in a sensor zone

        birdPoint = (self.x, self.y, self.x, self.y)
        # Getting the index of the sensor zone that the bird is in
        possibleZones = list(BaseGraphGenerator.sensorZoneIndex.intersection(birdPoint))

        for zoneID in possibleZones:
            sensorZone = BaseGraphGenerator.SensorZone.instances[zoneID]
            distance = self.ifPointIsInsideSensorZoneReturnTheDistanceToTheSensorFromThePoint(self.x, self.y,
                                                                                              sensorZone)
            # If the distance is not -1, the bird is in a sensor zone
            if distance != -1:
                self.currentSensorZone = sensorZone
                self.distanceFromSensor = distance
                print("Bird is in a sensor zone")
                print("Sensor zone coords: ", sensorZone.getX(), sensorZone.getY())
                print("Distance from sensor: ", distance)
                return True

        self.currentSensorZone = None
        self.distanceFromSensor = 0
        # Printing that the bird is not in a sensor zone in a red highlight
        print("\033[91mBird is not in a sensor zone\033[0m")
        return False

    # Returns a positive number (the distance) if the point is within the sensor zone
    # or -1 if it is not
    def ifPointIsInsideSensorZoneReturnTheDistanceToTheSensorFromThePoint(self, x, y, sensorZone):
        distance = ((x - sensorZone.getX()) ** 2 + (y - sensorZone.getY()) ** 2) ** 0.5
        if distance <= sensorZone.radius:
            return distance
        return -1

    def updatePosition(self, sizeofGraph):
        randomLowerBound = 0.5
        randomUpperBound = 1
        # if the bird is to the left of the target, move right
        if self.x < self.targetObject.getX():
            self.x += self.speed * random.uniform(randomLowerBound, randomUpperBound)
        elif self.x > self.targetObject.getX():
            self.x -= self.speed * random.uniform(randomLowerBound, randomUpperBound)

        # if the bird is below the target, move up
        if self.y < self.targetObject.getY():
            self.y += self.speed * random.uniform(randomLowerBound, randomUpperBound)
        elif self.y > self.targetObject.getY():
            self.y -= self.speed * random.uniform(randomLowerBound, randomUpperBound)

        # Wrap around logic remains unchanged
        self.x %= sizeofGraph
        self.y %= sizeofGraph

        # Check if near the target point to generate a new target
        # If the bird is within 1 unit of the target, generate a new target
        if abs(self.x - self.targetObject.getX()) < 1 and abs(self.y - self.targetObject.getY()) < 1:
            self.targetObject.setNewTargetCoords()
            self.targetObject.artist = None
            self.targetObject.drawTarget(plt.gca())


global count
count = 0


def update(frame, bird, ax, sizeofGraph):
    # Incrementing the coords of the bird
    global count

    bird.updatePosition(sizeofGraph)
    # Printing current coords of the bird
    print("\n-----------------------")
    print("Bird is at: ", bird.getX(), bird.getY())
    # Re-draw the target each time the bird moves
    bird.targetObject.drawTarget(ax)
    bird.draw(ax)
    if bird.sensorZoneCheck():
        # Passing the bird to the AudioManipulator
        # Where the frame acts as the count
        AudioManipulator.main(bird, count)
    plt.draw()
    # If not in a sensor zone, the bird will not make a sound
    # Incrementing the count
    count += 1
    # The comma at the end is to unpack the tuple, so it can be passed as expected into caller
    return bird.artist,


def main(sizeofGraph):
    # Setting up the plot
    fig, ax = plt.subplots()
    ax.set_xlim(0, sizeofGraph)
    ax.set_ylim(0, sizeofGraph)

    # The bird walker will start in the bottom left corner for initial test purposes
    # Making a new bird object
    speedOfBird = 0.5
    species = 'robin'
    # Starting the bird at random coords between 0 and the size of the graph
    startingX, startingY = randint(0, sizeofGraph), randint(0, sizeofGraph)

    bird1 = Bird(startingX, startingY, 'Images/robin.png', species, speedOfBird, sizeofGraph)

    # Drawing the static background only once
    BaseGraphGenerator.main(sizeofGraph)

    # Drawing the bird
    bird1.draw(ax)

    plt.draw()
    # Short pause to allow for the new bird to be accurately drawn
    plt.pause(0.01)
    # Running the animation - ensuring that the garbage collector does not delete the animation object
    birdAnimation = FuncAnimation(fig, update, fargs=(bird1, ax, sizeofGraph), frames=range(sizeofGraph * 20),
                                  blit=True, interval=50)

    plt.show()
