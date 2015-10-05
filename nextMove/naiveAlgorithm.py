import sys
import numpy as np
sys.path.insert(0, './../')
import functions as Tools;
from smartGridClass import smartGrid

def generateNextMove(game_state):
    grid = Tools.getGridState(game_state);
    sg = smartGrid(True, grid, np.zeros((4, 4), bool));
    sgUp = sg.simulateMove("up");
    sgRight = sg.simulateMove("right");
    sgLeft = sg.simulateMove("left");

    if (not Tools.staleMove(sg, sgUp) and sgUp.getHighestTile() == sgUp.intGrid[0, 0]):
        return "up";
    elif (not Tools.staleMove(sg, sgLeft) and sgLeft.getHighestTile() == sgLeft.intGrid[0, 0]):
        return "left";
    elif (not Tools.staleMove(sg, sgRight) and sgRight.getHighestTile() == sgRight.intGrid[0, 0]):
        return "right";
    elif (not Tools.staleMove(sg, sgUp)):
        return "up";
    elif (not Tools.staleMove(sg, sgLeft)):
        return "left";
    elif (not Tools.staleMove(sg, sgRight)):
        return "right";
    else:
        return "down";
