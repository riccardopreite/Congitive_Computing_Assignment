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

from .nodes import Node

import numpy as np

class Graph:
    
    def __init__(self):
        self.nodes = {}
        
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
            
    def get_number_of_nodes(self) -> int:
        """
            Returns
            -------
            int
                The total number of nodes in the graph.
        """
        return len(self.nodes)

    @property
    def num_nodes(self) -> int:
        """
            Performs the same as "get_number_of_nodes" but as a property.

            Returns
            -------
            int
                The total number of nodes in the graph.
        """
        return len(self.nodes)
    
    def get_parents(self, node: Union[str, Node]) -> List[Node]:
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
                Be careful that these are the actual node objects contained in
                the graph, NOT copies!

            Raises
            ------
            ValueError
                When the graph does not contain the queried node.
        """
        try:
            return list(self.nodes[node].parents.values())
        except KeyError:
            raise ValueError("The graph does not contain a node called {}".format(node))
            
    def get_children(self, node: Union[str, Node]) -> List[Node]:
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
                Be careful that these are the actual node objects contained in
                the graph, NOT copies!

            Raises
            ------
            ValueError
                When the graph does not contain the queried node.
        """
        try:
            return list(self.nodes[node].children.values())
        except KeyError:
            raise ValueError("The graph does not contain a node called {}".format(node)) 
            
    def get_ancestors(self, node: Union[str, Node]) -> List[Node]:
        """
            Parameters
            ----------
            node: String or Node
                The name of the node whose ancestors are queried.
                The Node object itself can also be used.
                
            Returns
            -------
            set
                A set containing all ancestor nodes of the specified node.
                Be careful that these are the actual node objects contained in
                the graph, NOT copies!

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

    def get_descendants(self, node: Union[str, Node]) -> List[Node]:
        """
            Parameters
            ----------
            node: String or `ccbase.nodes.Node`
                The name of the node whose descendants are queried.
                
            Returns
            -------
            set
                A set containing all descendant nodes of the specified node.
        """
        def _add_children(tmp_node):
            for p in tmp_node.children.values():
                if p in res:
                    continue
                res.add(p)
                _add_children(p)
        res = set()
        _add_children(self.nodes[node])
        return res
  

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
            
    def copy(self, deep=True) -> Graph:
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

    @property
    def is_directed(self) -> bool:
        """
            A property checking if this graph is directed in the 
            sense that there is only a directed edge between any two
            connected nodes. If any node is connected with a neighbor
            in both directions it is considered an undirected graph.
            A return of "False" here could mean an undirected graph, or
            a "broken" graph, not all edges are checked in that case.

            Returns
            -------
            bool
                True if there are only single connections between two
                connected nodes, False otherwise.
                False does **NOT** directly mean that this is a correct
                undirected graph! 
        """
        for n in self.nodes.values():
            for c in n.children.values():
                if c in n.parents:
                    return False
        return True
            
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
        # if res.is_directed: # This could be a shortcut, but since False does not 
        # guarantee a correct undirected graph, it is safer this way
        for n in res.nodes.values():
            for p in n.parents.values():
                n.add_child(p)
                p.add_parent(n)
            for c in n.children.values():
                c.add_child(n)
                n.add_parent(c)
        return res
        
        