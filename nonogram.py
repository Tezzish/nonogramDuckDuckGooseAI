class nonogram:
    def __init__(self, size, clues):
        self.size = size
        self.grid = self.generate_grid()
        # clues is a tuple of arrays where the first array is the clues of the rows
        # the second is the clues of the column
        # the arrays are two dimensional as there are a variable number of numbers per clue
        self.clues = clues
        # boolean for if the board is solved
        self.solved = False
        # the number of mistakes, if this is more than 3, we terminate the game
        self.mistakes = 0
    
    def generate_grid(self):
        # Create a 2d array with the size of the grid
        grid = [[0 for i in range(self.size)] for j in range(self.size)]

        # Fill the grid with 0's
        for i in range(self.size):
            for j in range(self.size):
                grid[i][j] = 0
        
        return grid
    
    def make_move(self, move: tuple):
        # Check if the move is valid
        if self.is_valid_move(move):
            # Update the grid
            self.grid[move[0]][move[1]] = 1
            # We could also check if the puzzle is solved here but we'll let the user do that via a button
            return True
        else:
            return False
        
    def is_valid_move(self, move: tuple):
        #checks if the move is in the grid
        if move[0] < self.size and move[1] < self.size:
            # if it's already selected, it's not a valid move so we return false
            if self.grid[move[0]][move[1]] == 1:
                return False
            else:
                return True
        else:
            return False
         
    def is_solved(self):
        # check if the grid is solved
        # we do this by checking if for each row and column the clues are satisfied
        # we'll start with the rows
        row_clues = self.clues[0]
        for i in range(self.size):
            # call check line function with the clues and the line
            if not self.check_line(self.grid[i], row_clues[i]):
                return False

        # next check the columns
        col_clues = self.clues[1]
        for i in range(self.size):
            # use python indexing to get the slice
            column = [row[i] for row in self.grid]
            if not self.check_line(column, col_clues[i]):
                return False
        return True

    def check_line(self, line, clues):
        # go through the line and check if it fulfills the clues
        curr_count = 0
        curr_clue = 0
        # we don't care about the "whitespace" before and after the values
        encountered = False
        for i in range(len(line)):
            if line[i] == 0 and encountered and curr_count > 0:
                #check if the current count is equal to the current clue
                if curr_count != clues[curr_clue]:
                    return False

                #increase the curr_clue
                curr_clue += 1
                if curr_clue >= len(clues):
                    return True
                #reset the counter
                curr_count = 0
                
            if line[i] == 1:
                if not encountered:
                    encountered = True
                curr_count += 1
            
        if (curr_clue != len(clues) - 1):
            return False
        return True