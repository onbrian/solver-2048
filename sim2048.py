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
from slowpokeAlgorithm import generateNextMoves

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
        currentNode = nodeDq.pop();
        print "move: " + str(moveC);
        print currentNode.stepToHere
        moveC = moveC + 1;
        Tools.move(gridElement, currentNode.stepToHere);


        game_state = Tools.getGameState(driver);
        grid = Tools.getGridState(game_state)
        sg = smartGrid(True, grid, None);
        highestTile = sg.getHighestTile();
'''
        currentSg = currentNode.sg;
        restart = False;

        for x in range(1):
            for y in range(4):
                if (currentSg.intGrid[x][y] != sg.intGrid[x][y]):
                    restart = True;

        if (restart):
            break;
'''
