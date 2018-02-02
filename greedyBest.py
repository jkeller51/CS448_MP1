#Implementation of greedy best first search
#Use a heuristic function to determine most promising node and expand accordingly.
#Use priority queue data structure
#Heuristic to use is Manhattan's distance.


import include_node_version as inc
from queue import PriorityQueue





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


    dataQ = PriorityQueue()


    firstEntry = (startNode, inc.heuristic(startNode, endNode))
    dataQ.put(firstEntry)


    while (!dataQ.empty()): #while the queue is not empty.
        curEntry = dataQ.get() #tuple with node, number
        if  curEntry[0] == endNode: #if the current node is the goal
            #done
            continue
        else:
            neighborNodes = curEntry[0].find_children(maze)
            for neighborNode in neighborNodes:
                if neighborNode.beenthere == 0:
                    dataToAdd = (neighborNode, inc.heuristic(neighborNode, endNode))
                    dataQ.put(dataToAdd) #add neighbor
                
   

    
    
 
