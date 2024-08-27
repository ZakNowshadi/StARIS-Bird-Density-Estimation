import os
import pandas as pd

from matplotlib import pyplot as plt
from matplotlib.widgets import Slider

import GlobalConstants


def readCSVFile(folderPath):
    # Reading the csv file
    csvFile = [f for f in os.listdir(folderPath) if f.endswith('.csv')]
    dataFrame = [pd.read_csv(os.path.join(folderPath, file)) for file in csvFile]

    return dataFrame


def plotPoints(ax, data_frame):
    ax.clear()
    ax.plot(data_frame['sensor_x'], data_frame['sensor_y'], 'o')
    ax.set_xlim(0, GlobalConstants.MAX_GRAPH_SIZE)
    ax.set_ylim(0, GlobalConstants.MAX_GRAPH_SIZE)


def createSlideshow(data_frames):
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)
    currentFrame = [0]

    def update(frameChange):
        currentFrame[0] = (currentFrame[0] + frameChange) % len(data_frames)
        print(f"Updating to frame: {currentFrame[0]}")
        plotPoints(ax, data_frames[currentFrame[0]])
        fig.canvas.draw()

    # Making the slider
    axSlider = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    slider = Slider(axSlider, 'Frame', 0, len(data_frames) - 1, valinit=0, valstep=1)
    slider.on_changed(update)

    # For the first frame
    update(0)
    plt.show()


if __name__ == '__main__':
    topLevelManipulatedAudioFolder = GlobalConstants.MANIPULATED_AUDIO_FOLDER
    dataFrames = readCSVFile(topLevelManipulatedAudioFolder + '/robin/robin1')
    createSlideshow(dataFrames)
