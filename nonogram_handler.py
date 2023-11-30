from nonogram import nonogram
import json
import csv
import random

class nonogram_handler:
    def __init__(self, size):
        self.mistakes = 0
        self.nonogram = None
        self.game_over = False
        self.size = size

    def generate_nonogram(self):
        # choose a random nonogram from the database
        # the table has two columns, size and clues
        # now we parse the input
        # the first element is the size
        # the second element is the clues
        # open the csv file
        with open('nonograms.csv', 'r') as file:
            csvreader = csv.reader(file)
            # skip the header
            next(csvreader)
            # get the nonograms
            nonograms = [row for row in csvreader]
            # choose a random nonogram with the given size
            unparsed_nonogram = None
            # filter out the nonograms that don't have the right size
            print(nonograms[0])
            nonograms = [nonogram for nonogram in nonograms if nonogram[0] == self.size]
            # choose a random nonogram
            unparsed_nonogram = random.choice(nonograms)
            size = int(unparsed_nonogram[0])
            print(size)
            clues = json.loads(unparsed_nonogram[1])     
            print(clues)
            # create a new nonogram
            self.nonogram = nonogram(size, clues)

    def make_move(self, move):
        # check if the move is valid
        if self.nonogram.is_valid_move(move):
            # update the grid
            self.nonogram.make_move(move)
            return True
        else:
            return False

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
        
