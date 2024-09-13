# Bird Density Estimating Simulation

This program has two possible strands of running:
1. With graphical rendering of the bird simulation.
   1. This comes at the disadvantage of being much slower compared to without the graphics, but it does provide a visual representation to better understand what operations are occurring.
2. Without the graphical rendering.
   1. The program can complete much quicker as a result, but the underlying operations may not be clear.

In both strands the final output of the CSVs file, which later analysis is dependent on is done the same.

Currently only works for 2 pre-defined species namely: robins and blackbirds, and it assumes an equal amount of both. Also, please note that the possible number of ticks is capped (this was for testing purposes).
This cap can be altered by changing the "limiter" found in main under BirdWalker.py.

### Set up instructions:

1. Clone the repository
2. Make a venv using `python3 -m venv venv`
3. Activate the venv using `source venv/bin/activate`
4. Install the requirements using `pip install -r requirements.txt`
5. Run the main program by running `python main.py`
6. Optional - Run the slide show maker by running `python InteractiveSlideShowMaker.py`


Possible Next Steps:

1. Fix the problem where the dots produced on the heatmap overlap and do not scale based on the number of birds.
2. Make likelihood of a bird whistling, which is dependent on the species, more true to life.
3. Look into a more efficient way of generating the visual representation, maybe instead of doing it on the fly, generate a video at the end of the backend calculations and then play that.
4. Look into adding background noise to the simulation.
5. Make the simulation into tiles which can be put together to make a larger lattice.
6. Add an option so the user can remove all print statements from the backend when it is running.

Made by Zak Nowshadi under the supervision of Prof. Simon Dobson and Dr Alison Johnston at the University of St Andrews.