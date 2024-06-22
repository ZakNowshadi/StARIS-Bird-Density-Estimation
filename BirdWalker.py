from matplotlib import pyplot as plt


# Making the bird walk from the bottom left corner to the top right corner

def main():
    # The bird walker will start at the bottom left corner
    birdX = 0
    birdY = 0

    # The bird walker will move to the top right corner
    while birdX < X and birdY < Y:
        birdX += 1
        birdY += 1
        plt.plot(birdX, birdY, 'bo')
        plt.pause(0.1)
    # The bird walker will stop when it reaches the top right corner
    plt.show()
