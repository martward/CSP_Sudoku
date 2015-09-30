import sys
import time
from Classes import *


def main(argv):
    f = open('1000_sudokus.txt', 'r')
    puzzle = f.readline()
    puzzle = f.readline()
    print_puzzle(puzzle)
    f.close()
    sqs = list(puzzle)
    Sudoku = Puzzle(sqs)
    print Sudoku.get_numFilled()
    squares = Sudoku.get_squares()
    for sq in squares:
        constraints(sq, Sudoku)
    Sudoku.check_singles()
    print Sudoku.get_numFilled()
    

# This function removes the shared value from the domains of all squares which are in the same row
# or column as a square with only one value in it's domain.
# if i == index[0] they are in the same row
# if j == index[1] they are in the same column
# if i/3 == index[0]/3 and j/3 == index[1]/3) they are in the same 3x3 grid
def constraints(sq1, Sudoku):
    if len(sq1.get_domain()) == 1:
        value = sq1.get_domain()[0]
        index = sq1.get_index()
        
        squares = Sudoku.get_squares()
        for i in range(0,9):
            for j in range(0,9):
                if index != [i,j] and ((i == index[0] or j == index[1]) 
                                            or (i/3 == index[0]/3 and j/3 == index[1]/3) ):
                    sq2 = squares[(9*i+j)]
                    if value in sq2.get_domain():
                        sq2.remove_from_domain(value)
                        
#  This function prints the domains of all squares (Testing purposes)
def print_domains(squares):
    for i in range(0, len(squares)):
        print squares[i].get_domain()

# This function prints a visualization of the initial puzzle (Testing purposes)
def print_puzzle(puzzle):
    print "======================="
    puzz = list(puzzle)
    num = 0
    for i in range(0,9):
        row = "||"
        for j in range(0,9):
            if j%3 == 2:
                row = row + puzz[num] + "||"
            else:
                row = row + puzz[num] + "|"  
            num += 1
        print row
        if i%3 == 2:
            print "======================="
        else:
            print "-----------------------"
            

if __name__ == "__main__":
    main(sys.argv[1:])
