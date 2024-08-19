import os
import pandas as pd

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.image import imread
from matplotlib.widgets import Button

import GlobalConstants


def readCSVFile(folderPath):
    # Reading the csv file
    csvFile = [f for f in os.listdir(folderPath) if f.endswith('.csv')]
    dataFrame = [pd.read_csv(os.path.join(folderPath, file)) for file in csvFile]

    return dataFrame


def addNavigationButtons(fig, update_func):
    axprev = fig.add_axes([0.7, 0.05, 0.1, 0.075])
    axnext = fig.add_axes([0.81, 0.05, 0.1, 0.075])
    bnext = Button(axnext, 'Next')
    bprev = Button(axprev, 'Previous')

    bnext.on_clicked(lambda event: update_func(1))
    bprev.on_clicked(lambda event: update_func(-1))


def plotPoints(ax, data_frame):
    ax.clear()
    ax.plot(data_frame['sensor_x'], data_frame['sensor_y'], 'o')
    ax.set_xlim(0, GlobalConstants.MAX_GRAPH_SIZE)
    ax.set_ylim(0, GlobalConstants.MAX_GRAPH_SIZE)


def createSlideshow(data_frames):
    fig, ax = plt.subplots()
    currentFrame = [0]

    def update(frameChange):
        currentFrame[0] = (currentFrame[0] + frameChange) % len(data_frames)
        print(f"Updating to frame: {currentFrame[0]}")
        plotPoints(ax, data_frames[currentFrame[0]])
        fig.canvas.draw()

    addNavigationButtons(fig, update)
    # For the first frame
    update(0)
    plt.show()


if __name__ == '__main__':
    topLevelManipulatedAudioFolder = GlobalConstants.MANIPULATED_AUDIO_FOLDER
    dataFrames = readCSVFile(topLevelManipulatedAudioFolder + '/robin/robin1')
    createSlideshow(dataFrames)
