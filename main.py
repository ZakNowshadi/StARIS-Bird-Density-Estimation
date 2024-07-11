# Running the base graph generator and then putting the bird walker on top of it
import BirdWalker
import shutil
import os

# Defining the size of the graph
maxSize = 20

manipulatedAudioFolder = 'ManipulatedAudioFiles'
# Checking if the manipulated audio files folder exists
if os.path.exists(manipulatedAudioFolder):
    # If it does, delete it
    shutil.rmtree(manipulatedAudioFolder)
# Making a new manipulated audio files folder
os.makedirs(manipulatedAudioFolder)

BirdWalker.main(maxSize)
