# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 16:03:19 2018

@author: jkell
"""

# commence search with depth first
import os

def loadmaze(filename):
    if not (os.path.exists(filename) and os.path.isfile(filename)):
        print("File not found!")
    try:
        file = open(filename)
        
    except:
        print("File not found or accessible.")
        raise
    else:
        maze = []
        for line in file:
            maze.append(line)
            
        file.close()
    
        return maze

medium = loadmaze("mediumMaze.txt")
    