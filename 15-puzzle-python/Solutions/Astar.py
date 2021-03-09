#!/usr/bin/env python3
import time
from heapq import heappush,heappop

class Node:
    def __init__(self, state, level, zeroIndex, parent=None, move=None):
        self.state = state              #List representing current configration of the puzzle
        self.parent = parent            #Refrence to the parent Node
        self.move = move                #String containing the move required to generate current Node from parent
        self.level = level              #Int containing the depth of Node
        self.zeroIndex = zeroIndex      #Tuple containing the indices of the empty tile
    
    def __lt__(self,other):             #Compares two instances of Nodes. Required to push Nodes in heapq
        return False
    
    def __str__(self):                  #Returns string representation of the puzzle
        return  str(self.state)

goalStateIndices = ((0,0),(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(2,3),(3,0),(3,1),(3,2),(3,3)) #Tuple of tuples containing goalState indices of every tile.
#Returns heurestic of a node. h(n) = manhattan distance + 2*linear conflict
def calculateHeurestic(state):
    manhattan_distance = 0
    linear_conflict = 0
    for i in range(0,4):
        for j in range(0,4):
            num = state[i][j]
            if num == 0:
                continue
            x = goalStateIndices[num][0]
            y = goalStateIndices[num][1]
            if(x == i):
                for k in range(j,4):
                    if state[i][k] != 0 and goalStateIndices[state[i][k]][0] == i and state[i][k]<num:
                        linear_conflict += 1
            if(y==j):
                for k in range(i,4):
                    if state[k][j] != 0 and goalStateIndices[state[k][j]][1] == j and state[k][j]<num:
                        linear_conflict += 1
            manhattan_distance += abs(i - x) + abs(j - y)
    return manhattan_distance + 2*linear_conflict

#Returns tuple containing indices of num in lst
def getIndex(lst,num):
    for i,x in enumerate(lst):
        if num in x:
            return (i,x.index(num))

#Generates and returns neighbours of node not yet visited
def getNeighbours(node,closed):
    n1=n2=n3=n4=None
    i = node.zeroIndex[0]
    j = node.zeroIndex[1]
    if i+1<4:   #If empty tile can go down
        node.state[i][j], node.state[i+1][j] = node.state[i+1][j],node.state[i][j]
        tempstr = str(node)
        if tempstr not in closed: #If this puzzle configration has not been seen before
          n1 = Node(list(map(list,node.state)),node.level+1,(i+1,j),node, 'Down')
        node.state[i][j], node.state[i+1][j] = node.state[i+1][j],node.state[i][j]

    if i-1>-1: #If empty tile can go up
        node.state[i][j], node.state[i-1][j] = node.state[i-1][j],node.state[i][j]
        tempstr = str(node)
        if tempstr not in closed: #If this puzzle configration has not been seen before
          n2 = Node(list(map(list,node.state)),node.level+1,(i-1,j),node, 'Up')
        node.state[i][j], node.state[i-1][j] = node.state[i-1][j],node.state[i][j]

    if j+1<4: #If empty tile can go right
        node.state[i][j], node.state[i][j+1] = node.state[i][j+1],node.state[i][j]
        tempstr = str(node)
        if tempstr not in closed: #If this puzzle configration has not been seen before
          n3 = Node(list(map(list,node.state)),node.level+1,(i,j+1),node, 'Right')
        node.state[i][j], node.state[i][j+1] = node.state[i][j+1],node.state[i][j]
    
    if j-1>-1: #If empty tile can go left
        node.state[i][j], node.state[i][j-1] = node.state[i][j-1],node.state[i][j]
        tempstr = str(node)
        if tempstr not in closed: #If this puzzle configration has not been seen before
          n4 = Node(list(map(list,node.state)),node.level+1,(i,j-1),node, 'Left')
        node.state[i][j], node.state[i][j-1] = node.state[i][j-1],node.state[i][j]
        
    return (n1,n2,n3,n4)

#Converts elements in the lst to their numeric representation
def convertToNum(lst):
    for i in range(4):
        for j in range(4):
            if (lst[i][j].isdigit()):
                lst[i][j] = int(lst[i][j])
            else:
                lst[i][j] =  10 + ord(lst[i][j]) - ord("A")


def FindMinimumPath(initialState,goalState):
    minPath=[] # This list should contain the sequence of actions in the optimal solution
    nodesGenerated=0 # This variable should contain the number of nodes that were generated while finding the optimal solution
    closed = set() # set containing nodes that have been visited
    convertToNum(initialState)
    goalState = '[[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]'
    rootNode = Node(initialState,0,getIndex(initialState,0))
    rootHeurestic = calculateHeurestic(rootNode.state)
    if(rootHeurestic == 0):
        return minPath, nodesGenerated
    heap = []
    heappush(heap,(rootHeurestic, rootNode))
    currNode = None
    while heap:
        currNode = heappop(heap)[1]
        currStr = str(currNode)
        if(currStr in closed):
          continue
        closed.add(currStr)
        if (currStr == goalState):
            break
        for neighbour in getNeighbours(currNode,closed):
            if neighbour is None:
                continue
            nodesGenerated += 1
            heappush(heap,(neighbour.level + calculateHeurestic(neighbour.state), neighbour)) #Push neighbours in heap ordered by f(n)
    
    while currNode.parent != None:
        minPath.append(currNode.move)
        currNode = currNode.parent
    
    return minPath[::-1], nodesGenerated




#**************   DO NOT CHANGE ANY CODE BELOW THIS LINE *****************************


def ReadInitialState():
    with open("initial_state.txt", "r") as file: #IMP: If you change the file name, then there will be an error when
                                                        #               evaluators test your program. You will lose 2 marks.
        initialState = [[x for x in line.split()] for i,line in enumerate(file) if i<4]
    return initialState

def ShowState(state,heading=''):
    print(heading)
    for row in state:
        print(*row, sep = " ")

def main():
    initialState = ReadInitialState()
    ShowState(initialState,'Initial state:')
    goalState = [['0','1','2','3'],['4','5','6','7'],['8','9','A','B'],['C','D','E','F']]
    ShowState(goalState,'Goal state:')
    
    start = time.time()
    minimumPath, nodesGenerated = FindMinimumPath(initialState,goalState)
    timeTaken = time.time() - start
    
    if len(minimumPath)==0:
        minimumPath = ['Up','Right','Down','Down','Left']
        print('Example output:')
    else:
        print('Output:')

    print('   Minimum path cost : {0}'.format(len(minimumPath)))
    print('   Actions in minimum path : {0}'.format(minimumPath))
    print('   Nodes generated : {0}'.format(nodesGenerated))
    print('   Time taken : {0} s'.format(round(timeTaken,4)))

if __name__=='__main__':
    main()
