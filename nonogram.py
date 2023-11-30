class nonogram:
    def __init__(self, size, clues, solution):
        self.size = size
        self.grid = self.generate_grid()
        # clues is a tuple of arrays where the first array is the clues of the rows
        # the second is the clues of the column
        # the arrays are two dimensional as there are a variable number of numbers per clue
        self.clues = clues
        # boolean for if the board is solved
        self.solved = False
        self.solution = solution
    
    def generate_grid(self):
        # Create a 2d array with the size of the grid
        grid = [[0 for i in range(self.size)] for j in range(self.size)]

        # Fill the grid with 0's
        for i in range(self.size):
            for j in range(self.size):
                grid[i][j] = 0
        
        return grid
    
    def make_move(self, move: tuple):
        self.grid[move[0]][move[1]] = 1