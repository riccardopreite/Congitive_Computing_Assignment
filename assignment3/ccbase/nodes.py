#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 16:14:30 2021
Refactored module, holding different kinds of graph nodes. Our basic graph
node from before will be used as baseclass for other extensions.

Last modified: 10.11.2021 

@author: jpoeppel
"""
from __future__ import annotations
import numpy as np
import copy


class Node:
    """
        Base class for nodes within a graph.

        Attributes
        ----------
        name: String
            The name or identifier of the node
        parents: dict
            A dictionary containing parent-name:Node pairs for all parents of this node
        children: dict
            A dictionary containing child-name:Node pairs for children of this node

    """
    
    def __init__(self, name: str):
        self.name = name
        self.parents = {}
        self.children = {}
        
    def add_parent(self, parent: Node):
        """
            Add or overwrites a parent node. Will not check if there already is
            a parent with the same name.
            
            Parameters
            ----------
            parent: Node
                The node to be added as parent.
        """
        self.parents[parent.name] = parent
        
    def add_child(self, child: Node):
        """
            Add or overwrites a child node. Will not check if there already is
            a child with the same name.
            
            Parameters
            ----------
            child: Node
                The node to be added as child.
        """
        self.children[child.name] = child
        
    def remove_parent(self, parent: Node):
        """
            Removes a parent node if it exists. If it did not exist, will do 
            nothing.
            
            Parameters
            ----------
            parent: Node
                The node to be removed as parent.
        """
        
        if parent.name in self.parents:
            del self.parents[parent.name]
            
    def remove_child(self, child: Node):
        """
            Removes a child node if it exists. If it did not exist, will do 
            nothing.
            
            Parameters
            ----------
            child: Node
                The node to be removed as child.
        """
        if child.name in self.children:
            del self.children[child.name]
        
    def destroy(self):
        """
            "Destroys" the node by removing its link to all its neighbours.
            This will **not** destroy the actual node object. This would have
            to be taken care of elsewhere.
        """
        for p in self.parents.values():
            p.remove_child(self)
        
        for c in self.children.values():
            c.remove_parent(self)
        self.parents = {}
        self.children = {}
        
    def __hash__(self) -> str:
        """
            The hash of a node is the same as the hash of its name.
            This allows to reference nodes in dictionaries by their object
            instantiation or their name.
        """
        return hash(self.name)
        
    def __str__(self) -> str:
        """
            Overwrites the default string representation of this class to just
            return it's name.
        """
        return self.name
    
    def __repr__(self) -> str:
        """
            Overwrites the default string representation of this class to just
            return it's name.
        """
        return self.name
    
    def __eq__(self, other: Node) -> bool:
        """
            Two nodes are considered to be identical if they have the
            same name.
            In order for the access in dictionaries via the name to work, a
            random node is equal to its name as well.
        """
        try:
            return other.name == self.name
        except AttributeError:
            return other == self.name
        
    def __ne__(self, other: Node) -> bool:
        """
            Checking if the given node is NOT equal to the current instance.
        """
        return not self.__eq__(other)

    def clone(self) -> Node:
        """
            Creates a deep copy of the current node instance.
        """
        return copy.deepcopy(self)