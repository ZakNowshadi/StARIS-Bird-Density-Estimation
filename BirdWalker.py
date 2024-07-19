from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from matplotlib.animation import FuncAnimation
import AudioManipulator
import BaseGraphGenerator
import random

# The size of the image will be divided by this number to make it fit the graph
# Such that the image will be the same relative size no matter the size of the graph
global imageSizeAdjustment
imageSizeAdjustment = 14


# Making a super parent class for all the objects in the graph
class GraphObject:
    global imageSizeAdjustment

    def __init__(self, sizeofGraph, imagePath=None):
        self.sizeOfGraph = sizeofGraph
        self.x, self.y = None, None
        self.imagePath = imagePath
        self.image = mpimg.imread(imagePath) if imagePath else None
        self.artist = None

    def setRandomCoords(self):
        slightReduction = self.sizeOfGraph * 0.1
        self.remove()
        self.x, self.y = random.uniform(0, self.sizeOfGraph - slightReduction), random.uniform(0,
                                                                                               self.sizeOfGraph
                                                                                               - slightReduction)

    def draw(self, ax):
        if self.image is not None and self.x is not None and self.y is not None:
            extent = [self.x, self.x + self.sizeOfGraph / imageSizeAdjustment, self.y,
                      self.y + self.sizeOfGraph / imageSizeAdjustment]
            if self.artist is not None:
                self.artist.remove()
            self.artist = ax.imshow(self.image, extent=extent)

    # Removing the object
    def remove(self):
        if self.artist is not None:
            self.artist.remove()
            self.artist = None

    # Getters for x and y
    def getX(self):
        return self.x

    def getY(self):
        return self.y


# Home class for the bird walker
class Home(GraphObject):
    def __init__(self, sizeofGraph):
        homeImageFilePath = 'Images/GraphItems/bird_nest.png'
        super().__init__(sizeofGraph, homeImageFilePath)
        self.setRandomCoords()


# Making the target class
class Target(GraphObject):
    def __init__(self, sizeofGraph):
        targetImageFilePath = 'Images/GraphItems/red_target.png'
        super().__init__(sizeofGraph, targetImageFilePath)
        self.setRandomCoords()


# Making a bird class
class Bird(GraphObject):
    def __init__(self, name, imagePath, species, speed, sizeofGraph):
        super().__init__(sizeofGraph, imagePath)
        self.image = mpimg.imread(imagePath)
        self.name = name
        self.species = species
        # Will be null if in no sensor zone
        # Needs to be know so know which sensor to play the sound to as
        # Under current implementation only one sensor should hear a bird at a time
        self.currentSensorZone = None
        self.distanceFromSensor = 0
        self.speed = speed
        # Making the initial target object
        self.targetObject = Target(sizeofGraph)
        self.homeObject = Home(sizeofGraph)
        # TODO: Implement the currentlyInFlight mechanic such that audio is only recorded when the bird is in flight
        #  or not depending on the species
        self.currentlyInFlight = False
        self.setRandomCoords()

    # Getter for species and name
    def getSpecies(self):
        return self.species

    def getName(self):
        return self.name

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
                # Printing that the bird is in a sensor zone in green text
                print("\033[92m" + self.name + " is in a sensor zone" + "\033[0m")
                print("Sensor zone coords: ", sensorZone.getX(), sensorZone.getY())
                print("Distance from sensor: ", distance)
                return True

        # If the bird is not in any sensor zone
        self.currentSensorZone = None
        self.distanceFromSensor = 0
        # Printing that the bird is not in a sensor zone in a red text
        print("\033[91m" + self.name + " is not in a sensor zone" + "\033[0m")
        return False

    # Returns a positive number (the distance) if the point is within the sensor zone
    # or -1 if it is not
    def ifPointIsInsideSensorZoneReturnTheDistanceToTheSensorFromThePoint(self, x, y, sensorZone):
        distance = distanceBetweenTwoPoints(x, y, sensorZone.getX(), sensorZone.getY())
        if distance <= sensorZone.radius:
            return distance
        return -1

    def updatePosition(self, sizeofGraph):
        # Finding the distance the bird is from home
        distanceFromHome = distanceBetweenTwoPoints(self.x, self.y, self.homeObject.getX(), self.homeObject.getY())

        # Making the probability of going home a function of the distance from home
        # The further the bird is from home, the more likely it is to go home
        probabilityOfGoingHome = min(1, distanceFromHome / (self.sizeOfGraph * 0.5 * 2))

        # Moving towards home with a probability that increases as the bird gets further from home
        if random.random() < probabilityOfGoingHome:
            self.moveTowardsPoint(self.homeObject.getX(), self.homeObject.getY())
        else:
            self.moveTowardsPoint(self.targetObject.getX(), self.targetObject.getY())

        # Wrapping around the graph
        self.x %= sizeofGraph
        self.y %= sizeofGraph

    def moveTowardsPoint(self, targetX, targetY):
        randomLowerBound = 0.5
        randomUpperBound = 1
        # if the bird is to the left of the target, move right
        if self.x < targetX:
            self.x += self.speed * random.uniform(randomLowerBound, randomUpperBound)
        elif self.x > targetX:
            self.x -= self.speed * random.uniform(randomLowerBound, randomUpperBound)

        # if the bird is below the target, move up
        if self.y < targetY:
            self.y += self.speed * random.uniform(randomLowerBound, randomUpperBound)
        elif self.y > targetY:
            self.y -= self.speed * random.uniform(randomLowerBound, randomUpperBound)

        # Check if near the target point to generate a new target
        # If the bird is within 1 unit of the target, generate a new target
        if abs(self.x - self.targetObject.getX()) < 1 and abs(self.y - self.targetObject.getY()) < 1:
            self.targetObject.setRandomCoords()
            self.targetObject.artist = None
            self.targetObject.draw(plt.gca())
            # The location of the home is also changed when the target is reached
            self.homeObject.setRandomCoords()


global count
count = 0


def distanceBetweenTwoPoints(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def update(frame, birds, ax, sizeofGraph):
    # Incrementing the coords of the bird
    global count

    for bird in birds:
        bird.updatePosition(sizeofGraph)
        # Printing current coords of the bird
        print("\n-----------------------")
        print(bird.getName() + " is at: ", bird.getX(), bird.getY())
        # Re-draw the target each time the bird moves
        bird.targetObject.draw(ax)
        # Re-draw the home each time the bird moves
        bird.homeObject.draw(ax)
        bird.draw(ax)
        if bird.sensorZoneCheck():
            # Passing the bird to the AudioManipulator
            # Where the frame acts as the count
            AudioManipulator.saveManipulatedAudioFile(bird, count)

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
    speciesList = ['robin', 'blackbird']
    numberOfBirdsPerSpecies = 1
    birds = []

    for species in speciesList:
        birdImageFilePath = 'Images/Species/' + species + '.png'
        birds += [Bird(species + str(i), birdImageFilePath, species, speedOfBird, sizeofGraph) for i in
                  range(numberOfBirdsPerSpecies)]

    # Drawing the static background only once
    BaseGraphGenerator.main(sizeofGraph)

    # Drawing the bird(s)
    for bird in birds:
        bird.draw(ax)

    plt.draw()
    # Short pause to allow for the new bird to be accurately drawn
    plt.pause(0.01)
    # Running the animation - ensuring that the garbage collector does not delete the animation object
    birdAnimation = FuncAnimation(fig, update, fargs=(birds, ax, sizeofGraph), frames=range(sizeofGraph * 20),
                                  blit=True, interval=50)

    plt.show()
