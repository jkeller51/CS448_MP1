# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 16:35:11 2018

@author: jkell
"""

import os

debug=1

class Node:
    beenthere=0
    wall=0
    previousNode=0;
    
    def __init__(self, cost, wall):
        self.cost = cost
        self.wall = wall
        
    
    

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
    q=0
    startpos=(-1,-1)
    while q<len(maze):
        i=0
        while i<len(maze[q]):       # search each character
            if (maze[q][i] == "P"):   # if it is the starting character "P"
                startpos = (q,i)     # update startpos
                break
            i+=1
        if (startpos != (-1, -1)):    # we're done here
            break
        q+=1
        
    if (debug==1):        
        print(startpos)
    
    return startpos

def find_end(maze):
    # find goal position (.)
    q=0
    endpos=(-1,-1)
    while q<len(maze):
        i=0
        while i<len(maze[q]):       # search each character
            if (maze[q][i] == "P"):   # if it is the starting character "."
                endpos = (q,i)     # update startpos
                break
            i+=1
        if (endpos != (-1, -1)):    # we're done here
            break
        q+=1
        
    if (debug==1):        
        print(endpos)
        
    return endpos
