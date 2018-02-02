# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 16:03:19 2018

@author: jkell
"""

# commence search with depth first

def DFS(maze, startNode):
    """ Find the first working path using depth-first search

    Args:
        maze(list): list of node objects
        startNode(Node)
    Returns:
        step(int): number of steps of the found path from 'P' to '.'
    """
    found_solution=0
    
    # Initialize cost value
    startNode.cost = 0
    
    current = startNode

    # Count the number of expand step
    step = 0

    # begin expanding nodes, starting with the start node
    
    children = current.find_children(maze)
    while True:
        while (children != None):
            # investigate children
            current.beenthere = 1
            step+=1
            if current.value == ".":
                found_solution=1
                break
            found_child = 0
            for i in range(0,len(children)):
                # check to see if there are unvisited children
                child = children[i]
                if child.beenthere == 0:
                    found_child = 1
                    break
            if (found_child == 0):
                # we've visited all children. nothing more to see here
                break
            child.previousNode = current        # so we can trace back later
            child.cost = child.previousNode.cost + 1
            current = child
            children = current.find_children(maze)
        if (found_solution == 1):
            break
        elif current.value != "P":           # check to see we haven't climbed all the way up the tree yet
            current = current.previousNode
            children = current.find_children(maze)
        else:    # this shouldn't happen, but just in case we find no solution
            break
            
    return step
            
        
