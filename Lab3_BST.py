# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 20:55:43 2019
CS 2302 - Andres Silva
> Teacher: Olac Fuentes
> TAs: Anindita Nath  & Maliheh Zargaran
> Lab #3
> The purpose of this lab is to work with binary search trees and their structure. Mainly, the navigation
of them using recursion and iteration.
> LAST MODIFIED: MARCH 8th, 2019
"""

# Code to implement a binary search tree 
# Programmed by Olac Fuentes
# Last modified February 27, 2019
import matplotlib.pyplot as plt
import numpy as np
import math 
import time


class BST(object):
    # Constructor
    def __init__(self, item, left=None, right=None):  
        self.item = item
        self.left = left 
        self.right = right      
        
def Insert(T,newItem):
    if T == None:
        T =  BST(newItem)
    elif T.item > newItem:
        T.left = Insert(T.left,newItem)
    else:
        T.right = Insert(T.right,newItem)
    return T

def Delete(T,del_item):
    if T is not None:
        if del_item < T.item:
            T.left = Delete(T.left,del_item)
        elif del_item > T.item:
            T.right = Delete(T.right,del_item)
        else:  # del_item == T.item
            if T.left is None and T.right is None: # T is a leaf, just remove it
                T = None
            elif T.left is None: # T has one child, replace it by existing child
                T = T.right
            elif T.right is None:
                T = T.left    
            else: # T has two chldren. Replace T by its successor, delete successor
                m = Smallest(T.right)
                T.item = m.item
                T.right = Delete(T.right,m.item)
    return T
         
def InOrder(T):
    # Prints items in BST in ascending order
    if T is not None:
        InOrder(T.left)
        print(T.item,end = ' ')
        InOrder(T.right)
  
def InOrderD(T,space):
    # Prints items and structure of BST
    if T is not None:
        InOrderD(T.right,space+'   ')
        print(space,T.item)
        InOrderD(T.left,space+'   ')
  
def SmallestL(T):
    # Returns smallest item in BST. Returns None if T is None
    if T is None:
        return None
    while T.left is not None:
        T = T.left
    return T   
 
def Smallest(T):
    # Returns smallest item in BST. Error if T is None
    if T.left is None:
        return T
    else:
        return Smallest(T.left)

def Largest(T):
    if T.right is None:
        return T
    else:
        return Largest(T.right)   

def Find(T,k):
    # Returns the address of k in BST, or None if k is not in the tree
    if T is None or T.item == k:
        return T
    if T.item < k:
        return Find(T.right,k)
    return Find(T.left,k)
    
def FindAndPrint(T,k):
    f = Find(T,k)
    if f is not None:
        print(f.item,'found')
    else:
        print(k,'not found')
        
def PrintStructure(T,space):
    if T is not None:
        print(space,T.item)
        PrintStructure(T.right,space+'  ')
        PrintStructure(T.left,space[:-2])

def IterativeSearch(T,k):
    t = T 
    while(t is not None): #Move through tree until finding k or reaching the end.
        if k == t.item:# If k is found, return the reference to current node.
            return t
        else:
            if (k > t.item): #If k is greater than current node, move right.
                t = t.right
            else:
                t = t.left #Else, move left.
    return None #Exiting loop means k was not found, return None as reference.


def lines(ax,center,p): #Plots 1 line between 2 given points (modifes the center for neatness) 
    if p != None:    
        ax.plot([center[0] ,p[0]],[center[1] - 100,p[1] + 300] ,color='k')#Center and P1
        


def circle(center,rad): #Model code stays unmodified, it just traces a circle with a center and a radius.
    n = int(4*rad*math.pi)
    t = np.linspace(0,6.3,n)
    x = center[0]+rad*np.sin(t)
    y = center[1]+rad*np.cos(t)
    return x,y

def draw_trees(ax,T,center,segment_height,segment_width): 
    p1 =[center[0] - segment_width/4 ,center[1] - segment_height] #The two children points are calculated and stored in point 1 (p1) and point 2 (p2).
    p2 =[center[0] + segment_width/4 ,center[1] - segment_height]
    
    if T != None:#Only draw when node exist.
        x,y = circle([center[0], center[1] + 100],200) #Root Circle
        ax.plot(x,y,color='k') #Plot the circle.
        
        ax.text(center[0] - 120, center[1]  , T.item, fontsize=10) #Print item of node 

        
        if T.left != None: #Draw line to left child only if left child exists.
            lines(ax,center,p1)

            
        if T.right != None: #Draw line to right child only if left child exists.
            lines(ax,center,p2)


        draw_trees(ax,T.left,p1,segment_height,segment_width/2) #Repeat using left node as root.
        draw_trees(ax,T.right,p2,segment_height,segment_width/2)

def Extract(T):
    if T is None: #return empty list when T is none.
        return []
   
#    elif T.left == None and T.right == None: This is reduntant, but helps to understand.
#        L = [T.item]
#        return L
    
    else:
        List = Extract(T.left) +  [T.item] + Extract(T.right) #Concatenate the left child, the current node, and the right child.
        return List #return glued list.
    

def BuildBST(L): 
    if len(L) < 1: #If L is empty
        return None
    if len(L) == 1: #If L has 1 element, make a node with that element and return it.
        T = BST(L[0]) #Make a node with it, and return it.
        return T
    else:
       T = BST(L[len(L)//2]) #Make the root the middle element
       T.left = BuildBST(L[   :(len(L)//2)]) #Make the left child with the list from 0 to middle (exclusive)
       T.right = BuildBST(L[(len(L)//2) + 1 :  ]) #Make the right from middle + 1 (exlcuding root) to end of list.
       return T #Return 'glued tree'.
        
    

def PrintLevel(T,d):
    if T == None: 
        return
    if d == 0: #If at root level, print root.
        print(T.item, end=' ')
    elif d > 0: #Keep going and decrease d down to desired level to print
        PrintLevel(T.left, d-1)
        PrintLevel(T.right, d-1)
   
def GetHeight(T):
    if T == None: #At a none node, add 0 to our sum.
        return 0
    else:
        left = GetHeight(T.left) #Get height of left and right subtree.
        right = GetHeight(T.right)
    if right > left: #add 1 to the largest subtree and return int.
        return 1 + right
    else:
        return 1 + left
    
def PrintByDepth(T):
    HeightOfTree = GetHeight(T)#Get Height of tree
    
    for i in range(HeightOfTree): #Print all levels of the tree.
       print("Keys at depth ",i,": ",end= ' ')
       PrintLevel(T,i)
       print("\n")
    
    


# Code to test the functions above
T = None

#A = [70, 50, 90, 130, 150, 40, 10, 30, 100, 180, 45, 60, 140, 42]
A = [10,4,15,2,8,1,3,5,9,7,12,18]
#A = [0,1,2,3,4,5,6,7,8,9]
#A = []

#Build Tree with list A.
for a in A:
    T = Insert(T,a)
 
    

    



#################################################################
#################################################################
### METHOD TESTING ##############################################

print("List A = ", A)


print("#############################################################")
print("\n1)Print tree")
plt.close("all")
fig, ax = plt.subplots()#Call method below this line.

start = time.time()
draw_trees(ax,T,[0,0],1000,5000) 
end = time.time()
print(end - start)

ax.set_aspect(1.0) #And before this one .
ax.axis('off')
plt.show()

print("#############################################################")
print("\n2)Compare given 'Find' vs IterativeSearch.")
print("Find(T,7)           : ",Find(T,7))

start = time.time()
print("IterativeSearch(T,7): ", IterativeSearch(T,7))
end = time.time()
print(end - start)

print("#############################################################")
print("\n3)Build Tree using sorted list.")
print('\n')
SortedList = A
print("Sorted List: ",SortedList)
print("\nBST = BuildBST(SortedList)")

start = time.time()
BST1 = BuildBST(SortedList)
end = time.time()
print(end - start)

print("Printing BST using InOrderD(BST, '')\n")
InOrderD(BST1, '')

print("#############################################################")
print("\n4)Extract elements from BST to a sorted List.")
print("\nNewList = Extract(BST)")

start = time.time()
NewList = Extract(BST1)
end = time.time()
print(end - start)

print("Extracted List : ", NewList)

print("#############################################################")
print("\n5)Print by depth.")
print("\nCalling PrintByDepth(T)\n") #First list created

start = time.time()
PrintByDepth(T)
end = time.time()
print(end - start)










   


        
    
    



    
    
    
    
    
    
    
