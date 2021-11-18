"""
Last modified on Tue Nov 24 15:33 2020
@author: jpoeppel
"""

# Import of the provided graph class. You would
# need to change this line if you plan to use your
# own graph class!

# If you change this, make sure you also import you Graph
# with that name, e.g. if you want to use the assignment1.py file
# directly your import could look like:
# from assignment1.py import DGraph as Graph
# Also make sure to submit your assignment1.py (or whatever you end up)
# calling it, alongside this file so that the imports work!
from ccbase.networks import Graph
from ccbase.nodes import Node
###
# You should not really require numpy for this assignment, but you are free
# to use it if you want.
import numpy as np
# Imports for type hints
from typing import Union, List, Iterable

###
# Note: If you use your own graph implementation, take care
# that the parameters may be either a node's name or a node's
# object. You do however not need to worry about implementing both
# return types. It will be enough as long as the functions return either
# node objects or the node names (or lists thereof). Similarly, when implementing
# the functions below, it is sufficient if your solutions work with either names
# or node objects.


## Exercise 1: Finding basic (causal) structures

def find_forks(dg: Graph) -> List[Union[Node, str]]:
    
    """
        Finds all forks within the given directed graph.
        
        Parameters
        ----------
        dg: ccbase.networks.Graph
            The (directed) graph whose forks are to be found.
            You can assume that the graph will be directed.
            
        Returns
        ----------
        list of ccbase.nodes.Node or Strings
            A list containing all Nodes (either object or their name/id) that
            represent forks in the network.
    """
    fork_node:list = []
    for node_name in dg.nodes:
        node:Node = dg.nodes.get(node_name)
        if len(node.children) > 1:
            fork_node.append(node)
    return fork_node

def find_chains(dg: Graph) -> List[Union[Node, str]]:
    """
        Finds all chains within the given directed graph.
        
        Parameters
        ----------
        dg: ccbase.networks.Graph
            The (directed) graph whose chains are to be found.
            You can assume that the graph will be directed.
            
        Returns
        ----------
        list of ccbase.nodes.Node or Strings
            A list containing all Nodes (either object or their name/id) that
            represent chains in the network.
    """
    chain_node:list = []
    for node_name in dg.nodes:
        node:Node = dg.nodes.get(node_name)
        if len(node.children) > 0 and len(node.parents) > 0:
            chain_node.append(node)
    return chain_node
def find_collider(dg: Graph) -> List[Union[Node, str]]:
    """
        Finds all colliders within the given graph.
        
        Parameters
        ----------
        dg: ccbase.networks.Graph
            The (directed) graph whose colliders are to be found.
            You can assume that the graph will be directed.
            
        Returns
        ----------
        list of ccbase.nodes.Node or Strings
            A list containing all Nodes (either object or their name/id) that
            represent collider in the network.
    """
    collider_node:list = []
    for node_name in dg.nodes:
        node:Node = dg.nodes.get(node_name)
        if len(node.parents) > 1:
            collider_node.append(node)
    return collider_node

### Exercise 2: Markov Equality

def find_immoralities(graph: Graph) -> List:
    """
        A function to return all immoralities (i.e. two nodes with the same 
        child but no direct connection) of the given directed graph.

        Parameter
        ---------
        graph: ccbase.networks.Graph or equivalent
            The directed graph to check for immoralities

        Returns
        -------
        list
            A list of all immoralities contained in the graph. How you
            represent a single immorality is up to you.
    """
    raise NotImplementedError("TODO Exercise 2.1")

def same_skeleton(graph1: Graph, graph2: Graph) -> bool:
    """
        A function to check whether or not the two given directed graphs have the
        same skeleton

        Parameters
        ----------
        graph1: ccbase.networks.Graph or equivalent
            The first directed graph to test.
        graph2: ccbase.networks.Graph or equivalent
            The second directed graph to test against the first.

        Returns
        -------
        bool
            True if the two graphs have the same skeletongs, False otherwise.
    """
    raise NotImplementedError("TODO Exercise 2.2")

def markov_equivalent(graph1: Graph, graph2: Graph) -> bool:
    """
        A function to check whether or not the two given directed graphs are Markov
        equivalent.

        Parameters
        ----------
        graph1: ccbase.networks.Graph or equivalent
            The first directed graph to test.
        graph2: ccbase.networks.Graph or equivalent
            The second directed graph to test against the first.

        Returns
        -------
        bool
            True if the two graphs are Markov equivalent, False otherwise.
    """
    raise NotImplementedError("TODO Exercise 2.3")

## Exercise 3: Paths

