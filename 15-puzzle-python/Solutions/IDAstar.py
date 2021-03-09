import time

class Node:
    def __init__(self, state, zeroIndex, parent=None, move=None):
        self.state = state          # List representing the state of the board
        self.parent = parent        # Refrence to the parent node
        self.move = move            # String storing the action taken to generate current node from parent node
        self.zeroIndex = zeroIndex  # Tuple storing index of the empty tile.
        
    def __str__(self):
        return  str(self.state)     # Returns string representation of the board

goalState = [[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]] 
goalStateIndices = ((0,0),(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(2,3),(3,0),(3,1),(3,2),(3,3))
# Heurestic = Manhattan distance + 2*linear conflict
def calculateHeurestic(state):
    heurestic = 0
    conflict = 0
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
                        conflict += 1
            if(y==j):
                for k in range(i,4):
                    if state[k][j] != 0 and goalStateIndices[state[k][j]][1] == j and state[k][j]<num:
                        conflict += 1
            heurestic += abs(i - x) + abs(j - y)
    return heurestic + 2*conflict

# Returns tuple containing index of the num in lst
def getIndex(lst,num):
    for i,x in enumerate(lst):
        if num in x:
            return (i,x.index(num))

# Returns neighbours of node not yet visited
def getNeighbours(node,visited):
    n1=n2=n3=n4=None
    i = node.zeroIndex[0]
    j = node.zeroIndex[1]
    if i+1<4:
        node.state[i][j], node.state[i+1][j] = node.state[i+1][j],node.state[i][j]
        tempstr = str(node)
        if tempstr not in visited:
          n1 = Node(list(map(list,node.state)),(i+1,j),node, 'Down')
        node.state[i][j], node.state[i+1][j] = node.state[i+1][j],node.state[i][j]

    if i-1>-1:
        node.state[i][j], node.state[i-1][j] = node.state[i-1][j],node.state[i][j]
        tempstr = str(node)
        if tempstr not in visited: 
          n2 = Node(list(map(list,node.state)),(i-1,j),node, 'Up')
        node.state[i][j], node.state[i-1][j] = node.state[i-1][j],node.state[i][j]

    if j+1<4:
        node.state[i][j], node.state[i][j+1] = node.state[i][j+1],node.state[i][j]
        tempstr = str(node)
        if tempstr not in visited:
          n3 = Node(list(map(list,node.state)),(i,j+1),node, 'Right')
        node.state[i][j], node.state[i][j+1] = node.state[i][j+1],node.state[i][j]
    
    if j-1>-1:
        node.state[i][j], node.state[i][j-1] = node.state[i][j-1],node.state[i][j]
        tempstr = str(node)
        if tempstr not in visited:
          n4 = Node(list(map(list,node.state)),(i,j-1),node, 'Left')
        node.state[i][j], node.state[i][j-1] = node.state[i][j-1],node.state[i][j]        
    return (n1,n2,n3,n4)

# Converts input list to a list containing numbers
def convertToNum(lst):
    for i in range(4):
        for j in range(4):
            if (lst[i][j].isdigit()):
                lst[i][j] = int(lst[i][j])
            else:
                lst[i][j] =  10 + ord(lst[i][j]) - ord("A")

# Resursively search all the nodes with f < threshold and returns either the goalNode(if found) 
# or the next minimum f value greater than the threshold along with number of nodes generated
def search(node,g,threshold,visited):
    f = g + calculateHeurestic(node.state)
    nodesGenerated = 1
    if f > threshold:
        return f,nodesGenerated
    if node.state == goalState:
        return node,nodesGenerated
    mn = float("inf") # Minimum f value greater than current threshold
    for neighbour in getNeighbours(node,visited):
        tempstr = str(neighbour)
        if neighbour is None or tempstr in visited:
            continue
        visited.add(tempstr)
        temp,countNodes = search(neighbour,g+1,threshold,visited)
        nodesGenerated += countNodes
        if isinstance(temp, Node):
            return temp,nodesGenerated
        if temp < mn:
            mn = temp
        visited.remove(tempstr)
    return mn,nodesGenerated

def FindMinimumPath(initialState,goalState):
    minPath=[] # This list should contain the sequence of actions in the optimal solution
    nodesGenerated=0 # This variable should contain the number of nodes that were generated while finding the optimal solution
    convertToNum(initialState)
    rootNode = Node(initialState,getIndex(initialState,0))
    threshold = calculateHeurestic(rootNode.state)
    visited = set() # Set keeping track of vivited node
    rootString = str(rootNode)
    while True:
        visited.clear()
        visited.add(rootString)
        temp,countNodes = search(rootNode,0,threshold,visited)
        nodesGenerated += countNodes
        if isinstance(temp,Node):
            break
        if temp == float("inf"):
            return minPath,nodesGenerated
        threshold = temp
    
    while temp.parent != None:
        minPath.append(temp.move)
        temp = temp.parent

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
