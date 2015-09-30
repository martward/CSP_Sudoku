class Puzzle:
    def __init__(self, game):
        [self.squares, self.numFilled] = self.initialize_game(game)        
                   
    def initialize_game(self,game):
        sqs = []
        numClues = 0
        for i in range(0,9):
            for j in range(0,9):
                index_game = 9*i + j
                if game[index_game] == ".":
                    sqs.append(Square([i,j],0))
                else:
                    sqs.append(Square([i,j], int(game[index_game])))
                    numClues += 1
        return [sqs, numClues]
    
    def get_squares(self):
        return self.squares
        
    def get_numFilled(self):
        return self.numFilled
    
    def check_singles(self):
        num = 0
        for sq in self.squares:
            if len(sq.get_domain()) == 1:
                num += 1
        self.numFilled = num
        return num
 
class Square:
    def __init__(self, index, clue):
        self.index = index
        if clue != 0:
            self.domain = [clue]
        else:
            self.domain = [1,2,3,4,5,6,7,8,9]   
    
    def update_domain(self,newDomain):
        self.domain = newDomain
        
    def get_domain(self):
        return self.domain
        
    def get_index(self):
        return self.index
        
    def in_domain(self, value):
        if value in self.domain:
            return True
        else:
            return False
    
    def remove_from_domain(self, value):    
        self.domain.remove(value)
        
