# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 16:35:11 2018

@author: jkell, HaokunLi1994
"""

import os


# Indicating ON/OFF of debugging mode
debug = 1


class Node(object):
    """ Using coordinates (x, y) to mark the position
    of this node.

    Args:
        x(int):x-th line of the maze
        y(int):y-th position in that line of the maze
        char(string):character of a particular node
    """
    # Indicating whether or not the node has been visited
    beenthere = 0

    # Indicating whether the node is part of 'wall'
    wall = 0

    # Parent node
    previousNode = None
    
    def __init__(self, x, y, char):
        self.x = x
        self.y = y
        self.value = char
        self.cost = None
        self.evaluation = None

        if char == "%":
            self.wall = 1

        pass

    def find_children(self, maze):
        """ Find all children nodes of a particular node

        Args:
            maze(list):list of Node objects
        Returns:
            children(list):list of children in Node objects
        """
        children = []
        width = len(maze[0])
        height = len(maze)
        
        # up next
        if self.x  > 0:
            child = maze[self.x - 1][self.y]
            if (child.wall == 0) and (child.value != "P"):
                children.append(child)
            
        # left next
        if self.y  > 0:
            child = maze[self.x][self.y - 1]
            if (child.wall == 0) and (child.value != "P"):
                children.append(child)
            
        # right next
        if self.y + 1  < width:
            child = maze[self.x][self.y + 1]
            if (child.wall == 0) and (child.value != "P"):
                children.append(child)
            
        # bottom next
        if self.x + 1 < height:
            child = maze[self.x + 1][self.y]
            if (child.wall == 0) and (child.value != "P"):
                children.append(child)

        return children

    def set_previous_node(self, node):
        """ Set parent node for current node.

        Args:
            node(Node): current node
        Returns:
            (None)
        """
        self.previousNode = node
        pass

    def __eq__(self, other):
        """
        Override default equals behavior. 2 nodes are equal if and only if
        the two nodes have the same location (i.e. same x and y coordinates)
        """
        if (self.x == other.x) and (self.y == other.y):
            return True
        else:
            return False

    def __lt__(self, other):
        """
         Determine if one node is less than the other
        """
        if (self.x + self.y) < (other.x + other.y):
            return True
        return False



def loadmaze(filename):
    """ Load maze into memory

    Args:
        filename(str):path to a maze file, eg. 'openmaze.txt'
    Returns:
        maze(list):list of Node objects
    """
    myfile = open(filename)
    maze = []
    x = 0
    for line in myfile:
        row = []
        y = 0
        for char in line:
            if char == "\n":
                continue

            row.append(Node(x, y, char))
            y += 1

        maze.append(row)
        x += 1

    myfile.close()
    
    return maze


def printmaze(maze):
    """ Printing function for mazes

    Args:
        maze(list):list of Node objects
    Returns:
        (None)
    """
    out = []
    for line in maze:
        row = []
        for char in line:
            row.append(char.value)
        out.append(row)

    for line in out:
        print(''.join(line))

    pass


def find_start(maze):
    """ Find starting point of a maze

    Args:
        maze(list):list of Node objects
    Returns:
        startpos(tuple):(x, y) coordinates of starting point
    """
    for line in maze:
        for char in line:
            if char.value == "P":
                startpos = (char.x, char.y)

                if (debug == 1):
                    print(startpos)
                    
                return startpos


def find_end(maze):
    """ Find ending point of a maze

    Args:
        maze(list):list of Node objects
    Returns:
        endpos(tuple):(x, y) coordinates of ending point
    """
    for line in maze:
        for char in line:
            if char.value == ".":
                endpos = (char.x, char.y)

                if (debug == 1):
                    print(endpos)
                    
                return endpos


def traceback(maze, endNode):
    """ Mark the found path from 'P' to '.' with '+'

    Args;
        endNode(node): ending point of the maze
    Returns:
        (None)
    """
    current = endNode
    previous = current.previousNode

    while previous.value != "P":
        previous.value = "+"
        current = previous
        previous = current.previousNode

    printmaze(maze)
    pass





def heuristic(cur, goal):
    """
      Heuristic based on the manhattan distance between the current point and the goal position.
      Used for best first search      
    """
    distance = abs(cur.x - goal.x) + abs(cur.y - goal.y)
    return distance
    
