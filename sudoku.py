#This is the implementation of sudoku solver using BACKTRACKING and BITMASKING and HEURISTIC SEARCH for cells with minimum candidates

from copy import deepcopy

grid=[    [3,0,6,5,0,8,4,0,0], 
          [5,2,0,0,0,0,0,0,0], 
          [0,8,7,0,0,0,0,3,1], 
          [0,0,3,0,1,0,0,8,0], 
          [9,0,0,8,6,3,0,0,5], 
          [0,5,0,0,9,0,6,0,0], 
          [1,3,0,0,0,0,2,5,0], 
          [0,0,0,0,0,0,0,7,4], 
          [0,0,5,2,0,6,3,0,0] ] 

grid2=[[9, 0, 6, 0, 7, 0, 4, 0, 3],
       [0, 0, 0, 4, 0, 0, 2, 0, 0],
       [0, 7, 0, 0, 2, 3, 0, 1, 0],
       [5, 0, 0, 0, 0, 0, 1, 0, 0],
       [0, 4, 0, 2, 0, 8, 0, 6, 0],
       [0, 0, 3, 0, 0, 0, 0, 0, 5],
       [0, 3, 0, 7, 0, 0, 0, 5, 0],
       [0, 0, 7, 0, 0, 5, 0, 0, 0],
       [4, 0, 5, 0, 1, 0, 7, 0, 8]  ]

#here we are using bitmasking to store which numbers are absent in a particular row
#if 5th bit is unset in a row that means 6 is present in that particular row
#if 4th bit is set then 5 is not present in that row
rows = [511 for i in range(9)]
cols = [511 for i in range(9)]
boxes = [511 for i in range(9)]

numbers = [[511 for j in range(9)] for i in range(9)]  


#initializing rows,cols and boxes
def initialize(grid):
    global rows,cols,boxes
    rows = [511 for i in range(9)]
    cols = [511 for i in range(9)]
    boxes = [511 for i in range(9)]
    
    for i in range(9):
        for j in range(9):

            if grid[i][j] != 0:
                num = grid[i][j] - 1
                test = (1<<num)
                rows[i] = rows[i] & (~test) 
                cols[j] = cols[j] & (~test)

                boxes[3*(i//3) + j//3] &= (~test)
            else:
                numbers[i][j] = 0


#for printing the sudoku in an understanding way
def printingGrid(grid):
    for i in range(9):
        if i%3 == 0 and i!= 0:
            print('-------+------+-------')
        for j in range(9):
            if j%3 == 0:
                print('|',end='')
            if grid[i][j] == 0:
                print('. ',end='')
            else:
                print(grid[i][j],end=' ')
        print('|')
    print()


#To find empty cells
def findEmptyCells(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return (i,j)
    return None


#Implementing the normal backtracking 
NodesInBacktrackingTree = 0

def backtracking(grid):
    global NodesInBacktrackingTree

    t = findEmptyCells(grid)
    if not t:
        print ('Nodes expanded in the Backtracking tree=',NodesInBacktrackingTree)
        printingGrid(grid)
        return True
    
    x,y = t

    IsPossible = rows[x] & cols[y] & boxes[3*(x//3) + y//3]
    for num in range(9):
        if IsPossible & (1<<num) != 0:
            #previously for checking whether a number can be placed in a respective cell we have to check row,col and box
            #now we just have to check ispossible variable since we integrated row,col,box values into the ispossible
            #using or(|) bitwise opertor thanks to BITMASKING

            NodesInBacktrackingTree += 1
            
            grid[x][y] = num + 1
            test = (1<<num)
            rows[x] = rows[x] & (~test)
            cols[y] = cols[y] & (~test)
            boxes[3*(x//3) + y//3] &= (~test)
            

            nextStep = backtracking(grid)
            if nextStep == True:
                return True
             #backtracking to previous step    
            grid[x][y] = 0
            rows[x] = rows[x] ^ test 
            cols[y] = cols[y] ^ test
            boxes[3*(x//3) + y//3] ^= test
    return False    #if none of the present value is valid,then there is a mistake inthe previous step backtrack there.


def CandidatesCount(i,j):
    count = 0
    test = rows[i] & cols[j] & boxes[3*(i//3) + j//3]
    
    for i in range(test.bit_length()):
        if test & (1<<i) != 0:  
            count += 1

    return count

#To find empty cells with minimum candidates for HEURISTIC SEARCH
def findEmptyCellsWithMinCandidates(grid):
    minx,miny = -1,-1
    minCount = 10
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                count = CandidatesCount(i,j)
                if count == 1:
                    return (i,j)
                elif count < minCount:
                    minCount = count
                    minx,miny = i,j
    return (minx,miny)


#Here in this Heuristic search we are selecting the empty cells with minimum candidates 
#so that we increase the probability of finding the correct candidate 
#thus we can decrease the number of nodes in the backtracking tree

#And the best part is,it will first find the naked singles available in the grid 

HeuristicSearchNodes = 0

def HeuristicBacktracking(grid):
    global HeuristicSearchNodes

    x,y = findEmptyCellsWithMinCandidates(grid)
    if x==-1 and y==-1:
        print ('Nodes expanded in the Heuristic Backtracking tree=',HeuristicSearchNodes)
        printingGrid(grid)
        return True
    
    IsPossible = rows[x] & cols[y] & boxes[3*(x//3) + y//3]
    for num in range(9):
        if IsPossible & (1<<num) != 0:
            
            HeuristicSearchNodes += 1
            grid[x][y] = num + 1
            test = (1<<num)
            rows[x] = rows[x] & (~test)
            cols[y] = cols[y] & (~test)
            boxes[3*(x//3) + y//3] &= (~test)
            #printingGrid(grid)

            nextStep = HeuristicBacktracking(grid)
            if nextStep == True:
                return True
             #backtracking to previous step    
            grid[x][y] = 0
            rows[x] = rows[x] ^ test 
            cols[y] = cols[y] ^ test
            boxes[3*(x//3) + y//3] ^= test
    return False   

def solve1(grid):
    initialize(grid)
    backtracking(grid)

def solve2(grid):
    initialize(grid)
    HeuristicBacktracking(grid)

g1 = deepcopy(grid)
g2 = deepcopy(grid)
solve1(g1)     ##solving using backtracking
solve2(g2)     ##solving using Heuristic backtracking
