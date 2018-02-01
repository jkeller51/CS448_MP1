# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 16:03:19 2018

@author: jkell
"""

# commence search with depth first
import include_node_version as inc

found_solution=0

def go_to_child(current, step = 0):
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
        if (child.beenthere == 0):
            child.previousNode = current
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

    # Count the number of expand step
    step = 0

    step = go_to_child(startNode)
    
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