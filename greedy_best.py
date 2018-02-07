#Implementation of greedy best first search, with Manhattan's distance as heuristic.
#PriorityQueue data structure used. 



import include as inc
from queue import PriorityQueue





def GBFS(maze, startNode, endNode):
    """ Searching for a path using GBFS
    Args:
        maze(list): list of node objects
        startNode(Node)
        endNode(Node)
        
    Returns:
        step(int): number of expand steps to find a path from 'P' to '.'
    """
    
    #priority queue to store expanded nodes. 
    dataQ = PriorityQueue()


    
    firstEntry = (inc.heuristic(startNode, endNode), startNode)
    dataQ.put(firstEntry)
    
    #Initialize cost value
    startNode.cost = 0

    #Counter for number of expanded nodes
    numNodesVisited = 0

    while (dataQ.empty() == False): 
       
        curNode = dataQ.get(False)[1] #tuple with (priority #, node). False argument means we don't wait if queue is empty (it throws an exception)
        
        numNodesVisited = numNodesVisited + 1
    
        if  curNode == endNode: #if current node is goal
            return numNodesVisited
        else:
            neighborNodes = curNode.find_children(maze)
           
            for neighborNode in neighborNodes:
                if neighborNode.beenthere == 0:
                    
                    neighborNode.previousNode = curNode #set the path we took to get here (i.e. node we came from)

                    dataToAdd = (inc.heuristic(neighborNode, endNode), neighborNode)
                    dataQ.put(dataToAdd) #add neighbor
                    neighborNode.beenthere = 1 #mark node as visited
        
                    neighborNode.cost = neighborNode.previousNode.cost + 1 #update cost. 
                    
  
    return numNodesVisited
   


    

  

