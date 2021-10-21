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
    dict["max"] = np.max(array)
    dict["min"] = np.min(array)
    dict["median"] = np.median(array)
    return dict

    
### Exercise 1, Task 4:
# Comment: In this exercise you should use matplotlib to visualize some
# data. You will only need the "hist" function contained in the pyplot 
# module of matplotlib, but if you are interested, you may want to read
# https://realpython.com/python-matplotlib-guide/
def histogram(array: np.array, bins: Optional[int] = 10):
    plt.hist(x=array,bins=bins)
    #plt.show()
    
    
### Exercise 1, Task 5:
def list_ends(original_list: Union[List, np.array]) -> List:
    if type(original_list) == List:
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

    if(matrix_a.shape[-1] != matrix_b.shape[0]):
        raise AttributeError('Matrix shape are different. First shape is {} and second shape is {}'.format(matrix_a.shape,matrix_b.shape))
    return np.multiply(matrix_a,matrix_b)

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
    
    def __init__(self):
        """
            A constructor where instance attributes can be setup.
        """
        raise NotImplementedError("TODO Contructor")
        
    def add_node(self, node: str):
        """
            Adds a node with the given name to the graph. 
            
            Parameters
            ----------
            node: String
                The name of the new node.
        """
        raise NotImplementedError("TODO add_node")
        
    def remove_node(self, node: str):
        """
            Removes the node with the given name from the graph.
            Should raise an Exception when the given node is not
            in the graph.
            
            Parameters
            ----------
            node: String
                The name of the node to be removed.
        """
        raise NotImplementedError("TODO remove_node")
        
    def add_edge(self, node_a: str, node_b: str):
        """
            Adds a directed edge from node_a to node_b. 
            
            Parameters
            ----------
            node_a: String
                The name of the first node.
            node_b: String
                The name of the second node.
        """
        raise NotImplementedError("TODO add_edge")
            
    def remove_edge(self, node_a: str, node_b: str):
        """
            Removes an edge from node_a to node_b, if it exists. 
            Non-existing edges are ignored.
            
            Parameters
            ----------
            node_a: String
                The name of the first node.
            node_b: String
                The name of the second node.
        """
        raise NotImplementedError("TODO remove_edge")
            

    # Comment for porperties: Properties are the preferred way of not using explicit
    # get_x / set_x methods from other languages. We can discuss how exactly
    # they work in the tutorials, or you can read up on the reasoning behind them
    # at https://www.python-course.eu/python3_properties.php
    def get_number_of_nodes(self) -> int:
        """
            Returns
            -------
            int
                The total number of nodes in the graph.
        """
        raise NotImplementedError("TODO get_number_of_nodes")
    
    def get_parents(self, node: str) -> List[str]:
        """
            Collects and returns all parents of the given node. Should raise an
            exception when the node is not in the graph.

            Parameters
            ----------
            node: String
                The name of the node whose parents are queried.
                
            Returns
            -------
            list
                A list containing all parent nodes of the specified node.
        """
        raise NotImplementedError("TODO get_parents")
            
    def get_children(self, node: str) -> List[str]:
        """
            Collects and returns all children of the given node. Should raise
            an exception when the node is not in the graph.

            Parameters
            ----------
            node: String
                The name of the node whose children are queried.
                
            Returns
            -------
            list
                A list containing all children nodes of the specified node.
        """
        raise NotImplementedError("TODO get_children")

    def is_ancestor(self, node_a: str, node_b: str) -> bool:
        """
            Checks if node_a is an ancestor of node_b. 
            Should also work in cyclic graphs!

            Parameters
            ----------
            node_a: String
                The name of the potential ancestor node.
            node_b: String
                The name of the potential descendant node.

            Returns
            -------
            bool
                True if node_a is an ancestor of node_b, False otherwise.
        """
        raise NotImplementedError("TODO is_ancestor")

    def is_descendant(self, node_a: str, node_b: str) -> bool:
        """
            Checks if node_a is a descendant of node_b. 
            Should also work in cyclic graphs!

            Parameters
            ----------
            node_a: String
                The name of the potential descendant node.
            node_b: String
                The name of the potential ancestor node.

            Returns
            -------
            bool
                True if node_a is a descendant of node_b, False otherwise.
        """
        raise NotImplementedError("TODO is_descendant")

    def is_acyclic(self) -> bool:
        """
            Computes whether or not this graph is acyclic.
        
            Returns
            ----------
            bool
                True if there are no cycles within the provided graph, False otherwise.
        """
        raise NotImplementedError("TODO is_acyclic")

if __name__ == "__main__":
    # Comment: This condition will evaluate to true, if this
    # module is run directly, i.e. using "python assignment1.py".
    # You will find some simple example calls for the different functions,
    # which you may uncomment and extend to test your implementations.
    
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
    # graph = DGraph()
    # graph.add_node("node_a")
    # graph.add_node("node_b")
    # graph.add_node("node_c")
    # graph.remove_node("node_b")
    # graph.add_edge("node_a", "node_c")
    # print("Number of nodes: {}".format(graph.get_number_of_nodes()))
    # print("Number of nodes (properties): {}".format(graph.num_nodes))
    # print("Parents of node_c: {}".format(graph.get_parents("node_c")))
    # print("Is node_c a descendant of node_a? {}".format(graph.is_descendant("node_c","node_a")))
    # print("Is acyclic? {}".format(graph.is_acyclic))

    