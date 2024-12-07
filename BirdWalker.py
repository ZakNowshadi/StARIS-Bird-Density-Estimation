import os
import shutil
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from matplotlib.animation import FuncAnimation
import AudioManipulator
import BaseGraphGenerator
import GlobalConstants

import scipy
import numpy as np

# The size of the image will be divided by this number to make it fit the graph
# Such that the image will be the same relative size no matter the size of the graph


# Making a super parent class for all the objects in the graph
class GraphObject:

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
        # Adjusting the size of the image to fit the graph such that it appears consistent no matter the size of the
        # graph
        imageSizeAdjustment = 14
        if self.image is not None and self.x is not None and self.y is not None:
            imageWidth = self.sizeOfGraph / imageSizeAdjustment
            imageHeight = self.sizeOfGraph / imageSizeAdjustment
            extent = [self.x - imageWidth / 2, self.x + imageWidth / 2,
                      self.y - imageHeight / 2, self.y + imageHeight / 2]
            if self.artist:
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
        homeImageFilePath = GlobalConstants.HOME_IMAGE_FILE
        super().__init__(sizeofGraph, homeImageFilePath)
        self.setRandomCoords()


# Making the target class
class Target(GraphObject):
    def __init__(self, sizeofGraph):
        targetImageFilePath = GlobalConstants.TARGET_IMAGE_FILE
        super().__init__(sizeofGraph, targetImageFilePath)
        self.setRandomCoords()


class CircleManager:
    def __init__(self):
        self.circles = []

    def drawCircle(self, ax, x, y, radius, colour, fill=False):
        circle = plt.Circle((x, y), radius, color=colour, fill=fill)
        ax.add_artist(circle)
        plt.draw()
        # Pausing to allow the user to see the circle
        plt.pause(1)
        # Adding the circle to the list of circles to be removed
        self.circles.append(circle)
        plt.draw()

    def removeAllCircles(self):
        for circle in self.circles:
            circle.remove()
        self.circles.clear()
        plt.draw()

    def removeSpecificCircle(self, circle):
        circle.remove()
        self.circles.remove(circle)
        plt.draw()


