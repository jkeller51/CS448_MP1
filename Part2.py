# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 20:16:40 2018

@author: jkell
"""

import include as inc
import astar as AS
import copy

def find_moves(maze, boxes, startNode):
    """
    Determine possible next moves (in terms of the next box to move and what direction)
    
    Rejects paths where the player is blocked from getting into position.
    
    Structure returned:
        Each row has 3 objects
        1. Box to be moved
        2. Node to move to
        3. Node player needs to be in to perform the move
        4. Steps required for player to get into position
    
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
        
    
    
def print_state(maze, boxes):
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
        
def Search(maze, boxes, startNode):
    
    boxstate = []
    while get_progress(boxes) > 0:
        
        moves = find_moves(maze, boxes, startNode)
        for m in moves:
            newstate = copy.deepcopy(boxes)
            num = m[0].id
            get_box(newstate, num).move(m[1].x, m[1].y)
            boxstate.append(newstate)
            print("One possibility:")
            print_state(maze, newstate)
            print("Steps:")
            print(m[3])
        
        break
    
    
        
        
if __name__ == '__main__':
    # Initialize maze
    maze, boxes = inc.loadmaze("sokobanTest.txt", True)

    # Find startNode
    start_x, start_y = inc.find_start(maze)
    startNode = maze[start_x][start_y]
    
    print("Original state:")
    print_state(maze, boxes)
    
    Search(maze, boxes, startNode)
    
    
    