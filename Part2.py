# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 20:16:40 2018

@author: jkell
"""

import include as inc

def next_move(maze):
    """
    Determine possible next moves
    
    """
    
def check_location(x,y,boxes):
    """
    Check if there is a box at (x,y)
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
        
        
if __name__ == '__main__':
    # Initialize maze
    maze, boxes = inc.loadmaze("sokobanTest.txt", True)

    # Find startNode
    start_x, start_y = inc.find_start(maze)
    startNode = maze[start_x][start_y]
    
    print_state(maze, boxes)
    
    