# Making a bird class
class Bird(GraphObject):

    def __init__(self, name, imagePath, species, speed, sizeofGraph):
        super().__init__(sizeofGraph, imagePath)
        self.image = mpimg.imread(imagePath)
        self.name = name
        self.species = species
        # Will be null if in no sensor zone
        # Needs to be know so know which sensor to play the sound to as under the
        # current implementation only one sensor should hear a bird at a time due to the lack of overlaps between the
        # sensor zones
        self.currentSensorZone = None
        self.distanceFromSensor = 0
        self.speed = speed
        # Making the initial target object
        self.targetObject = Target(sizeofGraph)
        self.homeObject = Home(sizeofGraph)
        self.currentlyInFlight = None
        self.setRandomCoords()
        self.currentlyWhistling = None
        self.timeAwayFromHome = 0
        self.lineToHome = None
        self.lineToTarget = None
        # Making a circle manager object to manage the circles made when the bird is in a sensor zone and whistles
        self.circleManager = CircleManager()

    # Getter for species and name
    def getSpecies(self):
        return self.species

    def getName(self):
        return self.name

    # Function to allow the clear showing of when a bird is inside a sensor zone and makes a detectable whistle
    def drawTemporaryCircle(self, ax):
        radius = self.sizeOfGraph / 20
        colour = 'purple'
        self.circleManager.drawCircle(ax, self.x, self.y, radius, colour)

    def removeCircle(self):
        # Removing the circle if it is there
        if self.circleManager.circles:
            self.circleManager.removeSpecificCircle(self.circleManager.circles[0])

    def checkIfWhistling(self):
        # TODO: Implement a more sophisticated logic for when a bird should whistle based species by species
        if self.species == 'robin':
            if random.random() < 0.5:
                self.currentlyWhistling = True
        if self.species == 'blackbird':
            if random.random() < 0.7:
                self.currentlyWhistling = True

    def sensorZoneCheck(self, drawGraph):
        # Checking if the bird is in a sensor zone
        birdPoint = (self.x, self.y, self.x, self.y)
        # Getting the index of the sensor zone that the bird is in
        possibleZones = list(BaseGraphGenerator.sensorZoneIndex.intersection(birdPoint))

        for zoneID in possibleZones:
            sensorZone = BaseGraphGenerator.SensorZone.instances[zoneID]
            distance = self.ifPointIsInsideSensorZoneReturnTheDistanceToTheSensorFromThePoint(self.x, self.y,
                                                                                              sensorZone)
            # If the distance is not -1, the bird is actually inside a true circular sensor zone
            # But also need to check the bird is inside the mask
            # And also that the bird is currently whistling
            self.checkIfWhistling()
            if (distance != -1 and self.currentlyWhistling):
                
                # implementing the formula in the 2009 Dawson, D.K. & Efford study
                
                # use of arbitrary beta values, a potential improvement to be looked into
                beta0 = 80
                if distance <= 1:
                    mu = beta0
                else:
                    beta1 = 0.1
                    mu = beta0 - 10 * np.log10(distance ** 2) + beta1 * (distance - 1)

                normalDistributionAt0 = scipy.stats.norm(0)
                receivedSignalStrength = mu + normalDistribution.rsv(size = 1)
                # arbitrary choices of c and sigma
                c = 20
                sigma = 0.1
                gamma = c - mu / sigma

                delta = 0
                if mu > c:
                    delta = 1
                
                normalDistributionAtGamma = scipy.stats.norm(gamma)
                probabilityOfDetection = normalDistributionAtGamma(size = 1) ** (1 - delta)

                # arbitrary to see if the probability is sufficient: to be improved upon
                if probabilityOfDetection > 0.5:

                    self.currentSensorZone = sensorZone
                    self.distanceFromSensor = distance

                    # Drawing a temporary circle to show the user that the bird made a detectable whistle in a sensor zone
                    if drawGraph:
                        self.drawTemporaryCircle(plt.gca())

                    print("\033[92m" + self.name + " made a detectable whistle" + "\033[0m")
                    print("Sensor zone coords: ", sensorZone.getX(), sensorZone.getY())
                    print("Distance from sensor: ", distance)
                    return True

        # If the bird is not in any sensor zone
        self.currentSensorZone = None
        self.distanceFromSensor = 0
        # Removing the circle if it is there
        if drawGraph:
            self.removeCircle()

        # Printing that the bird is not in a sensor zone in a red text
        print("\033[91m" + self.name + " did NOT make a detectable whistle" + "\033[0m")
        return False

    # Returns a positive number (the distance) if the point is within the sensor zone
    # or -1 if it is not
    def ifPointIsInsideSensorZoneReturnTheDistanceToTheSensorFromThePoint(self, x, y, sensorZone):
        distance = distanceBetweenTwoPoints(x, y, sensorZone.getX(), sensorZone.getY())
        if distance <= sensorZone.radius:
            return distance
        return -1

    def removeAllCircles(self):
        self.circleManager.removeAllCircles()

    def updatePosition(self, sizeofGraph):
        self.removeAllCircles()

        # Finding the distance the bird is from home
        distanceFromHome = distanceBetweenTwoPoints(self.x, self.y, self.homeObject.getX(), self.homeObject.getY())

        # Existing logic to calculate distanceFromHome
        self.timeAwayFromHome += 1  # Increment time away from home

        # Adjusting probabilityOfGoingHome to factor in timeAwayFromHome
        # The longer the bird is away from home, the more likely it is to go home
        timeFactor = min(1, self.timeAwayFromHome / 100)

        # Making the probability of going home a function of the distance and time from home
        # The further the bird is from home, the more likely it is to go home
        probabilityOfGoingHome = min(1, (distanceFromHome / (self.sizeOfGraph * 0.5)) + timeFactor) / 2

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
            # # The location of the home is also changed when the target is reached
            # self.homeObject.setRandomCoords()

        # Check is in the vicinity of its home
        if abs(self.x - self.homeObject.getX()) < 1 and abs(self.y - self.homeObject.getY()) < 1:
            self.timeAwayFromHome = 0


global frameCount
frameCount = 0

global tickCount
tickCount = 0


