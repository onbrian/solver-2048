import sys
import numpy as np
import Queue
sys.path.insert(0, './../')
import functions as Tools;
from smartGridClass import smartGrid

def evaluate(sg):
    score = 0;
    values = [];
    for x in range(4):
        for y in range(4):
            values.append(sg.intGrid[x][y]);

    values.sort(reverse=True);

    if (values[0] == sg.intGrid[0][0]):
        score = score + 20000;
    if (values[1] == sg.intGrid[0][1]):
        score = score + 3000;
    if (values[2] == sg.intGrid[0][2]):
        score = score + 2000;
    if (values[3] == sg.intGrid[0][3]):
        score = score + 1000;

    index = 0

    # 0 to 3
    yRange1 = range(4);
    # 3 to 0
    yRange2 = range(3, -1, -1);

    for x in xrange(0, 2):
        # default to ascending order
        yRange = yRange1;
        # x isn't even
        if (x % 2 != 0):
            yRange = yRange2;
        for y in(yRange):
            if (values[index] == sg.intGrid[x][y]):
                bump = 200;
                if (x == 0):
                    bump = 1000;
                score = score + bump;
            index = index + 1

    for x in xrange(2, 4):
        for y in range(4):
            if (sg.intGrid[x][y] > 0):
                score = score - 30 * (4 - x);

    secondRow = []

    for y in range(4):
        if (sg.mergedGrid[0][y] == True):
            score = score + 1000 * (4 - y);

    for y in range(4):
        secondRow.append(sg.intGrid[1][y]);

    secondRow.sort(reverse = True);
    if (secondRow[0] == sg.intGrid[1][0] or secondRow[0] == sg.intGrid[1][3]):
        score = score + 500;


    return score

def nextThreeGrids(sg):
    sgUp = sg.simulateMove("up");
    sgRight = sg.simulateMove("right");
    sgLeft = sg.simulateMove("left");

    possibleFuture = [sgUp, sgRight, sgLeft];
    future = [];
    for sgFuture in (possibleFuture):
        if (Tools.staleMove(sg, sgFuture)):
            future.append(False);
        else:
            future.append(sgFuture);
    return future;

def prune(sg):
    if (sg == False):
        return False;
    if (sg.getHighestTile() != sg.intGrid[0][0]):
        return False
    if (nextThreeGrids(sg) == [False, False, False]):
        return False;
    return sg;

def countFuture(steps):
    i = 0;
    gridCount = 0;
    while (i < steps):
        gridCount = gridCount + pow(3, (i + 1));
        i = i + 1;
    return gridCount;

def generateNextMoves(game_state):
    grid = Tools.getGridState(game_state);
    sg = smartGrid(True, grid, None);

    gridCollection = [];

    stepsAhead = 5;

    i = 0;
    gridQueue = Queue.Queue();
    future = nextThreeGrids(sg);
    gridQueue.put([future[0], ["up"]]);
    gridQueue.put([prune(future[1]), ["right"]]);
    gridQueue.put([future[2], ["left"]]);

    while (i < countFuture(stepsAhead) and not gridQueue.empty()):
        #print i
        #print len(gridCollection)
        newSgPair = gridQueue.get();
        i = i + 1
        if (newSgPair[0] == False):
            continue;
        gridCollection.append(newSgPair);

        upMoveList = newSgPair[1][:];
        rightMoveList = newSgPair[1][:];
        leftMoveList = newSgPair[1][:];
        upMoveList.append('up');
        rightMoveList.append('right');
        leftMoveList.append('left');

        future = nextThreeGrids(newSgPair[0]);

        gridQueue.put([prune(future[0]), upMoveList]);
        gridQueue.put([prune(future[1]), rightMoveList]);
        gridQueue.put([prune(future[2]), leftMoveList]);

    if (len(gridCollection) == 0):
        return ["down"];

    bestIndex = 0;
    bestScore = -1;
    i = 0;
    for sgPair in (gridCollection):
        currScore = evaluate(sgPair[0]);
        if (currScore > bestScore):
            bestScore = currScore;
            bestIndex = i;
        i = i + 1;

    print bestScore

    return gridCollection[bestIndex][1];
