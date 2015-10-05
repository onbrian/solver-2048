# 2048Solver

This program uses Selenium WebDriver API to interact with the 2048 puzzle online -- not only to simulate arrow keys to actually play the game, but also to access online local storage the 2048 puzzle uses to store the game state after each move. This allows the algorithm to know the state of each tile after each move to best decide where to go next. 

The brain of the program is the directory "nextMove", which contains various algorithms to analyze the current board state and determine where to go next. "simulator2048" is the body of the program, which starts up the browser to the 2048 puzzle and reads the game state, specifies and calls one of the algorithms in "nextMove", and implements the move decided by the algorithm.   