def distanceBetweenTwoPoints(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def update(frame, birds, ax, sizeofGraph, drawGraph):
    # Incrementing the coords of the bird
    global frameCount, tickCount

    frameSavingFolder = GlobalConstants.SIMULATION_FRAME_SAVING_FOLDER
    # Working out the new positions of the birds
    for bird in birds:
        bird.updatePosition(sizeofGraph)
        # Printing current coords of the bird
        print("\n-----------------------")
        print(bird.getName() + " is at: ", bird.getX(), bird.getY())
        print(bird.getName() + " has spent " + str(bird.timeAwayFromHome) + " ticks away from home")

        if bird.sensorZoneCheck(drawGraph):
            # Passing the bird to the AudioManipulator
            # Where the frame acts as the count
            AudioManipulator.saveManipulatedAudioFile(bird, frameCount)
        tickCount += 1

    frameCount += 1
    # Drawing the graph
    if drawGraph:
        # Drawing each bird such that they all render to move at the same time
        for bird in birds:
            # Removing the existing lines
            if bird.lineToHome:
                bird.lineToHome.remove()
            if bird.lineToTarget:
                bird.lineToTarget.remove()

            # Re-draw the target each time the bird moves
            bird.targetObject.draw(ax)
            # Likewise for the home
            bird.homeObject.draw(ax)

            # Drawing a line from the bird to the home
            # Draw a green line from bird to home and store the reference
            bird.lineToHome, = ax.plot([bird.getX(), bird.homeObject.getX()], [bird.getY(), bird.homeObject.getY()],
                                       'g-')
            # Draw a red line from bird to target and store the reference
            bird.lineToTarget, = ax.plot([bird.getX(), bird.targetObject.getX()],
                                         [bird.getY(), bird.targetObject.getY()], 'r-')
            bird.draw(ax)

        framePath = os.path.join(frameSavingFolder, f'frame_{frameCount}.png')
        plt.savefig(framePath)

        plt.draw()
    # If not in a sensor zone, the bird will not make a sound

    # The comma at the end is to unpack the tuple, so it can be passed as expected into caller
    return bird.artist,


def main(drawGraph):
    sizeofGraph = GlobalConstants.MAX_GRAPH_SIZE
    if drawGraph:
        # Making the frame by frame folder if it does not exist and then wiping it clean
        frameSavingFolder = GlobalConstants.SIMULATION_FRAME_SAVING_FOLDER
        if os.path.exists(frameSavingFolder):
            # If it does, delete it
            shutil.rmtree(frameSavingFolder)
        # Making a new frame by frame folder
        os.makedirs(frameSavingFolder)

    # Making a new bird object
    speedOfBird = 0.5
    # Making the list of species by looking into the Images/Species folder and getting the names of the files
    # excluding the .png
    speciesFolder = GlobalConstants.SPECIES_IMAGES_FOLDER
    # Checking the species folder exists and is populated
    assert os.path.exists(speciesFolder), 'The ' + speciesFolder + ' folder does not exist or is empty'
    originalAudioFilesFolder = GlobalConstants.ORIGINAL_AUDIO_FOLDER
    assert os.path.exists(originalAudioFilesFolder), 'The ' + originalAudioFilesFolder + ('folder does not exist or is '
                                                                                          'empty')
    speciesList = [species.split('.')[0] for species in os.listdir(speciesFolder)]
    numberOfBirdsPerSpecies = 2
    birds = []

    # Making sure the number of files is the same in both the OriginalAudioFiles and the Species folder
    numberOfFilesInOriginalAudioFiles = len(os.listdir(originalAudioFilesFolder))
    numberOfFilesInSpeciesFolder = len(os.listdir(speciesFolder))
    assert numberOfFilesInOriginalAudioFiles == numberOfFilesInSpeciesFolder, 'The number of files in the ' + originalAudioFilesFolder + ' folder and the ' + speciesFolder + ' are not the same.'

    for species in speciesList:
        birdImageFilePath = speciesFolder + '/' + species + '.png'
        birds += [Bird(species + str(i), birdImageFilePath, species, speedOfBird, sizeofGraph) for i in
                  range(numberOfBirdsPerSpecies)]

    # Drawing the static background only once if needed otherwise just setting up the sensor zone
    # Setting up the plot
    fig, ax = plt.subplots()
    # Making the base graph
    BaseGraphGenerator.main(ax, drawGraph)

    # Running the program not using any matplotlib graphics
    # Scaling cap to ensure the program does not run for too long
    limiter = 100
    if not drawGraph:
        for i in range(sizeofGraph * limiter):
            update(i, birds, None, sizeofGraph, drawGraph)

    if drawGraph:

        ax.set_xlim(0, sizeofGraph)
        ax.set_ylim(0, sizeofGraph)

        # Drawing the bird(s)
        for bird in birds:
            bird.draw(ax)

        plt.draw()
        # Short pause to allow for the new bird to be accurately drawn
        plt.pause(0.01)
        # Running the animation - ensuring that the garbage collector does not delete the animation object
        birdAnimation = FuncAnimation(fig, update, fargs=(birds, ax, sizeofGraph, drawGraph),
                                      frames=range(sizeofGraph * limiter),
                                      blit=True, interval=50)

        plt.show()
