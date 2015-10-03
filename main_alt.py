import sys
import time
import copy

class CSP:
    import itertools
    def __init__(self):
        self.variables = []
        self.domains = {}
        self.all_different_constraints = []
        '''
        All variables that sould be different from the variable dictionary
        keyed by variable, values are arrays of other variables
        '''
        self.variable_constraints = {}

    def add_variable(self, name, domain):
        self.variables.append(name)
        self.domains[name] = list(domain)

    def add_all_different_constraint(self, variables):
        self.all_different_constraints.append(variables)
       
    '''
    This function will print the result of the CSP, per variable we will print the single entry of that variables domain
    to a string of numbers. Just like the Sudoku input
    '''
    def output_string(self):
        string = ''
        for var in self.variables:
            string += str(self.domains[var][0])
        return string
        
    '''
    Build dictionary of different constraints per variable
    '''
    def build_variable_constraints(self):
        for variable in self.variables:
            var_constraints = []
            for constr in self.all_different_constraints:
                if variable in constr:
                    for index in constr:
                        if index != variable and index not in var_constraints:
                            var_constraints.append(index)
                                
            self.variable_constraints.update({variable:var_constraints})    
        
    '''
    This function checks for each variable with a domain of length one whether the value
    is present in the domains of any variable which is in the all different constraints of that value
    and removes this value from the domain if this is the case.
    '''
    def arc_consistency(self):
        check = False
        for var in self.variables:
            if len(self.domains[var]) == 1:
                value = self.domains[var][0]
                for var2 in self.variable_constraints[var]:
                    dom = self.domains[var2]
                    if value in dom:
                        dom.remove(value)
                        self.domains.update({var2:dom})
                        check = True
        return check

    def constraint_propagation(self):
        return self.arc_consistency()
    
    def happy(self):
        for domain in self.domains:
            if len(self.domains[domain]) != 1:
                return False
        return True
    
    def consistent(self):
        for domain in self.domains:
            if len(self.domains[domain]) == 0:
                return False
        return True
        
    def preprocess(self):
        return True
        
    def split(self):
        
        new_domain_key, new_domain_value_frist, new_domain_value_second = self.split_smallest_splittable_domain()
        
        first = copy.deepcopy(self)
        first.domains.update({new_domain_key:new_domain_value_frist})
        if first.solve_rec():
            self.domains = first.domains
            return True
        second = copy.copy(self)
        second.domains.update({new_domain_key:new_domain_value_second})
        if second.solve_rec():
            self.domains = second.domains
            return True
            
        return False
        
    def split_smallest_splittable_domain(self):
        domains = self.domains
        sorted_domains = sorted(domains, key=lambda k: len(domains[k]))
        
        new_domain_key = ''
        countPerValue = {'1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0}
        
        for sorted_domain in sorted_domains:
            if len(self.domains[sorted_domain]) == 1:
                key = self.domains[sorted_domain][0]
                if key in countPerValue:
                    value = countPerValue[key]
                    countPerValue.update({key: value + 1})
                else:
                    countPerValue.update({key:1})
            elif len(self.domains[sorted_domain]) > 1:
                new_domain_key = sorted_domain
                break
        
        #A = self.domains[new_domain_key]
        A = []
        for sortedValue in sorted(countPerValue, key=lambda k: countPerValue[k], reverse=False):
            if sortedValue in self.domains[new_domain_key]:
                A.append(sortedValue)
            
        new_domain_value_frist = A[:len(A)/2]
        new_domain_value_second = A[len(A)/2:]
        
        return new_domain_key,new_domain_value_frist,new_domain_value_second
    
    def solve(self):
        self.build_variable_constraints()
        
        return self.solve_rec()
        
    def solve_rec(self):
        willContinue = True
        
        while willContinue and not self.happy():
            self.preprocess()
            changed = self.constraint_propagation()
            if not self.happy():
                if not self.consistent():
                    willContinue = False
                elif changed == False:
                    self.split()
        
        return self.happy()

#
# MAIN
#

def main(argv):
    # if len(sys.argv) != 2:
    #     print 'Please enter two arguments, the first for the input file and the second for the result'
    #     sys.exit(0)
    # inputFilePath, outputFilePath = argv    
    
    inputFilePath = '1000_sudokus.txt'
    outputFilePath = '1000_solutions.txt'
    
    inputFilePointer = open(inputFilePath)
    outputFilePointer = open(outputFilePath, 'w+')
    
    totalCreationTime = 0
    totalSolveTime = 0

    line = inputFilePointer.readline()
    while line:
        
        # Create CSP
        
        startCreationTime = time.time()
        
        csp = create_sudoku_csp(line)
        
        endCreationTime = time.time()
        creationTime = endCreationTime - startCreationTime
        totalCreationTime += creationTime
        #print 'Creation time: ' + str(creationTime)
        
        # Solving
        
        startSolveTime = time.time()
        
        result = csp.solve()
        
        endSolveTime = time.time()
        solveTime = endSolveTime - startSolveTime
        totalSolveTime += solveTime
        
        if result:
            outputFilePointer.write(csp.output_string() + '\n')
            print 'Solve time: ' + str(solveTime)
        else:
            print 'Puzzle inconsistent'
            
        line = inputFilePointer.readline()
        #line = False
        
    outputFilePointer.close()
        
    print 'Total creation time: ' + str(totalCreationTime)
    print 'Total solve time: ' + str(totalSolveTime)
    print 'Total time: ' + str(totalSolveTime + totalCreationTime)
    
def create_sudoku_csp(line):
    split = lambda A, n=9: [A[i:i+n] for i in range(0, len(A), n)]
    board = split(line)
    

    csp = CSP()

    for row in range(9):
        for col in range(9):
            if board[row][col] == '.':
                csp.add_variable('%d-%d' % (row, col), map(str, range(1, 10)))
            else:
                csp.add_variable('%d-%d' % (row, col), [board[row][col]])
    for row in range(9):
        csp.add_all_different_constraint(['%d-%d' % (row, col) for col in range(9)])
    for col in range(9):
        csp.add_all_different_constraint(['%d-%d' % (row, col) for row in range(9)])
    for box_row in range(3):
        for box_col in range(3):
            cells = []
            for row in range(box_row * 3, (box_row + 1) * 3):
                for col in range(box_col * 3, (box_col + 1) * 3):
                    cells.append('%d-%d' % (row, col))
            csp.add_all_different_constraint(cells)

    return csp

if __name__ == "__main__":
    main(sys.argv[1:])