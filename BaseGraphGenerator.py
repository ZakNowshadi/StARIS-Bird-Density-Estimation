from matplotlib import pyplot as plt


def main(maxSize):
    # Making the base graph

    X = maxSize
    Y = maxSize

    # Make a graph of x by y
    # Placing a purple dot in the center to represent the sensor
    plt.plot(X / 2, Y / 2, 'mo')

    # Placing a red dot in each corner
    plt.plot(0, 0, 'mo')
    plt.plot(0, Y, 'mo')
    plt.plot(X, 0, 'mo')
    plt.plot(X, Y, 'mo')

    # Draw a green of circle around each sensor
    radius = 3.5
    circle1 = plt.Circle((0, 0), radius, color='g', fill=False)
    circle2 = plt.Circle((0, Y), radius, color='g', fill=False)
    circle3 = plt.Circle((X, 0), radius, color='g', fill=False)
    circle4 = plt.Circle((X, Y), radius, color='g', fill=False)
    circle5 = plt.Circle((X / 2, Y / 2), radius, color='g', fill=False)

    plt.gca().add_artist(circle1)
    plt.gca().add_artist(circle2)
    plt.gca().add_artist(circle3)
    plt.gca().add_artist(circle4)
    plt.gca().add_artist(circle5)
