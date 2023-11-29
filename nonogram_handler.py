from nonogram import nonogram
import sqlite3
import json

class nonogram_handler:
    def __init__(self, size):
        self.mistakes = 0
        self.nonogram = None
        self.game_over = False
        self.size = size
        self.conn = sqlite3.connect('nonograms.db')
        self.c = self.conn.cursor()

    def generate_nonogram(self):
        # choose a random nonogram from the database
        # the table has two columns, size and clues
        # size is the size of the grid
        # clues is a json string of the clues
        # the clues are stored as a json string because they are a variable length
        # the clues are stored as a tuple of two arrays
        # the first array is the row clues
        # the second array is the column clues
        # select a random row from the table with a certain size
        # the size is passed in as a parameter
        self.c.execute(f"SELECT * FROM nonograms WHERE size = '{self.size}' ORDER BY RANDOM() LIMIT 1")
        # now we parse the input
        # the first element is the size
        # the second element is the clues
        unparsed_nonogram = self.c.fetchone()
        if unparsed_nonogram is None:
            self.nonogram = None
        else:
            # parse the size and the clues
            size = int(unparsed_nonogram[0])
            clues = json.loads(unparsed_nonogram[1])
            # create a new nonogram
            self.nonogram = nonogram(size, clues)
            print(self.nonogram)

    def make_move(self, move):
        # check if the move is valid
        if self.nonogram.is_valid_move(move):
            # update the grid
            self.nonogram.make_move(move)

    # check if solved
    # if it is solved, return a new nonogram
    # else increment the mistakes and if it's more than 3, quit the game
    def is_solved(self):
        if self.nonogram.is_solved():
            return True
        elif self.mistakes <= 3:
            self.mistakes += 1
            return False
        else:
            self.game_over = True
            return False
        
