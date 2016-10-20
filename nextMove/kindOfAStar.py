import sys
import numpy as np
from collections import deque
import Queue
sys.path.insert(0, './../')
import functions as Tools;
from smartGridClass import smartGrid
from nodeClass import sgNode

def evaluate(sg):
    score = 0;
    values = sg.getOrderedValues();

    if (values[0] == sg.intGrid[0][0] and values[0] > 4):
        score = score + 1000;
    else:
        score = score - 10000

    if (values[1] == sg.intGrid[0][1] and values[0] > 32):
        score = score + 50;
    if (values[2] == sg.intGrid[0][2]):
        score = score + 10;
    if (values[3] == sg.intGrid[0][3]):
        score = score + 5;

    secondRow = []

    for y in range(4):
        if (sg.mergedGrid[0][y] == True):
            score = score + 10;

    for y in range(4):
        if (sg.mergedGrid[1][y] == True):
            score = score + 5 * y;
        secondRow.append(sg.intGrid[1][y]);

    secondRow.sort(reverse = True);
    if (secondRow[0] == sg.intGrid[1][0] or secondRow[0] == sg.intGrid[1][3]):
        score = score + 5;

    return score

def isStaleMove(currentNode):
    # base node; shouldn't receive this
    assert (not currentNode.isBaseNode());

    # not base node; get previous node
    previousNode = currentNode.prevNode;

    # get their smart grids
    currentSg = currentNode.sg;
    previousSg = previousNode.sg;

    # check if stale move
    if (np.array_equal(currentSg.intGrid, previousSg.intGrid)):
        return True;

    return False

# how many steps to look ahead
def generateNextMoves(game_state, stepsAhead=5):

    # create the smart grid of the base grid
    grid = Tools.getGridState(game_state);
    sg = smartGrid(True, grid, None);

    # use the base smart grid to create the first node
    firstNode = sgNode(sg, 0, None, None, 0);

    frontier = deque()
    frontier.append(firstNode)
    newFrontier = deque()

    for i in xrange(0, stepsAhead + 1):
        # for each node in old frontier...
        while frontier:
            currentNode = frontier.popleft()

            # generate three new nodes from current node
            # get future smart grids
            leftSg = currentNode.sg.simulateMove("left");
            rightSg = currentNode.sg.simulateMove("right");
            upSg = currentNode.sg.simulateMove("up");

            # create nodes
            leftNode = sgNode(leftSg, currentNode.score + evaluate(leftSg), 
                              currentNode, "left", currentNode.moveCount + 1);
            rightNode = sgNode(rightSg, currentNode.score + evaluate(rightSg), 
                               currentNode, "right", currentNode.moveCount + 1);
            upNode = sgNode(upSg, currentNode.score + evaluate(upSg), 
                               currentNode, "up", currentNode.moveCount + 1);

            # add them to queue
            if (not isStaleMove(leftNode)):
                newFrontier.append(leftNode);
            if (not isStaleMove(rightNode)):
                newFrontier.append(rightNode);
            if (not isStaleMove(upNode)):
                newFrontier.append(upNode);

        # copy over new frontier to old frontier
        while newFrontier:
            frontier.append(newFrontier.popleft())

    if (not frontier):
        downSg = sg.simulateMove("down");
        downScore = evaluate(downSg, firstNode);
        downNode = sgNode(downSg, downScore, firstNode, "down", 1);
        nodeDq = deque();
        nodeDq.append(downNode);
        return nodeDq;

    # find best smart grid node
    # arbitrarily set to first node to begin search
    timeTraveler = frontier[0];
    for node in (frontier):
        if (node.score > timeTraveler.score):
            timeTraveler = node;

    print timeTraveler.score
    nodeDq = deque();


    # ignore first one
    timeTraveler = timeTraveler.prevNode.prevNode

    # trace node backwards to build moves
    while (True):
        if (timeTraveler.isBaseNode()):
            break;
        assert (not timeTraveler.stepToHere is None);
        assert (not timeTraveler.prevNode is None);

        # push sg onto deque
        nodeDq.appendleft(timeTraveler);
        timeTraveler = timeTraveler.prevNode;

    return nodeDq
