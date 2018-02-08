# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 20:16:40 2018

@author: jkell
"""

import include as inc
import astar as AS
import copy

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
    children = maze[x][y].find_children(maze)      # where can we move
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
        
def get_progress(boxes):
    """
    Returns the number of boxes not on dots
    """
    work = 0
    for b in boxes:
        if (b.ondot == False):
            work+=1
    return work


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


def find_win_states(maze, boxes, startNode):
    boxstates = []
    winstates = []
    global debug
    
    boxstates.append((boxes,0,startNode,None))  # starting state
    leaststeps = 99
    
    """
    boxstates structure
        0. list of box objects
        1. total steps up to this point
        2. player position
        3. previous state
    """
    
    while len(boxstates) > 0:
        newboxstates = []
        
        if (debug==1):
            print("\n\nSTATES:",len(boxstates))
            
        smallestcost = 99
        
        for state,cost,position,previous in boxstates:
            if (debug==1):
                print("\n\nCurrent state:")
                print_state(maze, state, position)
            if get_progress(state) == 0:
                if (debug==1):
                    print("Win state.")
                #print("Win state found")
                winstates.append((state, cost, position, previous))
                if (cost < leaststeps):
                    leaststeps = cost
                continue
            
            if (cost > leaststeps):
                # this branch is not a feasible path
                continue
            
            if (cost < smallestcost):
                smallestcost = cost
            
            curstate = (state,cost,position,previous)
            
            
            moves = find_moves(maze, state, position)
            if (len(moves) == 0 and debug==1):
                print("No moves.")
            
            for m in moves:
                newstate = copy.deepcopy(state)
                num = m[0].id
                curbox = get_box(newstate, num)
                curx = curbox.x
                cury = curbox.y
                curbox.move(m[1].x, m[1].y)
                newboxstates.append((newstate, cost+m[3], maze[curx][cury], curstate))
                if (debug==1):
                    print("\n")
                    print("One possibility:")
                    print_state(maze, newstate, maze[curx][cury])
                    print("Cost of move:")
                    print(m[3])
                    print("Total cost of this state:")
                    print(cost+m[3])
                
        
        boxstates = newboxstates
    
    return winstates
    

def print_solution(maze, endState):
    print("SOLUTION:")
    process = []
    curstate = endState
    while curstate is not None:
        process.insert(0, curstate)
        curstate = curstate[3]
        
        
    for state in process:
        print("\n")
        print_state(maze, state[0], state[2])
        
    print("Total steps:", endState[1])
        
        
def Search(maze, boxes, startNode):
    # find all potential win states
    winstates = find_win_states(maze, boxes, startNode)

    bestcost = 9999
    beststate = None
    for state in winstates:
        if state[1] < bestcost:
            beststate = state
    
    print_solution(maze, beststate)
    
    

    
    
    
    
        
        
if __name__ == '__main__':
    # Initialize maze
    maze, boxes = inc.loadmaze("sokobanTest2.txt", True)

    # Find startNode
    start_x, start_y = inc.find_start(maze)
    startNode = maze[start_x][start_y]
    
    
    Search(maze, boxes, startNode)
    
    
    