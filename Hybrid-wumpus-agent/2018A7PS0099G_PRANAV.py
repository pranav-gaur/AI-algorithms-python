#!/usr/bin/env python3
from Agent import * # See the Agent.py file


#### All your code can go here.

#### You can change the main function as you wish. Run this program to see the output. Also see Agent.py code.
countOfDpll = 0 #Counts how many time dpll was called

offx = [0,-1,0,1] # Offset along x axis
offy = [-1,0,1,0] # Offset along y axis
def getAdjRooms(i,j): # Returns room adjacent to the room at coordinate (i,j)
    adjRooms = []
    for k in range(4):
        if i+offx[k] >0 and i+offx[k] < 5 and j+offy[k] > 0 and j+offy[k] < 5:
            adjRooms.append([i+offx[k],j+offy[k]])
    return adjRooms 

# Wumpus = 1-16, Stench = 17-32, Pit = 33-48, Breeze = 49-64
def generateBackgroundKnowledge(): #Generates background knowledge and returns the Knowledge base
    knowledgeBase = [] #KB is a list of list where each sublist is a clause
    knowledgeBase.append([-1]) #Wumpus not present in room 1
    for i in range (1,5): # Adds Wij <=> Stench in adjacent rooms
        for j in range(1,5):
            adjRooms = getAdjRooms(j,i)
            percept = 16 + j + 4*(i-1)
            temp = [-1*percept]
            temp += [x[0] + 4*(x[1] - 1) for x in adjRooms]
            knowledgeBase.append(temp)
            for room in adjRooms:
                knowledgeBase.append([-1*(room[0] + 4*(room[1]-1)), percept])
    
    knowledgeBase.append([x for x in range(1,17)]) #Wumpus can be in any room
    for i in range(1,16): #Wumpus can be in atmost one room
        for j in range(i+1,17):
            knowledgeBase.append([-1*i,-1*j])
    tempKnowledgeBase = list(map(list, knowledgeBase)) #Copy of knowledge base. We can use the copy to generate kb for the pit and breeze by adding 16 to the absolute value of each literal as breeze/pit follow same rules as wumpus/pit 
    for i in range(len(tempKnowledgeBase)):
        for j in range(len(tempKnowledgeBase[i])):
            tempKnowledgeBase[i][j] = abs(knowledgeBase[i][j]) + 32
            if knowledgeBase[i][j]<0:
                tempKnowledgeBase[i][j] *= -1
    knowledgeBase += tempKnowledgeBase #Add the pit/breeze kn to wumpus/stench kb
    return knowledgeBase

def assignLiteral(knowledgeBase, literal): #Assign the literal in the kb and return the updated kb
    if knowledgeBase == -1 or len(knowledgeBase) == 0:
        return knowledgeBase
    newKnowledgeBase = [] #Updated kb
    for clause in knowledgeBase:
        if literal in clause: #If the literal is true in the clause then the clause is satisfied and we dont have to add it to the updated kb
            continue
        if -literal in clause:#If the literal is false in the clause then check how many literals are there in the clause except the curr literal
            newClause = []
            for tempLiteral in clause:
                if tempLiteral == -literal:
                    continue
                newClause.append(tempLiteral)
            if len(newClause) == 0:#If no other literal present in the clause then kb is unsatisfiable and return -1
                return -1
            newKnowledgeBase.append(newClause)#Construct a new clause with the remaining literals and add it to the kb
        else:
            newKnowledgeBase.append(clause)#If literal is not present in the clause then add the clause to updated kb
    return newKnowledgeBase #return the updated kb

def assignPureLiteral(knowledgeBase):
    if knowledgeBase == -1 or len(knowledgeBase) == 0: #If kb is unsatisfiable or kb is empty return kb
        return knowledgeBase
    literals = set() #set of literals
    for clause in knowledgeBase:
        for literal in clause:
            literals.add(literal)
    for literal in literals:
        if -literal not in literals:
            knowledgeBase = assignLiteral(knowledgeBase,literal) #if -literal is not present in kb then the literal is pure and assign it
            if knowledgeBase == -1 or len(knowledgeBase) == 0 :
                return knowledgeBase
    return knowledgeBase

def assignUnitClause(knowledgeBase):
    if knowledgeBase == -1 or len(knowledgeBase) == 0:
        return knowledgeBase
    while True:
        unitClauses = [] #List of unit clauses present
        for clause in knowledgeBase:
            if len(clause) == 1:
                unitClauses += clause
        if len(unitClauses) == 0:
            break
        for clause in unitClauses:
            knowledgeBase = assignLiteral(knowledgeBase, clause)
            if knowledgeBase == -1 or len(knowledgeBase) == 0:#IF kb becomes empty or unsatisfiable after assigning unit clause return kb
                return knowledgeBase
    return knowledgeBase

def findLiteral(knowledgeBase):# Return any non assigned literal from the kb
    for clause in knowledgeBase:
        for literal in clause:
            return literal
    
    

