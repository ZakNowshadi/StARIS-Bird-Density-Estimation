from matplotlib import pyplot as plt

import BaseGraphGenerator


# Making the bird walk from the bottom left corner to the top right corner

def main(sizeofGraph):
    # The bird walker will start in the bottom left corner
    x = 0
    y = 0

    # The bird walker will move to the top right corner
    while x < sizeofGraph and y < sizeofGraph:
        plt.plot(x, y, 'bo')
        # Making the base graph
        BaseGraphGenerator.main(sizeofGraph)
        plt.show()
        plt.close()
        x += 1
        y += 1


