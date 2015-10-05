from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import numpy as np
from smartGridClass import smartGrid

###########################################
############ Driver Functions #############
###########################################

# use global variable driver to get gameState from localStorage
def getGameState(driver):
    storedState = driver.execute_script("return localStorage.gameState;");
    return json.loads(storedState);

# move the tiles in the specified direction
def move(gridElement, direction):
    if (direction == "up"):
        gridElement.send_keys(Keys.ARROW_UP);
        return;
    elif (direction == "right"):
        gridElement.send_keys(Keys.ARROW_RIGHT);
        return;
    elif (direction == "down"):
        gridElement.send_keys(Keys.ARROW_DOWN);
        return;
    elif (direction == "left"):
        gridElement.send_keys(Keys.ARROW_LEFT);
        return;
    else:
        assert(False);
        return;

###########################################
########## Game State Functions ###########
###########################################

# accepts game state
# returns value at specified (x, y) position
# returns 0 no tile at specified location
def getTileState(game_state, x, y):
    assert 0 <= x <= 3
    assert 0 <= y <= 3
    grid = game_state['grid'];
    grid = grid['cells']

    # switch x and y because game_state stores the transpose of the grid
    tile = grid[y][x]

    if (tile == None):
        return 0
    else:
        return tile['value'];

# given the game state, return the grid state as a 2D array
def getGridState(game_state):
    grid = game_state['grid']
    grid = grid['cells']
    grid_state = np.zeros((4, 4), dtype = np.int)
    for x in range(4):
        for y in range(4):
            grid_state[x][y] = getTileState(game_state, x, y);
    return grid_state;

# return true is reached 2048
def victory(game_state):
    return game_state['won']

###########################################
############# Grid Functions ##############
###########################################

# return the difference in tile counts between grid and nextGrid
def staleMove(sg1, sg2):
    return sg1.countTiles() - sg2.countTiles();

# have any values changed grid1 to grid2
def staleMove(sg1, sg2):
    if (np.array_equal(sg1.intGrid, sg2.intGrid)):
        return True;
    return False;
