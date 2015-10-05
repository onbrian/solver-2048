import sys
import numpy as np
from collections import deque
import Queue
sys.path.insert(0, './../')
import functions as Tools;
from smartGridClass import smartGrid
from nodeClass import sgNode

def dangerousMove(penultimateNode):
    timeTraveler = penultimateNode;
    while (True):
        if (timeTraveler.isBaseNode()):
            break;
        assert (not timeTraveler.stepToHere is None);
        assert (not timeTraveler.prevNode is None);
        currentSg = timeTraveler.sg;

        # array of tile values of current smart grid, ordered largest to smallest
        values = currentSg.getOrderedValues();

        # check if top tile is moved out of place
        if (values[0] != currentSg.intGrid[0][0] and values[0] > 4):
            return False;
            # check if top tile is moved out of place
        elif (values[1] != currentSg.intGrid[0][1] and values[1] > 256):
            return False;

        timeTraveler = timeTraveler.prevNode;

    return True;

def evaluate1(sg, penultimateNode):
    score = 0;

    if (dangerousMove(penultimateNode)):
        score = score - 10000;

    values = sg.getOrderedValues();

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
        #if (x % 2 != 0):
        #   yRange = yRange2;
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
        secondRow.append(sg.intGrid[1][y]);

    for y in range(4):
        if (sg.mergedGrid[1][y] == True):
            score = score + 200 * (4-y);
        secondRow.append(sg.intGrid[1][y]);

    secondRow.sort(reverse = True);
    if (secondRow[0] == sg.intGrid[1][0] or secondRow[0] == sg.intGrid[1][3]):
        score = score + 1500;
    return score

def evaluate(sg, penultimateNode):
    score = 0;

    if (not dangerousMove(penultimateNode)):
        score = score - 10000;

    values = sg.getOrderedValues();

    if (values[0] == sg.intGrid[0][0]):
        score = score + 2000;
    if (values[1] == sg.intGrid[0][1] and values[0] > 32):
        score = score + 1000;
    if (values[2] == sg.intGrid[0][2]):
        score = score + 50;
    if (values[3] == sg.intGrid[0][3]):
        score = score + 50;

    for x in xrange(2, 4):
        for y in range(4):
            if (sg.intGrid[x][y] > 0):
                score = score - 5;

    secondRow = []

    for y in range(4):
        if (sg.mergedGrid[0][y] == True):
            score = score + 80 * (4 - y);

    for y in range(4):
        if (sg.mergedGrid[1][y] == True):
            score = score + 20 * y;
        secondRow.append(sg.intGrid[1][y]);

    secondRow.sort(reverse = True);
    if (secondRow[0] == sg.intGrid[1][0] or secondRow[0] == sg.intGrid[1][3]):
        score = score + 100;

    # trace backwards

    return score

def easyFilter(currentNode):
    # base node; shouldn't receive this
    assert (not currentNode.isBaseNode());

    # not base node; get previous node
    previousNode = currentNode.prevNode;

    # get their smart grids
    currentSg = currentNode.sg;
    previousSg = previousNode.sg;

    # array of tile values of current smart grid, ordered largest to smallest
    values = currentSg.getOrderedValues();

    # check if stale move
    if (np.array_equal(currentSg.intGrid, previousSg.intGrid)):
        return False;
    return True;

def pickyFilter(currentNode):
    # base node; shouldn't receive this
    assert (not currentNode.isBaseNode());

    # not base node; get previous node
    previousNode = currentNode.prevNode;

    # get their smart grids
    currentSg = currentNode.sg;
    previousSg = previousNode.sg;

    # array of tile values of current smart grid, ordered largest to smallest
    values = currentSg.getOrderedValues();

    # check if stale move
    if (np.array_equal(currentSg.intGrid, previousSg.intGrid)):
        return False;
    # check if top tile is moved out of place
    elif (values[0] != currentSg.intGrid[0][0] and values[0] > 4):
        return False;
        # check if top tile is moved out of place
    elif (values[1] != currentSg.intGrid[0][1] and values[1] > 256):
        return False;

    return True;

def getNodeCollection(stepsAhead, firstNode, nodeFilter):
    assert (type(stepsAhead) is int);
    assert (stepsAhead >= 1);
    assert (isinstance(firstNode, sgNode));

    nodeCollection = deque();

    dq = deque();
    # add first node
    dq.append(firstNode);

    while (dq):
        currentNode = dq.popleft();

        # base node case
        # don't add to collection
        # but add its future
        if (currentNode.isBaseNode()):
            pass;
        # non-base node doesn't pass filter
        # don't add to collection
        # don't add its future to collection
        elif (not nodeFilter(currentNode)):
            continue;
        # non-base node passes filter
        # add it to collection
        # add its future to collection
        else:
            nodeCollection.append(currentNode);

        # break if looking too far into future
        if (currentNode.moveCount > stepsAhead):
            break;

        # create three more nodes (its future)
        # append them to deque

        # get current smart grid
        currentSg = currentNode.sg;
        # get new move count
        newMoveCount = currentNode.moveCount + 1;

        # get future smart grids
        leftSg = currentSg.simulateMove("left");
        rightSg = currentSg.simulateMove("right");
        upSg = currentSg.simulateMove("up");

        # get future scores for smart grids
        leftScore = evaluate(leftSg, currentNode);
        rightScore = evaluate(rightSg, currentNode);
        upScore = evaluate(upSg, currentNode);

        # create nodes
        leftNode = sgNode(leftSg, leftScore, currentNode, "left", newMoveCount);
        rightNode = sgNode(rightSg, rightScore, currentNode, "right", newMoveCount);
        upNode = sgNode(upSg, upScore, currentNode, "up", newMoveCount);

        # add them to queue
        dq.append(leftNode);
        dq.append(rightNode);
        dq.append(upNode);

    return nodeCollection;

def generateNextMoves(game_state):

    # how many steps to look ahead
    stepsAhead = 5;

    # create the smart grid of the base grid
    grid = Tools.getGridState(game_state);
    sg = smartGrid(True, grid, None);

    # use the base smart grid to create the first node
    firstNode = sgNode(sg, None, None, None, 0);

    nodeCollection = getNodeCollection(stepsAhead, firstNode, pickyFilter);

    if (not nodeCollection):
        nodeCollection = getNodeCollection(stepsAhead, firstNode, easyFilter);

    if (not nodeCollection):
        return ['down']

    # find best smart grid node
    # arbitrarily set to first node to begin search
    timeTraveler = nodeCollection[0];
    for node in (nodeCollection):
        if (node.score > timeTraveler.score):
            timeTraveler = node;

    moves = [];
    # trace node backwards to process moves
    while (True):
        if (timeTraveler.isBaseNode()):
            break;
        assert (not timeTraveler.stepToHere is None);
        assert (not timeTraveler.prevNode is None);
        moves.append(timeTraveler.stepToHere)
        timeTraveler = timeTraveler.prevNode;

    moves.reverse();
    return moves
