import os

from matplotlib import pyplot as plt
from matplotlib.image import imread

import GlobalConstants


def loadTicks(ticksFolder):
    tickFiles = sorted([os.path.join(ticksFolder, f) for f in os.listdir(ticksFolder) if f.endswith('.png')])
    return tickFiles


class SlideShow:
    def __init__(self, ticksFolder):
        self.tickFiles = loadTicks(ticksFolder)
        self.currentTick = 0

        self.fig, self.ax = plt.subplots()
        self.image = self.ax.imshow(imread(self.tickFiles[self.index]))
        self.ax.set_title(f'Tick {self.index}')

        axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
        axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
        self.bnext = Button(axnext, 'Next')
        self.bnext.on_clicked(self.next)
        self.bprev = Button(axprev, 'Previous')
        self.bprev.on_clicked(self.prev)

    def update_image(self):
        self.image.set_data(imread(self.tickFiles[self.index]))
        self.ax.set_title(f'Tick {self.index}')
        self.fig.canvas.draw()

    def next(self, event):
        self.index = (self.index + 1) % len(self.tickFiles)
        self.update_image()

    def prev(self, event):
        self.index = (self.index - 1) % len(self.tickFiles)
        self.update_image()

    def show(self):
        plt.show()


def main():
    ticksFolder = GlobalConstants.SIMULATION_FRAME_SAVING_FOLDER
    tick_files = loadTicks(ticksFolder)
    slideshow = SlideShow(tick_files)
    slideshow.show()


if __name__ == '__main__':
    main()
