# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 20:16:40 2018

@author: jkell
"""

#Code outline:
#Boxes should be their own data structure
#Store whether the boxes are in a valid position (B)
#Store all boxes in puzzle in an array
#Heuristic (tentative): dist. to nearest displaced box + dist. to box after that
#or maybe dist. to nearest displaced box + dist. to nearest storage space

#State of world: your position(prob. just current node), the array of boxes.
#Transition from your position (pos, 8 displaced boxes) to (newpos, 7 displaced boxes) etc.


