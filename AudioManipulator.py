from pydub import AudioSegment

global count
count = 0


def main(bird):
    # TODO: Store every audio tick
    global count
    distance = bird.distanceFromSensor

    originalAudioFolder = 'OriginalAudioFiles'
    manipulatedAudioFolder = 'ManipulatedAudioFiles'

    originalWhistle = AudioSegment.from_file(originalAudioFolder + '/single_robin_tweeting.wav')

    # Manipulating the audio file
    # Using: https://stackoverflow.com/questions/13329617/change-the-volume-of-a-wav-file-in-python
    # Decreasing the amplitude of the sound as the distance from the sensor increases
    manipulatedWhistle = originalWhistle - (distance * 15)

    # Saving the manipulated audio file as a new file with a number at the end increasing with each new file
    # The coords of the bird and its species are also included in the file name
    filename = f"{bird.getSpecies()}{count}_{bird.getX()},{bird.getY()}.wav"
    filePath = manipulatedAudioFolder + '/' + filename
    manipulatedWhistle.export(filePath, format='wav')


    count += 1
