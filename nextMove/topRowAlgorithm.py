import sys
import numpy as np
sys.path.insert(0, './../')
import functions as Tools;
from smartGridClass import smartGrid

# count merges in top row
def countMergesInRowX(x, sg):
    count = 0;
    for y in range(4):
        if (sg.mergedGrid[x][y]):
            count = count + 1;
    return count;

# assume not stale
def compareFutures(sg1, sg2):
    score1 = 0;
    score2 = 0;

    # metric 1: highest score
    if (sg1.getHighestTile() > sg2.getHighestTile()):
        score1 = score1 + 20;
    elif (sg2.getHighestTile() < sg1.getHighestTile()):
        score2 = score2 + 20;

    # metric 2: number of tileso
    if (sg1.countTiles() > sg2.countTiles()):
        score1 = score1 + 2;
    elif (sg2.countTiles() < sg1.countTiles()):
        score2 = score2 + 2;

    # metric 3: number of merges in top row
    if (countMergesInRowX(0, sg1) > countMergesInRowX(0, sg2)):
        score1 = score1 + 40;
    elif (countMergesInRowX(0, sg1) < countMergesInRowX(0, sg2)):
        score2 = score2 + 40;

    # metric 3.33: number of merges in second row
    if (countMergesInRowX(1, sg1) > countMergesInRowX(1, sg2)):
        score1 = score1 - 20;
    elif (countMergesInRowX(1, sg1) < countMergesInRowX(1, sg2)):
        score2 = score2 - 20;

    # metric 3.66: number of merges in third row
    if (countMergesInRowX(2, sg1) > countMergesInRowX(2, sg2)):
        score1 = score1 - 30;
    elif (countMergesInRowX(2, sg1) < countMergesInRowX(2, sg2)):
        score2 = score2 - 30;

    # metric 4: [0, 0] contains highest value
    if (sg1.getHighestTile() == sg1.intGrid[0, 0]):
        score1 = score1 + 40;
    elif (sg2.getHighestTile() == sg2.intGrid[0, 0]):
        score2 = score1 + 40;

    return [score1, score2];

def generateNextMove(game_state):
    grid = Tools.getGridState(game_state);
    sg = smartGrid(True, grid, np.zeros((4, 4), bool));
    sgUp = sg.simulateMove("up");
    sgRight = sg.simulateMove("right");
    sgLeft = sg.simulateMove("left");

    # no moves possible
    if (Tools.staleMove(sg, sgUp) and Tools.staleMove(sg, sgRight) and Tools.staleMove(sg, sgLeft)):
        return "down";
    # one move possible
    elif (Tools.staleMove(sg, sgUp) and Tools.staleMove(sg, sgRight)):
        return "left";
    # one move possible
    elif (Tools.staleMove(sg, sgUp) and Tools.staleMove(sg, sgLeft)):
        return "right";
    # one move possible
    elif (Tools.staleMove(sg, sgRight) and Tools.staleMove(sg, sgLeft)):
        return "up";
    # right and left moves possible
    elif (Tools.staleMove(sg, sgUp)):
        scoresRL = compareFutures(sgRight, sgLeft);
        if (scoresRL[0] > scoresRL[1]):
            return "right";
        # on tie, choose left
        else:
            return "left";
    # right and up moves possible
    elif (Tools.staleMove(sg, sgLeft)):
        scoresRU = compareFutures(sgRight, sgUp);
        if (scoresRU[0] > scoresRU[1]):
            return "right";
        # on tie, choose up
        else:
            return "up";
    # left and up moves possible
    elif (Tools.staleMove(sg, sgRight)):
        scoresLU = compareFutures(sgLeft, sgUp);
        if (scoresLU[0] > scoresLU[1]):
            return "left";
        # on tie, choose up
        else:
            return "up";
    # all three moves possible
    else:
        scoresUL = compareFutures(sgUp, sgLeft);
        # up is better than left
        if (scoresUL[0] > scoresUL[1]):
            #compare up and right
            scoresUR = compareFutures(sgUp, sgRight);
            # up is best
            if (scoresUR[0] > scoresUR[1]):
                return "up";
            # right is best
            else:
                return "right";
        # left is better than up
        else:
            # compare left and right
            scoresLR = compareFutures(sgLeft, sgRight);
            # left is best
            if (scoresLR[0] > scoresLR[1]):
                return "left";
            # right is best
            else:
                return "right";