def dpll(knowledgeBase):#Returns True if KB is satisfiable and false if not
    global countOfDpll
    countOfDpll += 1
    knowledgeBase = assignPureLiteral(knowledgeBase)
    knowledgeBase = assignUnitClause(knowledgeBase)
    if knowledgeBase == -1: #After assigning Pure literals and Unit Clauses if any clause became empty return false
        return False
    if len(knowledgeBase) == 0: #After assigning Pure literals and Unit Clauses if all clauses have been satisfied return True
        return True
    literal = findLiteral(knowledgeBase)
    return dpll(assignLiteral(knowledgeBase, literal)) or dpll(assignLiteral(knowledgeBase, -literal))

def findActionsForNextRoom(currRoom,nextRoom,safe):#Find sequence of actions required to do from curr room to next room along the safe rooms. The path is foudn using BFS
    q = [] # Queue for BFS
    q.append(currRoom)
    prevRoom = {} # Dictionary which maps the curr room to its previous room 
    visited = set()
    visited.add(tuple(currRoom)) #Rooms visited in the BFS
    safe.add(tuple(nextRoom))
    while True:
        curr = q.pop(0)
        found = False
        for room in getAdjRooms(curr[0],curr[1]):
            if tuple(room) not in safe or tuple(room) in visited:
                continue
            prevRoom[tuple(room)] = curr
            if room == nextRoom:
                found = True
                break
            visited.add(tuple(room))
            q.append(room)
        if found:
            break
    actions = []
    temp = nextRoom
    while temp != currRoom:
        prevTemp = prevRoom[tuple(temp)]
        diff = [temp[0] - prevTemp[0], temp[1] - prevTemp[1]]
        if diff == [1,0]:
            actions.append("Right")
        elif diff == [0,1]:
            actions.append("Up")
        elif diff == [-1,0]:
            actions.append("Left")
        elif diff == [0,-1]:
            actions.append("Down")
        else:
            print("Error")
        temp = prevTemp
    return actions[::-1]
    
def ask(knowledgeBase, room): #Returns boolean value corresponding to the fact if the room is safe or not
    knowledgeBaseCopy1= list(map(list,knowledgeBase)) #Create 2 copies of the kb. first copy is used to ask whether room contains wumpus 
    knowledgeBaseCopy2 = list(map(list, knowledgeBase))# and the second copy asks whether the room contains pit or not 
    knowledgeBaseCopy1.append([1*(room[0] + 4*(room[1]-1))]) #Add Wumpus is present in the room
    knowledgeBaseCopy2.append([1*(room[0] + 4*(room[1]-1)) + 32])# Add Pit is present in the room
    return not dpll(knowledgeBaseCopy1) and not dpll(knowledgeBaseCopy2)# If KB != a then KB ^ -a is unsatisfiable. Therefore True is returned if both the copies of knowledgebase are unsatisfiable

def tell(knowledgeBase, currPercept, currRoom): #Adds the necessary sentence in the kb corresponding to the percept
    if currPercept[0] == True:
           knowledgeBase.append([16 + 32 + currRoom[0] + 4*(currRoom[1]-1)])
    else:
        knowledgeBase.append([-1*(16 + 32 + currRoom[0] + 4*(currRoom[1]-1))])
    
    if currPercept[1] == True:
        knowledgeBase.append([16 + currRoom[0] + 4*(currRoom[1]-1)])
    else:
        knowledgeBase.append([-1*(16 + currRoom[0] + 4*(currRoom[1]-1))])

def wumpusAgent(currRoom,currPercept ,knowledgeBase, visited, unvisitedAndSafe): #Returns list of actions for the current percept
    tell(knowledgeBase, currPercept, currRoom)
    for room in getAdjRooms(currRoom[0],currRoom[1]):
        if tuple(room) in visited:
            continue
        if ask(knowledgeBase, room):
            unvisitedAndSafe.append(room)
    if not unvisitedAndSafe: #If no unvisited and safe room if left, olan a route from current room to [4,4]
        return findActionsForNextRoom(currRoom,[4,4],visited)
    nextRoom = currRoom
    while nextRoom == currRoom:
        nextRoom = unvisitedAndSafe.pop(len(unvisitedAndSafe)-1)    
    return findActionsForNextRoom(currRoom,nextRoom,visited)
        

def main():
    ag = Agent()
    print('curLoc',ag.FindCurrentLocation())
    knowledgeBase = generateBackgroundKnowledge()#KB is a list of list where each sublist is a clause
    visited = set() #set of visited rooms
    unvisitedAndSafe = [] # list of rooms that are yet to be visited and are also safe to visit
    while True:
        currRoom = ag.FindCurrentLocation() 
        visited.add(tuple(currRoom))
        if currRoom == [4,4]: #Agent has exited the wumpus world so break the loop
            # print(countOfDpll) #Uncomment to get the number of times DPLL was called
            break
        actions = wumpusAgent(currRoom,ag.PerceiveCurrentLocation(),knowledgeBase, visited,unvisitedAndSafe) #Get list of actions agent should take based on current location and current percepts

        for action in actions: #Take tke actions
            # print('Percept [breeze, stench] :',ag.PerceiveCurrentLocation()) #Uncomment To print percept of current room
            ag.TakeAction(action)
       

if __name__=='__main__':
    main()
