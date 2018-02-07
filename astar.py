# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 16:05:27 2018

@author: jkell
"""

# implementation of A* search

import include as inc

debug=0
def Search(maze, startNode, endNode):
    """ A* Search

    Args:
        maze(list): list of Nodes
        startNode(Node): start point
        endNode(Node): goal node
    Returns:
        step(int): number of expanded steps
    """
    
    global debug
    # Initialize frontier queue
    unvisited = []
    unvisited.append(startNode)
    
    current = startNode
    
    startNode.cost=0
    startNode.evaluation = inc.heuristic(startNode,endNode)
    
    step = 0
    
    while len(unvisited) > 0:
        # main loop
        # we want to evaluate each node in the list
        # and see which one is best to explore
        
        if (debug == 1):
            print("Position:", "("+str(current.x)+","+str(current.y)+")" )
            print("Current frontier:")
            for i in range(0,len(unvisited)):
                print("("+str(unvisited[i].x)+","+str(unvisited[i].y)+")",":",unvisited[i].cost, unvisited[i].evaluation)
        
        current.beenthere = 1
        step+=1
        
        lowest_index = 0
        lowest_eval = 999999
        
        # Find the cheapest node on the frontier
        # in terms of evaluation function f = c+h
        for i in range(0,len(unvisited)):
            if (unvisited[i].evaluation < lowest_eval):
                lowest_index = i
                lowest_eval = unvisited[i].evaluation
                
        # we've found it, now go to it
        current = unvisited[lowest_index]
        
        # remove it from the list
        unvisited.pop(lowest_index)
        
        # we've reached the goal
        if (current.x == endNode.x) & (current.y == endNode.y):
            break
        
        # add all children to unvisited queue
        children = current.find_children(maze)
        for child in children:
            if (child.beenthere == 0) and (child not in unvisited):
                child.previousNode = current
                #unvisited.append(child)
                # insert it at the beginning to give precedence to the current "path"
                unvisited.insert(0, child)
                child.cost = child.previousNode.cost + 1
                child.evaluation = child.cost + inc.heuristic(child, endNode)
            elif (child.beenthere == 0):
                # what if we have two paths reaching the same node?
                newchild = inc.Node(child.x, child.y, child.value)
                newchild.previousNode = current
                unvisited.append(newchild)
                newchild.cost = newchild.previousNode.cost + 1
                newchild.evaluation = newchild.cost + inc.heuristic(newchild, endNode)
                
    return step
        
