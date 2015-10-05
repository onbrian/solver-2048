import numpy as np
# merged grid class
class mergedGrid:
    # grid should be a 4x4 2D array
    def __init__(self, intGrid, boolGrid):
        assert (intGrid.shape[0] == 4)
        assert (intGrid.shape[1] == 4)
        assert (boolGrid.shape[0] == 4)
        assert (boolGrid.shape[1] == 4)

        self.intGrid = np.copy(intGrid);
        self.boolGrid = np.copy(boolGrid);

    def ToValuesGrid(self):
        return np.copy(self.intGrid)

    def ToMergedGrid(self):
        return np.copy(self.boolGrid)
