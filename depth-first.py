# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 16:03:19 2018

@author: jkell
"""

# commence search with depth first
import include_node_version as inc

found_solution=0

def go_to_child(current, step = 0):
    """ Expand the selected node and visit each of its children recursively.
        Stop if the goal is found.

    Args:
        current (Node)
        step (int) : the total number of nodes visited so far
    Returns:
        step(int): number of steps of the found path from 'P' to '.'
    """
    global found_solution
    current.beenthere = 1
    step+=1
    
    #print("coords:", current.x, current.y)

    # Terminating conditions
    if current.value == ".":
        found_solution=1
        return step
    
    children = current.find_children(maze)
    
    # investigate the next steps
    for child in children:
        # if we haven't visited this node yet, let's check it out
        if (child.beenthere == 0):
            child.previousNode = current        # so we can trace back later
            child.cost = child.previousNode.cost + 1
            step = go_to_child(child, step)     # recursive!
            if (found_solution == 1):
                break
        
    return step

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
            current.beenthere = 1
            step+=1
            if current.value == ".":
                found_solution=1
                break
            found_child = 0
            for i in range(0,len(children)):
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
    step = DFS(maze, startNode)

    # Print
    print('original maze:')
    inc.printmaze(maze)
    print('\nsolved maze:')
    inc.traceback(maze, endNode)

    # Output
    print('\nnumber of nodes visited in total: {0}'.format(step))
    print('cost of path found: {0}'.format(endNode.cost))