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
        self.mistakes = 0

    def generate_nonogram(self):
        with open('nonograms.csv', 'r') as file:
            csvreader = csv.reader(file)
            # skip the header
            next(csvreader)
            # get the nonograms
            nonograms = [row for row in csvreader]
            # choose a random nonogram with the given size
            unparsed_nonogram = None
            # filter out the nonograms that don't have the right size
            nonograms = [nonogram for nonogram in nonograms if int(nonogram[0]) == self.size]
            if (len(nonograms) == 0):
                return
            # choose a random nonogram
            unparsed_nonogram = random.choice(nonograms)
            size = int(unparsed_nonogram[0])
            clues = json.loads(unparsed_nonogram[1])
            solution = json.loads(unparsed_nonogram[2])
            # create a new nonogram
            self.nonogram = nonogram(size, clues, solution)

    def is_correct_move(self, move):
        # check if the move is correct
        if self.nonogram.solution[move[0]][move[1]] == 1:
            return True
        else:
            return False
        
    def is_valid_move(self, move):
        # if it's in the grid
        if int(move[0]) < self.size and int(move[1]) < self.size:
                return True
        else:
            return False
        
    def make_move(self, move):
        valid = self.is_valid_move(move)
        correct = False
        if valid:
            correct = self.is_correct_move(move)
        # check if the move is valid and correct
        if valid and correct:
            # update the grid
            self.nonogram.make_move(move)
            return True
        # else it's a mistake
        else:
            self.mistakes += 1
            if self.mistakes > 2:
                self.game_over = True
            print("mistakes", self.mistakes)
            return False
                
    def is_solved(self):
        # check if the grid is solved
        # we do this by checking if for each row and column the clues are satisfied
        row_clues = self.nonogram.clues[0]
        for i in range(self.size):
            # call check line function with the clues and the line
            if not self.check_line(self.nonogram.grid[i], row_clues[i]):
                return False
        # next check the columns
        col_clues = self.nonogram.clues[1]
        for i in range(self.size):
            column = [row[i] for row in self.nonogram.grid]
            if not self.check_line(column, col_clues[i]):
                return False
        return True
    
    def check_line(self, line, clues):
        cluster = 0
        clusters = []
        for i in range(self.size):
            # if we encounter a 1, we increment the cluster
            if line[i] == 1:
                cluster += 1
            # if we encounter a 0, we check if the cluster matches the clue
            # if it does, we move onto the next clue
            # if it doesn't, we return false
            else:
                if cluster != 0:
                    clusters.append(cluster)
                cluster = 0
            # if we reach the end of the line, we check if the cluster matches the clue
            if i == self.size - 1 and cluster != 0:
                clusters.append(cluster)
        if clusters == clues:
            return True