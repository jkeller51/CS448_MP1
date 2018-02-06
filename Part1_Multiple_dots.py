# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 12:35:37 2018

@author: HaokunLi1994
"""

import queue
import operator
import time
import include as inc
import depth_first as DF
import breadth_first as BF
import astar as AS


def heuristic(path, distance_dict):
    """ Use the farest node as heuristic

    Args:
        path(list): current path, list of nodes
        distance_dict(dict): the dict returned by pre-computing
    Returns:
        estimate_cost(int)
    """
    curr = path[-1]
    estimate_cost = 0

    distanceList = distance_dict[(curr.x, curr.y)].copy()
    distanceList.reverse()

    for food_tuple in distanceList:
        if food_tuple[2] not in path:
            estimate_cost = food_tuple[0]
            break

    return estimate_cost


def pre_compute_distance(maze, startNode, endList):
    """ Pre-compute all pairs of nodes

    Args:
        maze(list): list of Nodes
        startNode(Node): start point
        endList(list): list of tuples, each of which marking a dot
    Returns:
        distance_dict(dict): with coordinate tuple of every node to be key;
                             and lists of distance to be values
                             {(x, y): [(cost, step, Node), ...]}
    """
    # Initialize dict of distance
    distance_dict = {}

    # Convert all tuples to Nodes
    food_list = []
    for xy in endList:
        food_x = xy[0]
        food_y = xy[1]
        food = maze[food_x][food_y]
        food_list.append(food)

    # Compute distance and update dict
    startList = food_list + [startNode]
    for start in startList:
        distanceList = []

        # Update the priority queue
        for end in food_list:
            step = AS.Search(maze, start, end)
            cost = end.cost

            # Pass the distance from a node to itself
            if cost == 0:
                continue
            
            distanceList.append((cost, step, end))
            inc.reset_all_nodes(maze)

        distanceList = sorted(distanceList, key = operator.itemgetter(0, 1))  
        distance_dict.update({(start.x, start.y):distanceList})

    return distance_dict


def multiple_dots(maze, startNode, endList):
    """ Deal with multiple dot mazes

    Args:
        maze(list): list of Nodes
        startNode(Node): start point
        endList(list): list of tuples, each of which marking a dot
    Returns:
        step(int): number of expanded steps
    """
    # Number of foods
    n = len(endList)

    # Distance dict
    distance_dict = pre_compute_distance(maze, startNode, endList)
    
    # Initialize path
    path = []

    # Initialize path cost
    current_path_cost = 0
    
    # Initialize priority queue
    frontier = queue.PriorityQueue()

    # Initialize current node
    current_tuple = (0, startNode, path)
    current = startNode

    while len(path) < n:
        # Update priority queue
        myList = distance_dict[(current.x, current.y)].copy()
        for food_tuple in myList:
            food = food_tuple[2]
            if food not in path:
                cost = food_tuple[0] + current_path_cost
                new_path = path.copy()
                new_path.append(food)
                estimate = heuristic(new_path, distance_dict)
                f_cost = cost + estimate
                frontier.put((f_cost, cost, new_path))

        # Update path and path cost
        path_tuple = frontier.get()

        path = path_tuple[2].copy()
        current_path_cost = path_tuple[1]
        current = path[-1]

    # Mark the order of food found
    mark_list = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in range(n):
        path[i].value = mark_list[i]

    # Print maze
    inc.printmaze(maze)

    return current_path_cost


if __name__ == '__main__':
    
    mydict = {'1':'tinySearch.txt',
              '2':'smallSearch.txt',
              '3':'mediumSearch.txt'}

    maze_index = input('Please enter a number to choose a maze:\n'
                       '1. tiny\n'
                       '2. small\n'
                       '3. medium\n')
    startTime = time.time()
    
    # Initialize maze
    maze = inc.loadmaze(mydict[maze_index])

    # Find start node
    s = inc.find_start(maze)
    startNode = maze[s[0]][s[1]]

    # Find end list
    endList = inc.find_end(maze)

    # Search, return cost
    cost = multiple_dots(maze, startNode, endList)
    endTime = time.time()

    print('\nCost: {0}'.format(cost))
    print('Time used: {0} min(s)'.format((endTime - startTime) / 60.0))
    
