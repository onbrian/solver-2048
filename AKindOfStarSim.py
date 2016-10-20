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
from kindOfAStar import generateNextMoves

'''
test_game_state = '{"grid":{"size":4,"cells":[[{"position":{"x":0,"y":0},"value":2},{"position":{"x":0,"y":1},"value":0},{"position":{"x":0,"y":2},"value":0},{"position":{"x":0,"y":3},"value":0}],[{"position":{"x":1,"y":0},"value":0},{"position":{"x":1,"y":1},"value":0},{"position":{"x":1,"y":2},"value":0},null],[{"position":{"x":2,"y":0},"value":0},{"position":{"x":2,"y":1},"value":2},null,null],[null,{"position":{"x":3,"y":1},"value":0},null,{"position":{"x":3,"y":3},"value":0}]]},"score":264,"over":false,"won":false,"keepPlaying":false}';
test_game_state = json.loads(test_game_state);

moveCount = 0
while(moveCount < 1):
    nodeDq = generateNextMoves(test_game_state);
    print nodeDq
    while (nodeDq):
        currentNode = nodeDq.popleft();
        print "move: " + str(moveCount);
        print currentNode.stepToHere
        print currentNode.sg.intGrid
        print currentNode.score
        moveCount +=1;

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

moveC = 0;
while(highestTile < 2048):
    nodeDq = generateNextMoves(game_state);
    print nodeDq
    while (nodeDq):
        currentNode = nodeDq.popleft();
        print "move: " + str(moveC);
        print currentNode.stepToHere
        moveC = moveC + 1;
        Tools.move(gridElement, currentNode.stepToHere);


        game_state = Tools.getGameState(driver);
        grid = Tools.getGridState(game_state)
        sg = smartGrid(True, grid, None);
        highestTile = sg.getHighestTile();
