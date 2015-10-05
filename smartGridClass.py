import numpy as np

############################################
########## Local Helper Functions ##########
############################################
# must be 4x4 array
def rotateArray90(array):
    assert (type(array) is np.ndarray);
    assert (array.shape[0] == array.shape[1]);
    if (type(array[0][0]) is np.bool_):
        newArray = np.zeros((array.shape[0], array.shape[1]), dtype=np.bool_);
    elif(type(array[0][0]) is np.int64):
        newArray = np.zeros((array.shape[0], array.shape[1]), dtype=np.int);
    else:
        assert(False);

    for y in range(4):
        # collection of initial points
        initialCoordinates = [];
        for x in range(4):
            pair = [x, y];
            initialCoordinates.append(pair);

        finalCoordinates = [];
        for coordinate in initialCoordinates:
            newPair = [coordinate[1], coordinate[0]];
            finalCoordinates.insert(0, newPair);

        for pair, newPair in zip(initialCoordinates, finalCoordinates):
            newArray[newPair[0]][newPair[1]] = array[pair[0]][pair[1]];
    return newArray

# must be 4x4 array
def rotateArray(array, integer):
    assert (type(array) is np.ndarray);
    assert (type(integer) is int);
    assert (array.shape[0] == array.shape[1]);
    assert (integer >= 1)
    assert (integer <= 4)
    rotatedGrid = np.copy(array);
    for x in range(integer):
        rotatedGrid = rotateArray90(rotatedGrid);
    return rotatedGrid;

# return the layout of the grid after pressing the "up" arrow key
def simulateUp(grid):
    assert (type(grid) is np.ndarray);
    # board simulating after move
    postGridInt = np.zeros((4, 4), dtype = np.int);
    postGridBool = np.zeros((4, 4), dtype = bool);

    # iterate through grid by going through each row
    for x in range(4):
        for y in range(4):
            thisVal = grid[x][y];
            postGridInt[x][y] = thisVal;
            postGridBool[x][y] = False;

            # check all tiles above, starting with closest tile first
            otherX = x - 1;

            movingX = x;
            # move (non-empty) current tile up as far as possible
            while (otherX >= 0 and thisVal != 0):
                # get tile directly above current tile
                otherVal = postGridInt[otherX][y];
                otherMerged = postGridBool[otherX][y];

                # case where other tile is an empty space
                if (otherVal == 0):
                    # overwrite new tile with current tile
                    postGridInt[otherX][y] = thisVal;
                    postGridBool[otherX][y] = False;
                    # set old tile to empty space
                    postGridInt[movingX][y] = 0;
                    postGridBool[movingX][y] = False;
                    movingX = movingX - 1;
                    otherX = otherX - 1;
                # case where other tile is already merged
                elif (otherMerged):
                    break;
                # case where values are mismatched
                elif (otherVal != thisVal):
                    break;
                # case where merge is possible
                elif (otherVal == thisVal):
                    # overwrite new tile with new merged value
                    postGridInt[otherX][y] = thisVal + otherVal;
                    postGridBool[otherX][y] = True;
                    # set old tile to empty space
                    postGridInt[movingX][y] = 0;
                    postGridBool[movingX][y] = False;
                    break;
                else:
                    assert(False);
    return [postGridInt, postGridBool];

##############################################
############## smartGrid Class ###############
##############################################

class smartGrid:
    def __init__(self, isOriginal, intGrid, boolGrid):
        assert (type(isOriginal) is bool);

        # check type of intGrid
        assert (type(intGrid) is np.ndarray);
        for x in range(4):
            for y in range (4):
                assert (type(intGrid[x][y]) is int or type(intGrid[x][y]) is np.int64)

        # check dimensions of intGrid
        assert (intGrid.shape[0] == 4);
        assert (intGrid.shape[1] == 4);

        # if isOriginal is true, boolGrid should be None
        if (isOriginal):
            assert (boolGrid is None);
        # otherwise, it should be a 4 x 4 numpy array of bools
        else:
            assert (type(boolGrid) is np.ndarray);
            assert (boolGrid.shape[0] == 4)
            assert (boolGrid.shape[1] == 4)
            for x in range(4):
                for y in range (4):
                    assert (type(boolGrid[x][y]) is bool or type(boolGrid[x][y]) is np.bool_)


        self.intGrid = np.copy(intGrid);
        self.isOriginal = isOriginal;
        self.mergedGrid = np.copy(boolGrid);

    # count number of tiles (non-empty spaces) in the grid
    def countTiles(self):
        count = 0;
        for x in range(4):
            for y in range(4):
                if (self.intGrid[x][y] != 0):
                    count = count + 1;
        return count

    # return the highest value contained in the tiles in the game state parameter
    def getHighestTile(self):
        max = 0;
        for x in range(4):
            for y in range(4):
                currTile = self.intGrid[x][y];
                if (currTile > max):
                    max = currTile;
        assert (max != 0);
        return max;

    def getOrderedValues(self, reverseList = True):
        values = [];
        for x in range(4):
            for y in range(4):
                values.append(self.intGrid[x][y]);
        values.sort(reverse=reverseList);
        return values;


    # return the layout of the grid after pressing the arrow key in the
    # given direction
    def simulateMove(self, direction):
        assert (type(direction) is str);
        if (direction == "up"):
            prediction = simulateUp(self.intGrid);
            return smartGrid(False, prediction[0], prediction[1])
        elif (direction == "right"):
            rotatedGrid = rotateArray(self.intGrid, 3);
            prediction = simulateUp(rotatedGrid);
            prediction[0] = rotateArray(prediction[0], 1);
            prediction[1] = rotateArray(prediction[1], 1);
            return smartGrid(False, prediction[0], prediction[1])
        elif (direction == "left"):
            rotatedGrid = rotateArray(self.intGrid, 1);
            prediction = simulateUp(rotatedGrid);
            prediction[0] = rotateArray(prediction[0], 3);
            prediction[1] = rotateArray(prediction[1], 3);
            return smartGrid(False, prediction[0], prediction[1])
        elif (direction == "down"):
            rotatedGrid = rotateArray(self.intGrid, 2);
            prediction = simulateUp(rotatedGrid);
            prediction[0] = rotateArray(prediction[0], 2);
            prediction[1] = rotateArray(prediction[1], 2);
            return smartGrid(False, prediction[0], prediction[1])
        assert (False);
