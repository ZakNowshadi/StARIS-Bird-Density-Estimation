# Running the base graph generator and then putting the bird walker on top of it
import BirdWalker
import shutil
import os
import globalConstants

# Defining the size of the graph
maxSize = 20

# Checking if the manipulated audio files folder exists
if os.path.exists(globalConstants.MANIPULATED_AUDIO_FOLDER):
    # If it does, delete it
    shutil.rmtree(globalConstants.MANIPULATED_AUDIO_FOLDER)
# Making a new manipulated audio files folder
os.makedirs(globalConstants.MANIPULATED_AUDIO_FOLDER)

BirdWalker.main(maxSize)
