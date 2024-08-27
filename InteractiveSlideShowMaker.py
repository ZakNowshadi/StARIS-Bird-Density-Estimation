import os
import pandas as pd
from PIL.ImageFont import truetype

from matplotlib import pyplot as plt
from matplotlib.widgets import Slider

import GlobalConstants


def readAllTicksFromCSV(tick, filePath):

    # Validation for the file path
    assert os.path.exists(filePath), f"ERROR - The file path does not exist: {filePath}"

    dataFrames = []
    with open(filePath, 'r') as file:
        for line in file:
            tick_data = line.strip().split(',')
            tickNumber = int(tick_data[0])
            sensorX = float(tick_data[1])
            sensorY = float(tick_data[2])
            dataFrames.append(pd.DataFrame({'sensor_x': [sensorX], 'sensor_y': [sensorY], 'tick': [tickNumber]}))
    return dataFrames


def plotPoints(ax, data_frame):
    ax.clear()
    ax.plot(data_frame['sensor_x'], data_frame['sensor_y'], 'o')
    ax.set_xlim(0, GlobalConstants.MAX_GRAPH_SIZE)
    ax.set_ylim(0, GlobalConstants.MAX_GRAPH_SIZE)


def createSlideshow(data_frames):
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)
    currentFrame = [0]

    def update(val):
        currentFrame[0] = int(val)
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
    dataFrames = readAllTicksFromCSV(18, topLevelManipulatedAudioFolder + '/robin/robin0/data.csv')
    createSlideshow(dataFrames)