def get_paths(graph: Graph, node_x: Union[Node, str], 
                    node_y: Union[Node, str]) -> List[List[Union[Node, str]]]:
    """
        Computes all undirected paths between node_x and node_y within
        the (directed or undirected) graph.

        Parameters
        ----------
        graph: ccbase.networks.Graph
            The graph in which to compute the paths. This may be directed or
            undirected.
        node_x: ccbase.nodes.Node or String
            The node object or name for the first of the two nodes.
        node_y: ccbase.nodes.Node or String
            The node object or name for the second of the two nodes.

        Returns
        --------
        list of lists of ccbase.nodes.Node or Strings
            A list of lists of node objects (or node names) that each represent
            an undirected path from node_x to node_y. These paths should contain
            the starting and end nodes as well.
    """
    raise NotImplementedError("TODO Exercise 3")

## Exercise 4: D-Separation

def is_collider(dg: Graph, node: Union[Node, str], 
                        path: List[Union[str, Node]]) -> bool:
    """
        Checks whether or not the given node is a collider with respect to the 
        given path.

        Parameters
        ----------
        dg: ccbase.networks.Graph
            The directed graph that contains at least all the nodes of the given 
            path and their connections.
        node: ccbase.nodes.Node or String
            The node object (or its name) of a node that should be present in the 
            given path, which is to be checked.
        path: list of ccbase.nodes.Node or Strings
            A list of node objects (or node names) that represents
            an undirected path that contains the given node.

        Returns
        ----------
        bool
            True if the given node is a collider with respect to the given path
            within the graph, False otherwise.
    """
    raise NotImplementedError("TODO Exercise 4.1")


def is_path_open(dg: Graph, path: List[Union[Node,str]], 
                    nodes_z: Iterable[Union[Node, str]]) -> bool:
    """ 
        Checks whether or not the given path is open conditioned on the given nodes.

        Parameters
        ---------
        dg: ccbase.networks.Graph
            The directed graph that should contain all the nodes and their connections.
        path: list of ccbase.nodes.Node or Strings
            A list of node objects (or node names) that represents
            an undirected path between the first and last node of the path within 
            the graph.
        nodes_z: iterable of ccbase.nodes.Node or Strings
            The set of conditioned nodes (or their names), that might influence the 
            paths between node_x and node_y
        
        Returns
        --------
        bool
            False if the path is blocked given given the nodes_z, True otherwise.
        
    """
    raise NotImplementedError("TODO Exercise 4.2")


def unblocked_path_exists(dg: Graph, node_x: Union[Node, str], 
            node_y: Union[Node, str], nodes_z: Iterable[Union[Node, str]]) -> bool:
    """
        Computes if there is at least one unblocked undirected path
        between node_x and node_y when considering the nodes in nodes_z.
        
        Parameters
        ---------
        dg: ccbase.networks.Graph
            The directed graph that should contain all the nodes.
        nodes_x: ccbase.nodes.Node or String
            The first of the two nodes whose paths are to be checked.
        nodes_y: ccbase.nodes.Node or String
            The second of the two nodes whose paths are to be checked.
        nodes_z: iterable of ccbase.nodes.Node or Strings
            The set of conditioned nodes, that might influence the paths 
            between node_x and node_y
            
        Returns
        --------
        bool
            False if all undirected paths between node_x and node_y are blocked 
            given the nodes_z, True otherwise.
    """
    raise NotImplementedError("TODO Exercise 4.3")

def check_independence(dg: Graph, nodes_x: Iterable[Union[Node, str]], 
        nodes_y: Iterable[Union[Node, str]], nodes_z: Iterable[Union[Node, str]]) -> bool:
    """
        Computes whether or not nodes in nodes_x are conditionally 
        independend of nodes in nodes_y given nodes in nodes_z.
        
        Parameters
        ---------
        dg: ccbase.networks.Graph
            The directed graph that should contain all the nodes.
        nodes_x: iterable of ccbase.nodes.Node or String
            The nodes that should be conditionally independent of the nodes
            in nodes_y
        nodes_y: iterable of ccbase.nodes.Node or String
            The nodes that should be conditionally independent of the nodes
            in nodes_x                
        nodes_z: iterable of ccbase.nodes.Node or String
            The set of nodes that should make nodes_x and nodes_y conditionally
            independent.
            
        Returns
        ----------
        bool
            True if all nodes in nodes_x are conditionally independent of all
            nodes in nodes_y given the nodes in nodes_z, False otherwise.
    """
    raise NotImplementedError("TODO Exercise 4.4")



## Exercise 5: General graphical test 

def make_ancestral_graph(graph: Graph, nodes: Iterable[Union[Node, str]]) -> Graph:
    """
        Computes the ancestral graph of the given graph for the given set of nodes.

        Parameters
        ----------
        graph: ccbase.networks.Graph
            The (directed) graph from which to compute the ancestral graph.
        nodes: Iterable of ccbase.nodes.Node or String
            The set of nodes for which to compute the ancestral graph.

        Returns
        -------
        ccbase.networks.Graph
            The resulting ancestral graph.
    """
    raise NotImplementedError("TODO Exercise 5.1")

