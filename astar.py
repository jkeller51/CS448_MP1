# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 16:05:27 2018

@author: jkell
"""

# implementation of A* search

import include as inc
    

def Search(maze, startNode, endNode):
    
    # Initialize frontier queue
    unvisited = []
    unvisited.append(startNode)
    
    current = startNode
    
    startNode.cost=0
    
    step = 0
    accum = 0    # represents accumulated cost it took to get to current position
    
    while len(unvisited) > 0:
        # main loop
        # we want to evaluate each node in the list
        # and see which one is best to explore
        
        current.beenthere = 1
        
        lowest_index = 0
        lowest_eval = 999999
        for i in range(0,len(unvisited)):
            unvisited[i].evaluation = accum + inc.heuristic(unvisited[i])
            if (unvisited[i].evaluation < lowest_eval):
                lowest_index = i
                lowest_eval = unvisited[i].evaluation
        
            
            
        
        
    pass