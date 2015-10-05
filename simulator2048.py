from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from math import exp, expm1
from collections import deque
import time
import json
import sys
import numpy as np
import functions as Tools

from smartGridClass import smartGrid
from nodeClass import sgNode

sys.path.insert(0, './nextMove/')
from futureFutureAlgorithm import generateNextMoves

'''
test_game_state = '{"grid":{"size":4,"cells":[[{"position":{"x":0,"y":0},"value":2},{"position":{"x":0,"y":1},"value":2},{"position":{"x":0,"y":2},"value":4},{"position":{"x":0,"y":3},"value":4}],[{"position":{"x":1,"y":0},"value":32},{"position":{"x":1,"y":1},"value":16},{"position":{"x":1,"y":2},"value":16},null],[{"position":{"x":2,"y":0},"value":16},{"position":{"x":2,"y":1},"value":4},null,null],[null,{"position":{"x":3,"y":1},"value":2},null,{"position":{"x":3,"y":3},"value":2}]]},"score":264,"over":false,"won":false,"keepPlaying":false}';
test_game_state = json.loads(test_game_state);
grid = Tools.getGridState(test_game_state);

# create root node
sg = smartGrid(True, grid, None);
firstNode = sgNode(sg, None, None, None, 0);

# create second node
nextSg = firstNode.sg.simulateMove("right");
secondNode = sgNode(nextSg, 2, firstNode, "right", 1);
print firstNode.isFirstMove();
print secondNode.isFirstMove();

print "original grid: "
print secondNode.prevNode.sg.intGrid

print "grid after 1 move right: "
print secondNode.sg.intGrid
print secondNode.stepToHere

dq = deque();

dq.append(firstNode);
dq.append(secondNode);

print dq[0]
print dq.popleft();
print bool(dq);
#generateNextMove(test_game_state);

print firstNode.isBaseNode()
'''
##########################################
##### Driver/Global Variables Setup ######
##########################################

print "hello, world";
driver = webdriver.Firefox();
driver.get("http://gabrielecirulli.github.io/2048/");
gridElement = driver.find_element_by_class_name('grid-container');

##########################################
######## Start 2048 Manipulation #########
##########################################

print "start!";
game_state = Tools.getGameState(driver);
grid = Tools.getGridState(game_state)
sg = smartGrid(True, grid, None);
print;

highestTile = sg.getHighestTile();

# move up
#Tools.move(gridElement, "up");
# move right
#Tools.move(gridElement, "left");

moveC = 0;
while(highestTile < 2048):
    moves = generateNextMoves(game_state);
    for move in (moves):
        print "move: " + str(moveC);
        print move
        moveC = moveC + 1;
        Tools.move(gridElement, move);
        game_state = Tools.getGameState(driver);
        grid = Tools.getGridState(game_state)
        sg = smartGrid(True, grid, None);
        highestTile = sg.getHighestTile();
