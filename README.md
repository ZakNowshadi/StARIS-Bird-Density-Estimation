# Bird Density Estimating Simulation

This program has two possible strands of running:
1. With graphical rendering of the bird simulation.
   1. This comes at the disadvantage of being much slower compared to without the graphics, but it does provide a visual representation to better understand what operations are occurring.
2. Without the graphical rendering.
   1. The program can complete much quicker as a result, but the underlying operations may not be clear.

In both strands the final output of the CSVs file, which later analysis is dependent on is done the same.

### Set up instructions:

1. Clone the repository
2. Make a venv using `python3 -m venv venv`
3. Activate the venv using `source venv/bin/activate`
4. Install the requirements using `pip install -r requirements.txt`
5. Run the main program by running `python main.py`
6. Optional - Run the slide show maker by running `python InteractiveSlideShowMaker.py`