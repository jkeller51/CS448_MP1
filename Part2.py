# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 20:16:40 2018

@author: jkell
"""

import include as inc

def find_moves(maze, boxes):
    """
    Determine possible next moves (in terms of the next box to move and what direction)
    
    """
    moves = []
    
    for box in boxes:
        children = find_box_moves(box.x, box.y, maze, boxes)
        for child in children:
            moves.append([box,child])
            
    return moves
        
def find_box_moves(x,y, maze, boxes):
    """
    Find out which directions a box at (x,y) can move
    """
    children = maze[x][y].find_children(maze)      # where can we move
    children2 = []
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
    return children2
    
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
        
        
def Search(maze, boxes, startNode):
    
    boxstate = []
    while get_progress(boxes) > 0:
        
        moves = find_moves(maze, boxes)
        for m in moves:
            newstate = boxes.copy()
            num = m[0].id
            get_box(newstate, num).move(m[1].x, m[1].y)
            boxstate.append(newstate)
            print("One possibility:")
            print_state(maze, newstate)
        
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
    
    
    