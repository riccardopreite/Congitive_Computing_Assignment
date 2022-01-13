#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 16:14:30 2020
Refactored module, holding different kinds of graph nodes. Our basic graph
node from before will be used as baseclass for other extensions.

@author: jpoeppel
"""
from __future__ import annotations
import numpy as np

from typing import Optional, List, Dict, Iterable

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
    
    
    
class DiscreteVariable(Node):
    """
        The extension of our classical graph node to represent discrete
        variables in Bayesian networks.
    """

    def __init__(self, name: str, outcomes: List[str], cpt: Optional[np.array] = None):
        super(DiscreteVariable, self).__init__(name)
        # In order to not rely on the parents dict to keep the order of the 
        # parents (which was not the case prior to Python3.6) we use an 
        # additional list to keep track of the parent order.
        self.parent_order = [] 
        
        # CPTs will be stored semi-compactly as an multidimensional array
        # using the first dimension for the outcomes of the variable itself,
        # and the following dimensions for this variable's parents.
        if cpt is not None:
            self.cpt = cpt
        else:
            self.cpt = 0
        self.outcomes = outcomes
        
    def add_parent(self, parent_node: DiscreteVariable):
        """
            Add the given parent node from this node's
            parents. Uses the DiscreteVariable function while
            making sure to update the parent_order as well.

            Parameter
            ---------
            parent_node: DiscreteVariable
                The DiscreteVariable to that is to be added as a parent.
        """
        self.parent_order.append(parent_node.name)
        super(DiscreteVariable,self).add_parent(parent_node)

    def remove_parent(self, parent_node: DiscreteVariable):
        """
            Removes the given parent node from this node's
            parents. Uses the DiscreteVariable function while
            making sure to update the parent_order as well.

            Parameter
            ---------
            parent_node: DiscreteVariable
                The DiscreteVariable to that is to be removed as a parent.
        """
        if parent_node.name in self.parent_order:
            self.parent_order.remove(parent_node.name)
        super(DiscreteVariable,self).remove_parent(parent_node)
        
    def set_probability_table(self, table: Iterable):
        """
            Allows to set the conditional probability density(table) of this
            node directly. Will check that the dimensions of the given cpd
            is conform to the current dependency structure but will not perform
            any tests on the actual values.
            
            Parameters
            ----------
            cpd : iterable
                Table containing the conditional probabilities. Each variable 
                is represented by a dimension in the size of the number of its
                outcomes.
        """
        
        # Check what dimensions the cpt would need to have given the current
        # parent structure of this node
        dimensions = [len(self.outcomes)]
        for parent_name in self.parent_order:
            dimensions.append(len(self.parents[parent_name].outcomes))
        #Make sure table is a numpy array and create copy.
        npTable = np.array(table)
        if npTable.shape != tuple(dimensions):
            raise ValueError("The dimensions of the given cpd do not match " + \
                             "the dependency structure of the node.")
        # Set the table
        self.cpt = npTable
        
    def get_distribution(self, evidence: Optional[Dict] = None) -> dict:
        """
            Returns the distribution in the form of a dictionary 
            (outcome:probability) for the this variable. 
            Uses a similar method as the factor.potential function.
            
            Parameter
            --------
            evidence: dict (optional)
                A dictionary containing variable:outcome pairs specifying
                the evidental state of the parent nodes.
                
            Returns
            -------
            dict
                A dictionary containing the outcomes of this variable as keys
                and their corresponding (conditional) probabilities given
                the evidence if present.
        """
        #Construct the index for the desired potential
        index = [list(range(len(self.outcomes)))]
        for p in self.parent_order:
            if p in evidence:
                try:
                    index.append([self.parents[p].outcomes.index(evidence[p])])
                except ValueError:
                    raise ValueError("The parent {} does not have the outcome " + \
                                     "{}".format(p, evidence[p]))
            else:
                raise ValueError("In order to get a distribution for this " + \
                                 "variable, all it's parents need to be specified " + \
                                 "as evidence, but {} was not specified.".format(p))
                    
        #np.ix_ constructs an access mask which allows efficient access
        #to the desired cells. This approach allows underspecification of the
        #instantiation (i.e. not all variables are specified) which will
        #result in returning a matrix for the remaining variables
        probs = np.squeeze(self.cpt[np.ix_(*index)])
        return {outcome: probs[i] for i,outcome in enumerate(self.outcomes)}
        
