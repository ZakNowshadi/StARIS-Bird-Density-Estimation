# Running the base graph generator and then putting the bird walker on top of it
import BirdWalker
import shutil
import os
import GlobalConstants

# Checking if the manipulated audio files folder exists
if os.path.exists(GlobalConstants.MANIPULATED_AUDIO_FOLDER):
    # If it does, delete it
    shutil.rmtree(GlobalConstants.MANIPULATED_AUDIO_FOLDER)
# Making a new manipulated audio files folder
os.makedirs(GlobalConstants.MANIPULATED_AUDIO_FOLDER)

# Asking the user if they would like to have the graph drawn to represent what is happening Such that if the user
# does not want any visuals, the underlying mechanics of the program would continue as normal, just without
# generating anything other than maybe print statements for the user to see But the program wil run much faster
# without having to generate the graphics, thus more likely be useful at scale when we have many birds of possibly
# many different species

# TODO: Maybe add an option for the user to say if they want the print statements or not to
#  give them the option to further speed up the program

while True:
    drawGraph = input("Would you like to draw the graph? (y/n): ")
    if drawGraph == 'y' or drawGraph == 'Y':
        drawGraph = True
        break
    elif drawGraph == 'n' or drawGraph == 'N':
        drawGraph = False
        break
    else:
        print("Invalid input - please try again")

BirdWalker.main(drawGraph)


