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

    fileName = f"{count}_{bird.getX()},{bird.getY()}.wav"
    filePath = birdFolder + '/' + fileName

    originalAudio = AudioSegment.from_file(originalAudioFolder + '/' + bird.getSpecies() + '.wav')
    distance = bird.distanceFromSensor
    # Manipulating the audio file
    # Using: https://stackoverflow.com/questions/13329617/change-the-volume-of-a-wav-file-in-python
    # Decreasing the amplitude of the sound as the distance from the sensor increases
    manipulatedWhistle = originalAudio - (distance * 15)

    manipulatedWhistle.export(filePath, format='wav')
