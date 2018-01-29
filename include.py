# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 16:35:11 2018

@author: jkell
"""

import os

debug=1

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
    
def search(maze):
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