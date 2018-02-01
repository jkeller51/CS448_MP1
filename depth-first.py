# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 16:03:19 2018

@author: jkell
"""

# commence search with depth first
import queue
import include_node_version as inc

def DFS(maze, startNode):
    """ Find the first working path using depth-first search

    Args:
        maze(list): list of node objects
        startNode(Node)
    Returns:
        step(int): number of steps of the found path from 'P' to '.'
    """
    
    # Initialize fontier queue
    unvisited = queue.Queue()
    unvisited.put(startNode)
    
    # Initialize cost value
    startNode.cost = 0

    # Count the number of expand step
    step = 0
    
    while not unvisited.empty():
        current = unvisited.get()
        current.beenthere = 1
        step += 1

        # Terminating conditions
        if current.value == ".":
            break
        
        