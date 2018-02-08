# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 12:35:37 2018

@author: HaokunLi1994
"""

import queue
import operator
import time
import networkx as nx
import include as inc
import depth_first as DF
import breadth_first as BF
import astar as AS


class PathState(object):
    """ To define a state. """
    def __init__(self, path):
        self.path = frozenset(path)
        self.node = None

        if len(path) > 0:
            self.node = path[-1]

    def __hash__(self):
        """ Hash function """
        return hash((self.path, self.node))


def generate_graph(distance_dict, endList):
    """ Generate a vertex graph using networkx

    Args:
        distance_dict(dict): the dict returned by pre-computing
        endList(list): list of tuples, each of which marking a dot
    Returns:
        G(nx.Graph)
    """
    G = nx.Graph()

    # Add nodes
    G.add_nodes_from(endList)

    # Add edges
    for u in endList:
        mylist = distance_dict[u]
        for mytuple in mylist:
            node = mytuple[2]
            d = mytuple[0]
            v = (node.x, node.y)
            G.add_edge(u, v, weight=d)
    
    return G


def modify_graph(G, path):
    """ Remove all nodes in path from G

    Args:
        G(nx.Graph): original vertex graph
        path(list): current path, list of nodes
    Returns:
        new_G(nx.Graph)
    """
    new_G = G.copy()

    for node in path:
        coordinate = (node.x, node.y)
        new_G.remove_node(coordinate)
    return new_G


def mst_heuristic(G, path):
    """ Heuristic using mst

    Args:
        G(nx.Graph): original vertex graph
        path(list): current path, list of nodes
    Returns:
        new_G(nx.Graph)
    """
    new_G = modify_graph(G, path)
    estimate = 0
    T = nx.minimum_spanning_tree(new_G, weight='weight')

    for temp in T.edges(data=True):
        estimate += temp[2]['weight']

    return estimate


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

    # Vertex graph
    G = generate_graph(distance_dict, endList)

    # State dict
    state_dict = dict()
    
    # Initialize path
    path = []
    state_dict.update({PathState(path): 0})

    # Initialize path cost
    current_path_cost = 0
    step = 0
    
    # Initialize priority queue
    frontier = queue.PriorityQueue()

    # Initialize current node
    current = startNode

    # Main loop
    while len(path) < n:
        # Check repeated states
        state = PathState(path)
        if state not in state_dict:
            state_dict.update({state: current_path_cost})
        else:
            path_tuple = frontier.get()
            path = path_tuple[2].copy()
            current_path_cost = path_tuple[1]
            current = path[-1]
            continue
        
        # Update priority queue
        myList = distance_dict[(current.x, current.y)].copy()
        for food_tuple in myList:
            food = food_tuple[2]
            if food not in path:
                cost = food_tuple[0] + current_path_cost
                new_path = path.copy()
                new_path.append(food)
                estimate = mst_heuristic(G, new_path)
                f_cost = cost + estimate
                frontier.put((f_cost, cost, new_path))

        # Update path and path cost
        path_tuple = frontier.get()
        path = path_tuple[2].copy()
        current_path_cost = path_tuple[1]
        current = path[-1]
        step += 1

    # Check optimality
    while True:
        path_tuple = frontier.get()
        if path_tuple[0] > current_path_cost:
            break
        else:
            temp_path = path_tuple[2]
            temp_cost = path_tuple[1]
            temp_current = temp_path[-1]
            if len(temp_path) == n:
                if temp_cost >= current_path_cost:
                    continue
                else:
                    path = temp_path
                    current_path_cost = temp_cost
                    current = temp_current
                step += 1
            else:
                myList = distance_dict[(temp_current.x, temp_current.y)].copy()
                for food_tuple in myList:
                    food = food_tuple[2]
                    if food not in temp_path:
                        cost = food_tuple[0] + temp_cost
                        new_path = temp_path.copy()
                        new_path.append(food)
                        estimate = mst_heuristic(G, new_path)
                        f_cost = cost + estimate
                        frontier.put((f_cost, cost, new_path))
            

    # Mark the order of food found
    mark_list = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in range(n):
        path[i].value = mark_list[i]

    # Print maze
    inc.printmaze(maze)

    return current_path_cost, step


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

    # Search, return cost and step
    cost, step = multiple_dots(maze, startNode, endList)
    endTime = time.time()

    print('\nCost: {0}'.format(cost))
    print('Expanded nodes: {0}'.format(step))
    print('Time used: {:.4f} min(s)'.format((endTime - startTime) / 60.0))
    
