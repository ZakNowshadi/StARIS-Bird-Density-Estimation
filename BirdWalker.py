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
        plt.plot(x, y, 'bo', label='bird')
        BaseGraphGenerator.main(sizeofGraph)
        # Adding a legand to the graph on the left side:
        #   - Purple is the sensors
        #   - Red is the centre of the sensor zone
        #  - Blue is the bird walker
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
        plt.tight_layout()
        plt.draw()
        plt.pause(0.5)  # short pause
        plt.close('all')
        x += 1
        y += 1
