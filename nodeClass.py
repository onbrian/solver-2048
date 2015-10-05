import numpy as np
from smartGridClass import smartGrid
from collections import deque

# sg is the current smartGrid of the node
# score is the smartGrid's score
class sgNode:
    def __init__(self, sg, score, previous, stepToHere, moveCount):
        assert (isinstance(sg, smartGrid));
        assert (type(score) is int or score is None);
        assert (isinstance(previous, sgNode) or previous is None);
        assert (type(stepToHere) is str or stepToHere is None);
        assert (type(moveCount) is int and moveCount >= 0);

        self.sg = sg;
        self.score = score;
        self.prevNode = previous;
        self.stepToHere = stepToHere;
        self.moveCount = moveCount;

    def isFirstMove(self):
        # edge case where this is the root node
        # this means there is no previous node
        # return False because this means the first move hasnt been made yet
        if (self.prevNode is None):
            assert (self.score is None);
            assert (self.moveCount == 0);
            assert (self.stepToHere is None);
            return False;
        # the previous node exists
        # if the previous node is the root node, one move has been made
        # return True
        elif (self.prevNode.prevNode is None):
            assert (self.moveCount == 1);
            return True;
        # more than one move made
        # return False
        else:
            assert (self.moveCount > 1);
            return False;

    def isBaseNode(self):
        if (self.prevNode is None):
            assert (self.score is None);
            assert (self.moveCount == 0);
            assert (self.stepToHere is None);
            return True;
        else:
            assert (self.moveCount >= 1);
            return False;
