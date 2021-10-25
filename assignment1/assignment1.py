#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 17:13:29 2021

@author: jpoeppel

Modified by: <Your group members here>
"""


# REMINDER: Only Python3 compatible code will be accepted!

# Some imports you may want or need to use.
# I will discuss differnet types of imports in the tutorial,
# but you can also learn more about imports in python you may want
# to read https://www.digitalocean.com/community/tutorials/how-to-import-modules-in-python-3
# or the official documentation at https://docs.python.org/3/reference/import.html

# A simple direct import of a module
import math
# Importing a module and renaming it for easier use
import numpy as np
# Importing a submodule and renaming it
import matplotlib.pyplot as plt

# Python3 supports type hints for the developer
# In order to express more complex types some additional imports
# are needed
from typing import Union, Optional, List, Tuple, Dict
import copy

### Exercise 1, Task 1:
# Comment: This is a function header in Python.
# All functions are defined using the keyword "def",
# followed by the function name and () with any potential
# parameters. Function headers can now also have type signatures.
# If the function is to return a value, you need to
# specifc this using "return <val>"
def fibonacci(n: int) -> int:
    if n < 0:
        return 0
    elif n >=0 and n <=1:
        return n
    else:
        return fibonacci(n-1)+fibonacci(n-2)


### Exercise 1, Task 2:
# Comment: In this function header, we have 2 different kinds of 
# parameters: positional and namend ones. Named parameters are optional
# and have default values. Positional parameters are required when calling
# a function.
# For more information on parameters, you may want to read: 
# https://www.pythoncentral.io/fun-with-python-function-parameters/
# Also, this exercise will require you to use numpy, a powerful package
# primarily for n-dimensional arrays, which we will make use of later.
# You will not need to learn everything about it, but for those interested,
# I recommend reading https://numpy.org/devdocs/user/index.html
def random_array(size: Union[int, Tuple[int, ...]], 
                min_val: Optional[float] = 0, 
                max_val: Optional[float] = 1) -> np.array: 
                
    vect = np.random.randint(min_val,max_val,size)
    return vect

### Exercise 1, Task 3:
# Comment: Remember to do both parts of the task!
def analyze(array: Union[List, np.array]) -> Dict:
    dict = {}
    dict["mean"] = np.mean(array)
    dict["maximum"] = np.max(array)
    dict["minimum"] = np.min(array)
    dict["median"] = np.median(array)
    return dict

    
### Exercise 1, Task 4:
# Comment: In this exercise you should use matplotlib to visualize some
# data. You will only need the "hist" function contained in the pyplot 
# module of matplotlib, but if you are interested, you may want to read
# https://realpython.com/python-matplotlib-guide/
def histogram(array: np.array, bins: Optional[int] = 10):
    plt.hist(x=array,bins=bins)
    plt.savefig("plot.png")
    plt.show()
    
    
### Exercise 1, Task 5:
def list_ends(original_list: Union[List, np.array]) -> List:
    if type(original_list) != np.array:
        return [original_list[0],original_list[-1]]
    elif original_list.ndim > 1:
        return [original_list[:,0],original_list[:,-1]]
    else:
        return [original_list[0],original_list[-1]]
    

### Exercise 1, Task 6:
def combine_dictionaries(dict_a: Dict, dict_b: Dict) -> Dict:
    
    return {k: dict_a.get(k, 0) + dict_b.get(k, 0) for k in set(dict_a) | set(dict_b)}

### Exercise 1, Task 7:
# In this exercise you should raise an Exception if its arguments
# do not have the proper shapes. Look at how the skeleton functions
# are already raising NotImplementedError exceptions as a hint.
# A good read on exceptions in Python can be found at: 
# https://realpython.com/python-exceptions/
def matrix_mul(matrix_a: np.array, matrix_b: np.array) -> np.array:
    if matrix_a.ndim > 2 or matrix_b.ndim > 2:
        raise AttributeError('Matrix are bigger then 2 dimensios. First dim is {} and second dim is {}'.format(matrix_a.ndim,matrix_b.ndim))
    if(matrix_a.shape[-1] != matrix_b.shape[0]):
        raise AttributeError('Matrix shape are different. First shape is {} and second shape is {}'.format(matrix_a.shape,matrix_b.shape))
    
    return np.matmul(matrix_a,matrix_b)


### Exercise 2
# In this exercise you are asked to write complete the class skeleton
# for the Graph class below. If you are interested in more information
# about classes, you may want to read: https://docs.python.org/3/tutorial/classes.html
# or play around with https://www.learnpython.org/en/Classes_and_Objects
# Keep in mind, that the way you solve these tasks is up to you, you may
# add additional functions to the class or even create your own classes, e.g.
# for nodes. For this reason, the docstrings will only focus on any input/
# output requirements and make no comments about what the functions may do 
# internally.

# A class is defined by the keyword "class" followed by the name of the class
# (conventionally written with a capital initial letter) and finally followed
# by a list of classes this class should inherit from. While no longer necessary
# in Python3, traditionally one specified to inherit from "object". In Python3
# all classes will inherit from object, regardless of whether one specifies this 
# or not. I've added this here, so that you are not confused when you see it while
# reading up on Python since a lot of material is still tailored to at least be compatible
# to Python2 where it made a difference whether or not this inheritance was specified.

# Another notable thing for classes in Python is the "self" keyword, which should always
# be the first parameter of all classmethods. Python will pass in a reference of the
# current instance to the function to use (same as "this" in Java) as the first parameter
# whenever calling a method on a class instance. I will not include this in the docstrings
# as it is always the same.
class DGraph(object):

    nodes = {}
    num_nodes = 0
    def __init__(self):
        self.nodes = {}
        self.num_nodes = self.get_number_of_nodes()

       
        
    def add_node(self, node: str):
        if node not in self.nodes.keys():
            self.nodes[node] = []
        self.num_nodes = self.get_number_of_nodes()

        
    def remove_node(self, node: str):
        if node in self.nodes.keys():
            self.nodes.pop(node)
            for node_graph in self.nodes:
                if node in node_graph:
                    node_graph.remove(node)
        self.num_nodes = self.get_number_of_nodes()



    def add_edge(self, node_a: str, node_b: str):
        if node_a in self.nodes and node_b in self.nodes:
            if node_b not in self.nodes[node_a]:
                self.nodes[node_a].append(node_b)
                
        # if not self.is_acyclic():
        #     self.remove_edge(node_a,node_b)
        #     print("Removed edge ["+node_a+"-"+node_b+"] because make graph cyclic.")
            
    def remove_edge(self, node_a: str, node_b: str):
        if node_a in self.nodes and node_b in self.nodes:
            if node_b in self.nodes[node_a]:
                self.nodes[node_a].remove(node_b)

    def get_number_of_nodes(self) -> int:
        return len(self.nodes.keys())
    
    def get_parents(self, node: str) -> List[str]:
        parents = []
        if node in self.nodes:
            for graph_node in self.nodes:
                if graph_node != node and node in self.nodes[graph_node]:
                        parents.append(graph_node)
        return parents
            
    def get_children(self, node: str) -> List[str]:
        children = []
        if node in self.nodes:
            children = self.nodes[node]
        return children

    def is_ancestor(self, node_a: str, node_b: str) -> bool:
        isAncestor = False
        if node_a not in self.nodes or node_b not in self.nodes:
            return isAncestor
            
        directParents = self.get_parents(node_b)
        if node_a in directParents:
            isAncestor = True
        else:
            for parent in directParents:
                newParent = self.get_parents(parent)
                if node_a in newParent:
                    isAncestor = True
                    break
                for newlyParent in newParent:
                    if newlyParent not in directParents:
                        directParents.append(newlyParent)

        return isAncestor

    def is_descendant(self, node_a: str, node_b: str) -> bool:
        isDescendant = False
        if node_a not in self.nodes or node_b not in self.nodes:
            return isDescendant

        directChildrens = self.get_children(node_b)
        if node_a in directChildrens:
            isDescendant = True
        else:
            for children in directChildrens:
                newChildrens = self.get_children(children)
                if node_a in newChildrens:
                    isDescendant = True
                    break
                for newlyChildren in newChildrens:
                    if newlyChildren not in directChildrens:
                        directChildrens.append(newlyChildren)

        return isDescendant

    def is_acyclic(self) -> bool:
        copy_graph = copy.deepcopy(self)
        L = []
        Q = [ node for node in self.nodes.keys() if len(self.get_parents(node)) == 0]
        while len(Q) != 0:
            n = Q.pop(0)
            L.append(n)
            for m in self.nodes[n]:
                copy_graph.remove_edge(n, m)
                if len(copy_graph.get_parents(m)) == 0:
                    Q.append(m)
        
        for node in copy_graph.nodes.values():
            if len(node) > 0:
                return False
        return True

if __name__ == "__main__":
    print("Example calls: ")

    ### Exercise 1
    # Exercise 1, Task 1:
    print("The fifth fibonacci number is: {}".format(fibonacci(9)))
    # Exercise 1, Task 2:
    array = random_array((3,3),1,4)
    print("Random array: {}".format(array))
    # Exercise 1, Task 3:
    moments = analyze(array)
    print("Stored moments: {}".format(moments))
    # Exercise 1, Task 4:
    histogram(array)
    # Exercise 1, Task 5:
    print("First and last item of list {}: {}".format(array, list_ends(array)))
    # print(combine_dictionaries({"S":19,"c":4,"f":"d"},{"S":4,"d":3,"f":"c"}))
    # Exercise 1, Task 6:
    m1 = np.eye(2)
    m2 = np.array([[2,1],[0,2]])
    res = matrix_mul(m1, m2)
    print("Result from the multiplication: {}".format(res))

    ### Exercise 2:
    graph = DGraph()
    graph.add_node("node_a")
    graph.add_node("node_b")
    graph.add_node("node_c")
    graph.remove_node("node_b")
    graph.add_edge("node_a", "node_c")
    graph.add_edge("node_c", "node_a")
    print("Number of nodes: {}".format(graph.get_number_of_nodes()))
    print("Number of nodes (properties): {}".format(graph.num_nodes))
    print("Parents of node_c: {}".format(graph.get_parents("node_c")))
    print("Is node_c a descendant of node_a? {}".format(graph.is_descendant("node_c","node_a")))
    print("Is acyclic? {}".format(graph.is_acyclic()))

    