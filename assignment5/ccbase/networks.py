#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 13:46:30 2017
Refactored module for holding graphical networks. At this point we only
need our graph class and its subclass for Bayesian networks.
@author: jpoeppel
"""
from __future__ import annotations

import copy
from typing import Union, Optional, List, Dict, Iterable

from .nodes import DiscreteVariable, Node
from .factor import Factor

import numpy as np

class Graph:
    
    def __init__(self):
        self.nodes = {}
        self.is_directed = True
        
    def add_node(self, node: Union[str, Node]):
        """
            Adds a node to the graph. Will first create a new node object
            with the given name.
            
            Parameters
            ----------
            node: String or Node
                The name of the new node or the new node directly. In case
                a string is passed, a new node will be created before adding it.
        """
        if node in self.nodes:
            raise ValueError("The graph already contains a node named {}".format(node))
        
        try:
            self.nodes[node.name] = node
        except AttributeError: #We check for an attribute, rather than a type.
            self.nodes[node] = Node(node)
        
    def remove_node(self, node: Union[str, Node]):
        """
            Removes the node with the given name from the graph.
            
            Parameters
            ----------
            node: String or Node
                The name of the new node or the node object itself.
        """
        if not node in self.nodes:
            raise ValueError("The graph does not contain a node named {}".format(node))
        
        self.nodes[node].destroy()
        del self.nodes[node]
        
    def add_edge(self, node1: Union[str, Node], node2: Union[str, Node]):
        """
            Adds a directed edge from node1 to node2. In this implementation, edges
            are only implictly represented, via parent and child relations in the
            nodes. One could alternatively explicitly represent edge objects that
            connect nodes.
            
            Parameters
            ----------
            node1: String or Node
                The name of the first node. The node object can also be used.
            node2: String or Node
                The name of the second node. The node object can also be used.

            Raises
            ------
            ValueError
                When either of the two nodes does not exist in the graph.
        """
        try:
            self.nodes[node1].add_child(self.nodes[node2])
            self.nodes[node2].add_parent(self.nodes[node1])
            self.is_directed = True
        except KeyError:
            raise ValueError("At least one of your specified nodes ({},{}) " \
                             "is not contained in the graph".format(node1, node2))
            
    def remove_edge(self, node1: Union[str, Node], node2: Union[str, Node]):
        """
            Removes an edge from node1 to node2, if it exists. Ignores incorrect
            edges.
            
            Parameters
            ----------
            node1: String or Node
                The name of the first node. The node object can also be used.
            node2: String or Node
                The name of the second node. The node object can also be used.
            Raises
            ------
            ValueError
                When either of the two nodes does not exist in the graph.
        """
        try:
            self.nodes[node1].remove_child(self.nodes[node2])
            self.nodes[node2].remove_parent(self.nodes[node1])
        except KeyError:
            raise ValueError("At least one of your specified nodes ({},{}) " \
                             "is not contained in the graph".format(node1, node2))
            
    def get_number_of_nodes(self):
        """
            Returns
            -------
            int
                The total number of nodes in the graph.
        """
        return len(self.nodes)
    
    def get_parents(self, node: Union[str, Node]):
        """
            Parameters
            ----------
            node: String or Node
                The name of the node whose parents are queried.
                The Node object itself can also be used.
                
            Returns
            -------
            list
                A list containing all parent nodes of the specified node.

            Raises
            ------
            ValueError
                When the graph does not contain the queried node.
        """
        try:
            return self.nodes[node].parents.values()
        except KeyError:
            raise ValueError("The graph does not contain a node called {}".format(node))
            
    def get_children(self, node: Union[str, Node]):
        """
            Parameters
            ----------
            node: String
                The name of the node whose children are queried.
                The Node object itself can also be used.
                
            Returns
            -------
            list
                A list containing all children nodes of the specified node.

            Raises
            ------
            ValueError
                When the graph does not contain the queried node.
        """
        try:
            return self.nodes[node].children.values()
        except KeyError:
            raise ValueError("The graph does not contain a node called {}".format(node)) 
            
    def get_ancestors(self, node: Union[str, Node]):
        """
            Parameters
            ----------
            node: String or Node
                The name of the node whose ancestors are queried.
                The Node object itself can also be used.
                
            Returns
            -------
            list
                A list containing all ancestor nodes of the specified node.

            Raises
            ------
            ValueError
                When the graph does not contain the queried node.
        """
        if not node in self.nodes:
            raise ValueError("The graph does not contain a node called {}".format(node))
        def _add_parents(tmpNode):
            for p in tmpNode.parents.values():
                if p in res:
                    continue
                res.add(p)
                _add_parents(p)
        res = set()
        _add_parents(self.nodes[node])
        return res

    def is_ancestor(self, node_a: Union[str, Node], node_b: Union[str, Node]) -> bool:
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
        return node_a in self.get_ancestors(node_b)

    def is_descendant(self, node_a: Union[str, Node], node_b: Union[str, Node]) -> bool:
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
        return node_b in self.get_ancestors(node_a)

    def is_acyclic(self) -> bool:
        """
            Computes whether or not this graph is acyclic.
        
            Returns
            ----------
            bool
                True if there are no cycles within the provided graph, False otherwise.
        """
        def _cyclic(node):
            """
                Private helper function to check if a node is cyclic.
                
                This basically implements a marking/painting algorithm going over all
                nodes and marking them according to 0=not yet visited, 1=currently
                active and 2=done, but with the short circuit of breaking as soon
                as we find a loop (i.e. we meet another node, that is currently
                active).
            """
            if statusMap[node] == 2:
                return False
            if statusMap[node] == 1:
                return True
            statusMap[node] = 1
            for n in node.children.values():
                if _cyclic(n):
                    return True
            statusMap[node] = 2
            return False
        
        statusMap = {}
        for n in self.nodes.values():
            statusMap[n] = 0
        for n in self.nodes.values():
            if _cyclic(n):
                return False

        return True
            
    def copy(self, deep: Optional[bool] = True) -> Graph:
        """
            Copies the current graph.
            
            Parameters
            ----------
            deep: Bool
                If true, a deep copy will be performed, i.e. all nodes are also
                copied. In a shallow copy, both graph instances will contain the
                same node references.
            
            Returns
            -------
            Graph
                Creates a (deep) copy of this graph.
        """
       
        if deep:
            return copy.deepcopy(self)
        else:
             return copy.copy(self)
            
    def to_undirected(self) -> Graph:
        """
            Returns an undirected copy this graph. Sine this implementation
            does not really specify edge directions, we consider a bidrectional
            graph as undirected!
            
            Returns
            -------
            Graph
                An undirected copy of this graph.
        """
        res = self.copy()
        if res.is_directed:
            for n in res.nodes.values():
                for p in n.parents.values():
                    n.add_child(p)
                    p.add_parent(n)
                for c in n.children.values():
                    c.add_child(n)
                    n.add_parent(c)
            res.is_directed = False  
        return res
        

class BayesianNetwork(Graph):
    """
        Currently our Bayesian Network will simply be the same as our graph,
        but so that we can extend it later if needed, we subclass it here.
    """
    def __init__(self):
        #Call the constructor of the Graph class.
        super(BayesianNetwork, self).__init__()
        
    def marginals(self, node: Union[str, DiscreteVariable], evidence: Optional[Dict[str,str]]=None) -> np.array:
        """
            Computes the exact marginals for the node, given the evidence in 
            this network, using the old factor class.
            
            Note: The factor class will work correctly as long as the cpts of
            the nodes which created the factors were correct.
            
            Parameters
            ----------
            node : DiscreteVariable, String
                Either the node or the name of the node for which the marginals
                should be computed
                
            evidence : dict (optional)
                A dictionary containing node : outcome pairs to specify the 
                state of the given variables.
                
            Returns
            -------
            np.array
                A 1D array containing the marginals for the given node
        """
        # Make sure node is actually a DiscreteVariable
        node = self.nodes[node]
        node_name = self.nodes[node].name
        factors = [Factor.from_node(n) for n in self.nodes.values()]

        if evidence:
            #reduce factors by their evidence
            factors = [f.reduce(evidence) for f in factors]

        # Eliminate all non-query variables
        for v in self.get_elimination_ordering():
            if v == node_name:
                continue
            
            new_factor = Factor()
            new_factors = []
            for f in factors:
                if v in f.variable_order:
                    new_factor = new_factor * f
                else:
                    new_factors.append(f)
            new_factor = new_factor.marginalize(v)
            
            new_factors.append(new_factor)
            factors = new_factors
            
        fres = Factor()
        for f in factors:
            fres = fres * f
        
        return fres.potentials/np.sum(fres.potentials)
    
    def get_probability(self, instantiation: Dict[str, str], 
                            evidence: Optional[Dict[str, str]]=None) -> float:
        """
            Computes the exact (posterior) probabiliy for the given
            instantiation, 
            e.g. net.get_probability({"A":"a", "B":"b") = P(A=a, B=b)
            
            Parameters
            ----------
            instantiation: dict
                A dictionary containing variable:outcome pairs specifying the
                probability one is interested in.
                
            evidence : dict (optional)
                A dictionary containing node : outcome pairs to specify the 
                state of the given variables.
                
            Returns
            -------
            float
                The probability for the given instantiation.
                
        """
        factors = [Factor.from_node(n) for n in self.nodes.values()]

        if evidence:
            #reduce factors by their evidence
            factors = [f.reduce(evidence) for f in factors]

        # Eliminate all non-query variables
        for v in self.get_elimination_ordering():
            if v in instantiation.keys():
                continue
            
            new_factor = Factor()
            new_factors = []
            for f in factors:
                if v in f.variable_order:
                    new_factor = new_factor * f
                else:
                    new_factors.append(f)
            new_factor = new_factor.marginalize(v)
            
            new_factors.append(new_factor)
            factors = new_factors
            
        fres = Factor()
        for f in factors:
            fres = fres * f
        fres.potentials /= np.sum(fres.potentials)
        return fres.potential(instantiation)
                    
                
                    
    def get_elimination_ordering(self) -> List[str]:
       """
           Dummy elimination order implementation.
       """
       return list(self.nodes.keys())
    
    def to_undirected(self):
        raise NotImplementedError("A Bayesian Network cannot be undirected!")