def make_moral_graph(graph: Graph) -> Graph:
    """
        Computes the moral graph of the given graph, i.e., an
        undirected copy of the given graph with all immoralities removed.

        Parameters
        ----------
        graph: ccbase.networks.Graph
            The (directed) graph from which to compute the moral graph.

        Returns
        -------
        ccbase.networks.Graph
            The resulting moral graph which is undirected.
    """
    raise NotImplementedError("TODO Exercise 5.2")

def separation(graph: Graph, nodes_z: Iterable[Union[Node, str]]) -> Graph:
    """
        Separates the given nodes from the graph.

        Parameters
        ----------
        graph: ccbase.networks.Graph
            The (directed) graph from which to separate the given nodes.
        nodes_z: Iterable of ccbase.nodes.Node or String
            The set of nodes to separate.

        Returns
        -------
        ccbase.networks.Graph
            The resulting graph with all links from the nodes in node_z
            separated.
    """
    raise NotImplementedError("TODO Exercise 5.3")

def check_independence_general(graph: Graph, nodes_x: Iterable[Union[Node, str]], 
            nodes_y: Iterable[Union[Node, str]], nodes_z: Iterable[Union[Node, str]]) -> bool:
    """
        Computes whether or not nodes in nodes_x are conditionally 
        independend of nodes in nodes_y given nodes in nodes_z
        using the general graphical test.
        
        Parameters
        ---------
        dg: ccbase.networks.Graph
            The directed or undirected graph that should contain all the nodes.
        nodes_x: iterable of ccbase.nodes.Node or String
            The nodes that should be conditionally independent of the nodes
            in nodes_y
        nodes_y: iterable of ccbase.nodes.Node or String
            The nodes that should be conditionally independent of the nodes
            in nodes_x                
        nodes_z: iterable of ccbase.nodes.Node or String
            The set of nodes that should make nodes_x and nodes_y conditionally
            independent.
            
        Returns
        ----------
        bool
            True if all nodes in nodes_x are conditionally independent of all
            nodes in nodes_y given the nodes in nodes_z, False otherwise.
    """
    raise NotImplementedError("TODO Exercise 5.4")

def create_example_graphs():
    """
        A method to create a trivial example graph from the 
        lecture. Feel free to create your own methods that generate
        graphs on which you want to test your implementations!

        Returns
        --------
        ccbase.networks.Graph
            A directed graph containing the four nodes A,B,E and R.
    """
    dg = Graph()
    dg.add_node("A")
    dg.add_node("B")
    dg.add_node("E")
    dg.add_node("R")
    dg.add_edge("B","A")
    dg.add_edge("E","A")
    dg.add_edge("E","R")

    dg2 = dg.copy()
    dg2.remove_edge("E","R")
    dg2.add_edge("R","E")
    return dg, dg2


if __name__ == "__main__":
    # Example calls
    g1, g2 = create_example_graphs()
    forks = find_forks(g1)
    print("The graph contains the following forks: {}".format(forks))
    assert set(forks) == set(["E"])
    chains = find_chains(g1)
    print("The graph contains the following chains: {}".format(chains))
    assert set(chains) == set([])
    colliders = find_collider(g1)
    print("The graph contains the following colliders: {}".format(colliders))
    assert set(colliders) == set(["A"])

    #Markov Equality Since you determine how to represent immoralities
    # I cannot provide any asserts here.
    print("Immoralities for graph 1: ", find_immoralities(g1))
    print("Do g1 and g2 have the same skeleton? ", same_skeleton(g1, g2))
    print("Are g1 and g2 Markov Equivalent? ", markov_equivalent(g1, g2))

    # Graphical independence tests
    # Hint: You may want to test these methods with a more complex graph!
    paths = get_paths(g1, "B", "R")
    print("Undirected paths from B to R in the graph: {}".format(paths))

    # D-Separation 
    path = ["B","A","E"]
    print("Is A a collider for the path {}? {}".format(is_collider(g1, "A", path)))
    print("Is path {} open? {}".format(path, is_path_open(g1, path, [])))
    nodes_z = ("A","E")
    print("Is there a path from B to R not blocked by {}? {}".format(nodes_z, unblocked_path_exists(g1, "B","R", nodes_z)))
    print("Are Nodes B and R independent given nodes {}?: {}".format(nodes_z, check_independence(g1, ("B"), ("R"), nodes_z)))

    # The general test should also work with undirected graphs:
    # This basically manually moralizes the graph before making it undirected 
    # to make it a fair comparison to the D-Separation above.
    g2.add_edge("B","E")
    g2 = g2.to_undirected()
    print("Are the nodes B and R independent given nodes {}?: {}".format(nodes_z, check_independence_general(g2, ("B"), ("R"), nodes_z)))