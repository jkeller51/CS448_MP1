#!usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 15:41:28 2018

@author: HaokunLi1994
"""


import queue

def BFS(maze, startNode, endNode):
    """ Searching for a path using BFS

    Args:
        maze(list): list of node objects
        startNode(Node)
        endNode(Node)
    Returns:
        step(int): number of expand steps to find a path from 'P' to '.'
    """
    # Initialize fontier queue
    unvisited = queue.Queue()
    unvisited.put(startNode)

    # Innitialize cost value
    startNode.cost = 0

    # Count the number of expand step
    step = 0

    while not unvisited.empty():
        current = unvisited.get()
        current.beenthere = 1
        step += 1

        # Terminating conditions
        if current == endNode:
            break

        # Update searching frontier
        children = current.find_children(maze)
        for child in children:

            # The node is unvisited and it is not in
            # the queue of unvisited nodes
            if (child.beenthere == 0) and (child not in unvisited.queue):
                child.previousNode = current
                unvisited.put(child)
                child.cost = child.previousNode.cost + 1

    return step

