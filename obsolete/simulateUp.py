# return the layout of the grid after pressing the "up" arrow key
def simulateUp(grid):
    # board simulating after move
    after_move = np.empty((4, 4), dtype = object);

    # iterate through grid by going through each row
    for x in range(4):
        for y in range(4):
            tileValue = grid[x][y];

            # set this tile in after_move
            after_move[x][y] = futureTile(tileValue, False);

            effX = x;

            # check all tiles above, starting with closest tile first
            otherX = x - 1;

            # move current tile up as far as possible
            while (otherX >= 0 and tileValue != 0):
                # get tile directly above current tile
                otherTile = after_move[otherX][y];

                # case where other tile is an empty space
                if (otherTile.value == 0):
                    after_move[otherX][y] = futureTile(tileValue, False);
                    after_move[effX][y] = futureTile(0, False);
                    effX = effX - 1;
                    otherX = otherX - 1;
                # case where other tile is already merged
                elif (otherTile.merged):
                    break;
                # case where values are mismatched
                elif (otherTile.value != tileValue):
                    break;
                # case where merge is possible
                elif (otherTile.value == tileValue):
                    # combine tiles
                    after_move[otherX][y] = futureTile(otherTile.value * 2, True)
                    # erase original tile
                    after_move[effX][y] = futureTile(0, False);
                    break;

    for x in range(4):
        for y in range(4):
            tile = after_move[x][y]
            after_move[x][y] = tile.value
    return after_move
