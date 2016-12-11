# Robot-Localisation-using-HMM

The file hmm-data.txt contains a map of a 10-by-10 2D grid-world. The row and column indices start
from 0 (the most left-bottom cell has a coordinate of (0, 0)). The free cells are represented as '1's and
the obstacles are represented as '0's. There are four towers, one in each of the four corners, as indicated
in the data file. Your task is to use a Hidden Markov Model to figure out the most likely trajectory of a
robot in this grid-world. Assume that the initial position of the robot has a uniform prior over all free
cells. In each time-step, the robot moves to one of its neighboring free cells chosen uniformly at
random. At a given cell, the robot measures L2 distances (Euclidean distances) to each of the towers.
For a true distance d, the robot records a noisy measurement chosen uniformly at random from the set
of numbers in the interval [0.7d, 1.3d] with one decimal place. These measurements for 11 time-steps
are also provided in the data file. You should output the coordinates of the most likely trajectory of the
robot for 11 time-steps.
