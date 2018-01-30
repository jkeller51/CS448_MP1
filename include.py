# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 16:35:11 2018

@author: jkell
"""

import os

debug=1

class Node(object):
    beenthere=0
    wall=0
    previousNode=None;
    
    def __init__(self, cost, wall):
        self.cost = cost
        self.wall = wall


'''        
class Node(object):
    """ Using coordinates (x, y) to mark the position
    of this node.
    """
    beenthere = 0
    wall = 0
    previousNode = None;
    
    def __init__(self, x, y, char):
        self.x = x
        self.y = y
        self.value = char

        if char == "%":
            self.wall = 1

    def find_children(self, maze):
        children = []
        width = len(maze[0])
        height = len(maze)
        
        # up next
        if self.x  > 0:
            child_char = maze[self.x - 1][self.y]
            child = Node(self.x - 1, self.y, child_char)
            if (child.wall == 0) and (child.value != "P"):
                children.append(child)
            
        # left next
        if self.y  > 0:
            child_char = maze[self.x][self.y - 1]
            child = Node(self.x, self.y - 1, child_char)
            if (child.wall == 0) and (child.value != "P"):
                children.append(child)
            
        # right next
        if self.y + 1  < width:
            child_char = maze[self.x][self.y + 1]
            child = Node(self.x, self.y + 1, child_char)
            if (child.wall == 0) and (child.value != "P"):
                children.append(child)
            
        # bottom next
        if self.x + 1 < height:
            child_char = maze[self.x + 1][self.y]
            child = Node(self.x + 1, self.y, child_char)
            if (child.wall == 0) and (child.value != "P"):
                children.append(child)

        return children

    def set_previous_node(self, node):
        self.previousNode = node
'''
    

def loadmaze(filename):
    if not (os.path.exists(filename) and os.path.isfile(filename)):
        print("File not found!")
    try:
        file = open(filename)          # error handling
        
    except:
        print("File not found or accessible.")
        raise
    else:
        maze = []                 # initialize maze
        for line in file:
            maze.append(line)     # load maze line by line
            
        file.close()
    
        return maze


def find_start(maze):
    # find start position (P)
    q = 0
    startpos = (-1, -1)
    while q < len(maze):
        i = 0
        while i < len(maze[q]):       # search each character
            if (maze[q][i] == "P"):   # if it is the starting character "P"
                startpos = (q, i)     # update startpos
                break
            i += 1
        if (startpos != (-1, -1)):    # we're done here
            break
        q += 1
        
    if (debug == 1):        
        print(startpos)
    
    return startpos


def find_end(maze):
    # find goal position (.)
    q = 0
    endpos = (-1, -1)
    while q < len(maze):
        i = 0
        while i < len(maze[q]):       # search each character
            if (maze[q][i] == "."):   # if it is the starting character "."
                endpos = (q, i)     # update startpos
                break
            i += 1
        if (endpos != (-1, -1)):    # we're done here
            break
        q += 1
        
    if (debug == 1):        
        print(endpos)
        
    return endpos
