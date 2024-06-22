from matplotlib import pyplot as plt

import BaseGraphGenerator


# Making the bird walk from the bottom left corner to the top right corner

def main(sizeofGraph):
    plt.ion()

    # The bird walker will start in the bottom left corner
    x = 0
    y = 0

    # The bird walker will move to the top right corner
    while x < sizeofGraph and y < sizeofGraph:
        plt.plot(x, y, 'bo')
        BaseGraphGenerator.main(sizeofGraph)
        plt.draw()
        plt.pause(0.3)  # short pause
        plt.close('all')
        x += 1
        y += 1
