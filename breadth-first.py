#!usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 15:41:28 2018

@author: HaokunLi1994
"""


import queue
import include_node_version as inc


def BFS(maze, startNode):
    """ Searching for a path using BFS

    Args:
        maze(list): list of node objects
        startNode(Node)
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
        if current.value == ".":
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


if __name__ == '__main__':
    mydict = {'1':'mediumMaze.txt',
              '2':'bigMaze.txt',
              '3':'openmaze.txt'}

    maze_index = input('Please enter a number to choose a maze:\n'
                       '1. medium\n'
                       '2. big\n'
                       '3. open\n')
    
    # Initialize maze
    maze = inc.loadmaze(mydict[maze_index])

    # Find startNode
    start_x, start_y = inc.find_start(maze)
    startNode = maze[start_x][start_y]

    # Find endNode
    end_x, end_y = inc.find_end(maze)
    endNode = maze[end_x][end_y]

    # Number of steps
    step = BFS(maze, startNode)

    # Print
    print('original maze:')
    inc.printmaze(maze)
    print('\nsolved maze:')
    inc.traceback(maze, endNode)

    # Output
    print('\nnumber of nodes visited in total: {0}'.format(step))
    print('cost of path found: {0}'.format(endNode.cost))
