# Running the base graph generator and then putting the birdwalker on top of it
import BaseGraphGenerator
import BirdWalker

# Defining the size of the graph
sizeofGraph = 10
BaseGraphGenerator.main(sizeofGraph)

BirdWalker.main()

