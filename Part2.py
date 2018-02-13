# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 20:16:40 2018

@author: jkell
"""

import include as inc
import astar as AS
import copy
import time

debug=0

def find_moves(maze, boxes, startNode):
    """
    Determine possible next moves (in terms of the next box to move and what direction)
    
    Rejects paths where the player is blocked from getting into position.
    
    Structure returned:
        Each row has 4 objects
        0. Box to be moved
        1. Node to move to
        2. Node player needs to be in to perform the move
        3. Steps required for player to get into position
    
    """
    moves = []
    
    for box in boxes:
        children, playerpositions = find_box_moves(box.x, box.y, maze, boxes)
        for i in range(0,len(children)):
            child = children[i]
            pp = playerpositions[i]
            steps = find_path(maze, boxes, startNode, pp)
            if (steps != -1):
                # check if path exists for player
                # (may be slow)
                moves.append([box,child,pp,steps])
            
    return moves
        
def find_box_moves(x,y, maze, boxes):
    """
    Find out which directions a box at (x,y) can move
    """
    children = maze[x][y].find_children(maze,True)      # where can we move
    children2 = []
    playerpositions = []
    for c in children:
        if check_location(c.x,c.y, boxes):
            # just kidding, we can't move here because there is a box
            continue
        checkx = 2*x - c.x
        checky = 2*y - c.y    # opposite side of the box
        if (check_location(checkx, checky, boxes) or maze[checkx][checky].value == "%"):
            # we can't move this way because the player can't get into position
            continue
        
        # if we didn't continue, now we can add to the list
        children2.append(c)
        playerpositions.append(maze[checkx][checky])
    return children2, playerpositions
    
def check_location(x,y,boxes):
    """
    Check if there is a box at (x,y)
    Return true if there is
    """
    
    for a in boxes:
        if (a.x == x and a.y == y):
            return True
        else:
            continue
        
    return False
        
    
    
def print_state(maze, boxes, playerposition=None):
    """
    
    Print the current state of the map
    
    """
    for x in range(0,len(maze)):
        line=""
        for y in range(0,len(maze[0])):
            if (check_location(x,y,boxes)):
                if (maze[x][y].value == "."):
                    line+="B"
                else:
                    line+="b"
            else:
                # overwrite player position if we want to
                if (playerposition is None):
                    line+=maze[x][y].value
                else:
                    if (maze[x][y].value == "P"):
                        if (playerposition.x == x and playerposition.y == y):
                            line+="P"
                        else:
                            line+=" "
                    else:
                        if (playerposition.x == x and playerposition.y == y):
                            line+="P"
                        else:
                            line+=maze[x][y].value
        print(line)
        
def get_progress(boxes, dots=None):
    """
    Returns the number of boxes not on dots
    """
    work = 0
    accum_distance = 0
    for b in boxes:
        if (b.ondot == False):
            work+=1
            
        if (dots != None):
            # A* Search heuristic
            # add the city-block distance to the nearest dot
            mindistance = 999
            for d in dots:
                distance = abs(b.x - d.x) + abs(b.y - d.y)
                if (distance < mindistance):
                    mindistance = distance
            
            accum_distance+=mindistance
            
            
    return work+accum_distance


def get_box(boxes, ID):
    """
    Find a box by its ID
    """
    for b in boxes:
        if (b.id == ID):
            return b
    return None
        
        
def find_path(maze, boxes, startNode, endNode):
    """
    Find a path from start to end, avoiding boxes
    return number of steps of this path
    """
    maze_boxes = copy.deepcopy(maze)
    for b in boxes:
        maze_boxes[b.x][b.y].wall=1  # make boxes act like walls
        
    steps = AS.Search(maze_boxes, startNode, endNode)
    
    
    return steps

def in_corner(maze, node):
    # returns true if this location is in a corner
    # and not on a dot
    if (maze[node.x][node.y].value == "."):
        return False
    if ((maze[node.x-1][node.y].wall == 1 and  maze[node.x][node.y-1].wall == 1) or 
        (maze[node.x-1][node.y].wall == 1 and  maze[node.x][node.y+1].wall == 1) or
        (maze[node.x+1][node.y].wall == 1 and  maze[node.x][node.y+1].wall == 1) or
        (maze[node.x+1][node.y].wall == 1 and  maze[node.x][node.y-1].wall == 1)):
        return True
    return False


def add_box_state(maze, boxstates, this_state):
    """ adds the box state but checks for a duplicate in current states as
    well as previous states
    """
    boxes = this_state[0]
    index=-1
    lowcost = this_state[1]
    
    # first check for duplicates in past states
    previous = this_state[3]
    
    while previous != None:
        identical=1
        # check all the boxes
        for b in boxes:
            if not check_location(b.x, b.y, previous[0]):
                identical=0
                break
            
        if (previous[2] != this_state[2]):
            identical=0
            break
            
        if (identical==1): 
            # we found a duplicate, so we will not add this state to the queue
            return boxstates
        previous = previous[3]
    
    for i in range(0,len(boxstates)):
        state,cost,position,previous = boxstates[i]
        
        identical=1
        for b in boxes:
            if not check_location(b.x, b.y, state):
                identical=0
                break
            
        if (position != this_state[2]):
            identical=0
        
        if (identical == 0):
            continue
        
        index = i
        if (cost < lowcost):
            lowcost = cost
        
    if (index != -1 and lowcost > this_state[1]):
        # there is a duplicate that is worse. remove it
        boxstates.append(this_state)
        boxstates.pop(index)
    elif (index == -1):
        # no duplicates
        boxstates.append(this_state)
        
    return boxstates

def find_win_states_blind(maze, boxes, startNode):
    """
    Find the best win states
    Expands lowest cost next moves until a solution is found
    """
    boxstates = []
    winstates = []
    step=0
    global debug
    
    boxstates.append((boxes,0,startNode,None))  # starting state
    leaststeps = 999
    
    """
    boxstates structure
        0. list of box objects
        1. total steps up to this point
        2. player position
        3. previous state
    """
    
    while len(boxstates) > 0:
        
        if (debug==1):
            print("\n\nSTATES:",len(boxstates))
            
        smallestcost = 9999
        
        # find the lowest cost state to try next
        for state,cost,position,previous in boxstates:
            if (cost+get_progress(state) < smallestcost):
                togo = (state,cost,position,previous)
                smallestcost = cost+get_progress(state)
        
        (state,cost,position,previous) = togo
        
        ### BEGIN State expansion
        print("Cost:",cost)
        print("\n\nCurrent state:")
        print_state(maze, state, position)
        
        if (debug==1):
            print("\n\nCurrent state:")
            print_state(maze, state, position)
            
        if get_progress(state) == 0:
            if (debug==1):
                print("Win state.")
            #print("Win state found")
            winstates.append((state, cost, position, previous))
            boxstates.remove(togo)
            if (cost < leaststeps):
                leaststeps = cost
            continue
        
        if (cost > leaststeps):
            # obviously this branch isn't going to be the best
            break
        
        curstate = (state,cost,position,previous)
        
        step+=1
        
        moves = find_moves(maze, state, position)
        if (len(moves) == 0 and debug==1):
            print("No moves.")
        
        for m in moves:
            
            # check if this box is moved into a corner...
            # this is always a losing situation
            if (in_corner(maze,m[1])):
                
                continue
            
            newstate = copy.deepcopy(state)
            num = m[0].id
            curbox = get_box(newstate, num)
            curx = curbox.x
            cury = curbox.y
            curbox.move(m[1].x, m[1].y)
            #boxstates.append((newstate, cost+m[3], maze[curx][cury], curstate))
            boxstates = add_box_state(maze, boxstates, (newstate, cost+m[3], maze[curx][cury], curstate))
            if (debug==1):
                print("\n")
                print("One possibility:")
                print_state(maze, newstate, maze[curx][cury])
                print("Cost of move:")
                print(m[3])
                print("Total cost of this state:")
                print(cost+m[3])
        
        if togo in boxstates:        
            boxstates.remove(togo)
    
    return winstates,step


def find_win_states_smart(maze, boxes, startNode):
    """
    Find the best win states
    Expands lowest cost next moves until a solution is found
    """
    boxstates = []
    winstates = []
    dots = []
    step=0
    global debug
    
    boxstates.append((boxes,0,startNode,None))  # starting state
    leaststeps = 999
    
    """
    boxstates structure
        0. list of box objects
        1. total steps up to this point
        2. player position
        3. previous state
    """
    
    # load the dots into array
    for x in range(0,len(maze)):
        for y in range(0,len(maze[0])):
            if (maze[x][y].value == "." or maze[x][y].value == "B"):
                dots.append(maze[x][y])
                
    
    while len(boxstates) > 0:
        
        if (debug==1):
            print("\n\nSTATES:",len(boxstates))
            
        smallestcost = 9999
        
        # find the lowest cost state to try next
        for state,cost,position,previous in boxstates:
            if (cost+get_progress(state,dots) < smallestcost):
                togo = (state,cost,position,previous)
                smallestcost = cost+get_progress(state,dots)
        
        (state,cost,position,previous) = togo
        
        ### BEGIN State expansion
#        print("Cost:",cost)
#        print("\n\nCurrent state:")
#        print_state(maze, state, position)
        
        if (debug==1):
            print("\n\nCurrent state:")
            print_state(maze, state, position)
            
        if get_progress(state) == 0:
            if (debug==1):
                print("Win state.")
            #print("Win state found")
            winstates.append((state, cost, position, previous))
            boxstates.remove(togo)
            if (cost < leaststeps):
                leaststeps = cost
            continue
        
        if (cost > leaststeps):
            # obviously this branch isn't going to be the best
            break
        
        curstate = (state,cost,position,previous)
        
        step+=1
        
        moves = find_moves(maze, state, position)
        if (len(moves) == 0 and debug==1):
            print("No moves.")
        
        for m in moves:
            
            # check if this box is moved into a corner...
            # this is always a losing situation
            if (in_corner(maze,m[1])):
                
                continue
            
            newstate = copy.deepcopy(state)
            num = m[0].id
            curbox = get_box(newstate, num)
            curx = curbox.x
            cury = curbox.y
            curbox.move(m[1].x, m[1].y)
            #boxstates.append((newstate, cost+m[3], maze[curx][cury], curstate))
            boxstates = add_box_state(maze, boxstates, (newstate, cost+m[3], maze[curx][cury], curstate))
            if (debug==1):
                print("\n")
                print("One possibility:")
                print_state(maze, newstate, maze[curx][cury])
                print("Cost of move:")
                print(m[3])
                print("Total cost of this state:")
                print(cost+m[3])
        
        if togo in boxstates:        
            boxstates.remove(togo)
    
    return winstates,step

def print_solution(maze, endState, step):
    print("SOLUTION:")
    process = []
    curstate = endState
    while curstate is not None:
        process.insert(0, curstate)
        curstate = curstate[3]
        
        
    for state in process:
        print("")
        print_state(maze, state[0], state[2])
        
    print("Total cost:", endState[1])
    print("Number of expanded nodes:", step)
        
        
def Search(maze, boxes, startNode, smart=False):
    # find all potential win states
    if (smart == False):
        winstates,step = find_win_states_blind(maze, boxes, startNode)
    else:
        winstates,step = find_win_states_smart(maze, boxes, startNode)

    bestcost = 9999
    beststate = None
    for state in winstates:
        if state[1] < bestcost:
            beststate = state
            bestcost = state[1]
    
    print_solution(maze, beststate, step)
    
    

    
    
    
    
        
        
if __name__ == '__main__':
    # Initialize maze
    startTime = time.time()
    maze, boxes = inc.loadmaze("sokoban3.txt", True)

    # Find startNode
    start_x, start_y = inc.find_start(maze)
    startNode = maze[start_x][start_y]
    
    
    Search(maze, boxes, startNode, True)
    endTime = time.time()
    print('\nTime used: {0} min(s)'.format((endTime - startTime) / 60.0))
    
    