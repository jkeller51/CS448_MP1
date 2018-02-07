# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 15:39:09 2018

@author: jkell
"""

import include as inc
import depth_first as DF
import breadth_first as BF
import greedy_best as GB
import astar as AS

if __name__ == '__main__':
    search_index = input('Please enter a number to choose a search algorithm:\n'
                         '1. Depth-first\n'
                         '2. Breadth-first\n'
                         '3. Greedy best-first\n'
                         '4. A*\n')
    
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
    if (search_index == '1'):
        step = DF.DFS(maze, startNode)
    elif (search_index == '2'):
        step = BF.BFS(maze, startNode, endNode)
    elif (search_index == '3'):
        step = GB.GBFS(maze, startNode, endNode)
    elif (search_index == '4'):
        step = AS.Search(maze, startNode, endNode)

    # Print
    print('original maze:')
    inc.printmaze(maze)
    print('\nsolved maze:')
    inc.traceback(maze, endNode)

    # Output
    print('\nnumber of nodes visited in total: {0}'.format(step))
    print('cost of path found: {0}'.format(endNode.cost))
