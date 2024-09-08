import os
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider
import GlobalConstants


def readAllTicksFromCSV(filePath):
    # Validation for the file path
    assert os.path.exists(filePath), f"ERROR - The file path does not exist: {filePath}"

    dataFrames = []
    with open(filePath, 'r') as file:
        # Getting the name of the bird from the file path
        birdName = filePath.split(os.sep)[-2]
        # Skipping the header
        next(file)
        for line in file:
            tickData = line.strip().split(',')
            frameNumber = int(tickData[0])
            sensorX = float(tickData[1])
            sensorY = float(tickData[2])
            dataFrames.append(pd.DataFrame(
                {'sensor_x': [sensorX], 'sensor_y': [sensorY], 'frame': [frameNumber], 'name': [birdName]}))
    return dataFrames


def readAllTicksFromMultipleCSVs(filePaths):
    allDataFrames = []
    for filePath in filePaths:
        allDataFrames.extend(readAllTicksFromCSV(filePath))
    return allDataFrames


# Iterating over the data frame to plot the relevant points of the sensors that make the detections
def plotPoints(ax, dataFrames, currentFrame):
    ax.clear()
    for df in dataFrames:
        dataFrameFrameData = df[df['frame'] == currentFrame]
        if not dataFrameFrameData.empty:
            ax.plot(dataFrameFrameData['sensor_x'], dataFrameFrameData['sensor_y'], 'o',
                    label=dataFrameFrameData['name'].iloc[0])
    ax.set_xlim(0, GlobalConstants.MAX_GRAPH_SIZE)
    ax.set_ylim(0, GlobalConstants.MAX_GRAPH_SIZE)
    ax.legend()


def createSlideshow(dataFrames):
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)
    currentFrame = [0]

    def update(val):
        currentFrame[0] = int(val)
        print(f"Updating to frame: {currentFrame[0]}")
        plotPoints(ax, dataFrames, [currentFrame[0]])
        fig.canvas.draw()

    # Making the slider
    maxFrameNumber = max([df['frame'].max() for df in dataFrames])
    axSlider = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    slider = Slider(axSlider, 'Frame', 0, maxFrameNumber, valinit=0, valstep=1)
    slider.on_changed(update)

    # For the first frame
    update(0)
    plt.show()


if __name__ == '__main__':
    topLevelManipulatedAudioFolder = GlobalConstants.MANIPULATED_AUDIO_FOLDER
    filePaths = []
    # Finding all CSVs in the manipulated audio folder
    for root, dirs, files in os.walk(topLevelManipulatedAudioFolder):
        for file in files:
            if file.endswith('.csv'):
                filePaths.append(os.path.join(root, file))

    dataFrames = readAllTicksFromMultipleCSVs(filePaths)
    createSlideshow(dataFrames)
