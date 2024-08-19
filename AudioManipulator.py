import os
from pydub import AudioSegment
import GlobalConstants


def saveManipulatedAudioFile(bird, count):
    # Base folder
    manipulatedAudioFolder = GlobalConstants.MANIPULATED_AUDIO_FOLDER
    originalAudioFolder = GlobalConstants.ORIGINAL_AUDIO_FOLDER
    speciesFolder = manipulatedAudioFolder + '/' + bird.getSpecies()
    # Checking if the species folder exists
    if not os.path.exists(speciesFolder):
        # If it does not, make it
        os.makedirs(speciesFolder)
    birdFolder = speciesFolder + '/' + bird.getName()
    # Checking if the bird folder exists
    if not os.path.exists(birdFolder):
        # If it does not, make it
        os.makedirs(birdFolder)

    fileName = f"{count}_{bird.currentSensorZone.getX()},{bird.currentSensorZone.getY()}.wav"
    filePath = birdFolder + '/' + fileName

    originalAudio = AudioSegment.from_file(originalAudioFolder + '/' + bird.getSpecies() + '.wav')
    distance = bird.distanceFromSensor
    # TODO: Possibly explore white noise, e.g. trees could muffle different frequencies

    # Manipulating the audio file
    # Using: https://stackoverflow.com/questions/13329617/change-the-volume-of-a-wav-file-in-python
    # Decreasing the amplitude of the sound as the distance from the sensor increases
    manipulatedWhistle = originalAudio - (distance * 15)
    manipulatedWhistle.export(filePath, format='wav')
    # Appending the tick number, sensor x and y to the csv file
    appendSpecificBirdTickToCSV(bird, count)


def appendSpecificBirdTickToCSV(bird, count):
    # Base folder
    manipulatedAudioFolder = GlobalConstants.MANIPULATED_AUDIO_FOLDER
    speciesFolder = manipulatedAudioFolder + '/' + bird.getSpecies()
    birdFolder = speciesFolder + '/' + bird.getName()

    fileName = birdFolder + '/' + f"{bird.getName()}_data.csv"
    # Checking if the csv file exists
    if not os.path.exists(fileName):
        # If it does not, make it
        with open(fileName, 'a') as file:
            file.write("tick_number,sensor_x,sensor_y\n")

    # Writing to the CSV file using the audio file name as the source, the tick number, and the sensor x and y
    # Writing the tick number and sensor x and y
    with open(fileName, 'a') as file:
        file.write(f"{count},{bird.currentSensorZone.getX()},{bird.currentSensorZone.getY()}\n")
