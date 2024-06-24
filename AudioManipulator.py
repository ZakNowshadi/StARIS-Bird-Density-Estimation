from shutil import copyfile
import os


def main(bird):
    distance = bird.distanceFromSensor

    # Making a temporary copy of the original audio file
    originalAudioFolder = 'OriginalAudioFiles'
    manipulatedAudioFolder = 'ManipulatedAudioFiles'
    copyfile(originalAudioFolder + '/single_robin_tweeting.wav', manipulatedAudioFolder + '/tempAudio.wav')

    # Manipulating the audio file
    # Decreasing the amplitude of the sound as the distance from the sensor increases

    # Deleting the entire contents of the manipulated audio tracks folder
    for file in os.listdir(manipulatedAudioFolder):
        os.remove(manipulatedAudioFolder + '/' + file)
