#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Last modified on Thu Nov  23 16:17:23 2021
Skeleton file for exact inference.
@author: jpoeppel
"""

"""
    There are minor changes to the ccbase compared to assignment 3:
    ccbase.networks now contains a subclass BayesianNetwork, which so far does
    not add any additional information. 
    I also added a "DiscreteVariable" class to ccbase.nodes, which subclasses
    the old Node class to better represent variables in a Bayesian Network,
    in particular with respect to their outcomes. See the docs or the functions for
    creating example graphs for details.
    Furthermore, a reference implementation of the Factor class can now be 
    found in ccbase.factor.
    The known classes Graph and Node have themselves not been changed and are
    just as you have seen in the previous assignments.
"""

from copy import copy
from typing import Union, Optional, List, Dict, Iterable, Tuple

from ccbase.networks import BayesianNetwork, Graph
from ccbase.nodes import DiscreteVariable, Node
from ccbase.factor import Factor
import numpy as np
from math import inf


########
#      #
# Ex 1 #
#      #
########

def get_elimination_ordering(bn: BayesianNetwork) -> List[str]:
    """
        Computes an elimination order of all the variables in the network
        according to the MinFillOrder heuristic.

        Parameters
        ---------
        bn: BayesianNetwork
            The BayesianNetwork for which the elimination order is to be 
            computed.
        
        Returns
        -------
        [str]
            A list containing the names of all the nodes in the network
            bn, in an order following a suitable heuristic.
            
        Remark:
            Exercise 1 Task 2 does not require you to write code, instead
            you should describe another heuristic and explain how it works
            and what the differences are with respect to the MinFillOrder.
    """
    def compute_neighbors_edge(g: Graph, node: Union[str,Node])-> int:
        parents: list = g.get_parents(node)
        edge_number: int = 0

        ext_neighbor: Node
        for ext_neighbor in parents:
            
            int_neighbor: Node
            for int_neighbor in parents:
                if (ext_neighbor != int_neighbor) and (int_neighbor not in ext_neighbor.parents):
                    
                    edge_number += 1
                    g.add_edge(int_neighbor,ext_neighbor)
                    g.add_edge(ext_neighbor,int_neighbor)
        
        g.remove_node(node)
        return edge_number, g

    graph: Graph = Graph()
    graph.nodes = copy(bn.nodes)
    elimination_order: list = []

    graph = graph.to_undirected()

    
    # for index in range(0,len(graph.nodes)):
    while (True):
        """These variables are used to updating the local min"""
        node_to_remove: str = ""
        min_adding_edge: int = inf
        """Making a copy of the working graph so we can physically adding the edges and removing the node"""
        working_graph = graph.copy()
        tmp_added_edges_graph = Graph()
        
        for node in graph.nodes:
            
            if node not in elimination_order:
                """Computing the number of edges that should be added to the node neighborhood"""
                (edge_that_should_be_added, editedGraph) = compute_neighbors_edge(working_graph.copy(), node)
                
                """Updating local min edge counter and node name that should be removed"""
                if edge_that_should_be_added < min_adding_edge:
                    node_to_remove = node
                    tmp_added_edges_graph = editedGraph

        """
            When the node that should be removed is computed we can add it to te list
            And updated the working graph with the edges added in the node 
            neighborhood and that node removed
        """
        elimination_order.append(node_to_remove)
        working_graph = tmp_added_edges_graph

        if len(elimination_order) == len(graph.nodes):
            break

    return elimination_order
        


########
#      #
# Ex 2 #
#      #
########

def initialize_factors(bn: BayesianNetwork, evidence: Optional[Dict[str, str]]) -> Iterable[Factor]:
    """
        Creates and returns a factor for every node in the Bayesian network initialized according
        to the node's CPTs while taking the given evidence into account.

        Parameters
        ---------
        bn: BayesianNetwork
            The BayesianNetwork for which the elimination order is to be 
            computed.
        evidence: Dict[str, str], optional
            A dictionary containing the evidence variables as keys and their
            observed outcomes as values. 

        Returns
        -------
            Iterable[Factor]
            An iterable (e.g. a list or a set) containing a factor for every 
            node in the BayesianNetwork, properly initialized.
    """
    raise NotImplementedError("TODO Exercise 2.1")

def sum_product_elim_var(factors: Iterable[Factor], variable: str) -> Iterable[Factor]:
    """
        Eliminates the given variable from the given factors via marginalization.

        Parameters
        ----------
        factors: iterable of ccbase.factor.Factor
            Any iterable of factors from which the variable is to be removed
        variable: String
            The variable to be eliminated.

        Returns
        --------
        iterable of ccbase.factor.Factor
            The remaining factors that do no longer include the eliminated variable.
    """
    raise NotImplementedError("TODO Exercise 2.2")


def calculate_probabilities(bn: BayesianNetwork, 
                        variables: Union[str, DiscreteVariable], 
                        evidence: Optional[Dict[str,str]] = None) -> Factor:
    """
        Calculates P(variables|evidence) for all outcome combinations of
        variables  (i.e. you should return a table similar to a cpt, 
        only representing a joint distribution in this case.)
        
        Example: Calling calculate_marginals(["rain", "winter"], 
                                                {"sprinkler":"True"})
        should return a Factor representing P(rain,winter|sprinkler=True). 
        
        Parameters
        ----------
        bn: BayesianNetwork
            The BayesianNetwork for which the elimination order is to be 
            computed.
        variables: [str, Node]
            List containing the nodes, or their names of the variables of 
            interest.
            (Hint: Your code can/should assume, that a name is passed and
            simply retrieve the node manually, so that you do not have
            to differentiate these two cases.)
        evidence: Dict[str, str], optional
            A dictionary containing the evidence variables as keys and their
            observed outcomes as values. If evidence is not given, the prior
            marginals should be computed.
            
        Returns
        -------
        ccbase.factor.Factor
            A Factor over the specified variables, specifying the joint (posterior) probability
            of these variables.
    """
    raise NotImplementedError("TODO Exercise 2.3")
            

########
#      #
# Ex 3 #
#      #
########     

def maximize_out(factor: Factor, variable: str) -> Factor:
    """
        Takes a factor and removes the given variable from that
        factor via maximization, according to the definition in
        Darwiche: Modeling and Reasoning with Bayes:

        $$ (max_x f)(\mathbf{y}) = max_x f(x, \mathbf{y}) $$

        Parameters
        ----------
        factor: ccbase.factor.Factor
            The factor from which to remove the variable.
        variable: String
            The name of the variable to be maxmized out.

        Returns
        --------
        ccbase.factor.Factor
            A new factor that results from maximizing out the 
            variable from the initial factor.
    """
    raise NotImplementedError("TODO Exercise 3.1")


def max_product_elim_var(factors: Iterable[Factor], variable: str) -> Tuple[Iterable[Factor], Factor]:
    """
        Eliminates the given variable from the given factors via maximization.
        You will want to return BOTH the iterable (e.g. list) of remaining facotrs
        as well as a factor combining all factors that contained the eliminated 
        variable.

        Parameters
        ----------
        factors: iterable of ccbase.factor.Factor
            Any iterable of factors from which the variable is to be removed
        variable: String
            The variable to be eliminated.

        Returns
        --------
        iterable of ccbase.factor.Factor
            The remaining factors that do no longer include the eliminated variable.
        ccbase.factor.Factor
            The factor combining all factors containing the variable, i.e. the "product-factor"
            before the maximization. This is helpful for traceback function.
    """ 
    raise NotImplementedError("TODO Exercise 3.2")

def traceback(factors: Dict[str, Factor], order: List[str]) -> Dict[str,str]:
    """
        Computes the optimal instantiation of all variables based on
        the given factors and elimination order.

        Parameters
        ----------
        factors: dict of ccbase.factor.Factor
            A dictionary containing variable-name:Factor pairs, where each 
            Factor is the Factor from which the variable was removed via
            maximization.
        order: list of String
            The order in which the variables have been eliminated.

        Returns
        -------
        dict
            A dictionary containing variable:outcome pairs representing the
            MPE.
    """
    raise NotImplementedError("TODO Exercise 3.3")


def calculate_MAP(bn: BayesianNetwork, 
                evidence: Optional[Union[str, DiscreteVariable]] =None) -> Tuple[float, Dict[str,str]]:
    """
        Function calculating the most probable explanation (MPE) as well as its
        probability given potential evidence.

        Parameters
        -----------
        bn: ccbase.networks.BayesianNetwork
            The BayesianNetwork for which the MAP is to be computed.
        evidence: {Node/Nodename: Outcome}, optional
            The evidence which needs to be considered when computing the MAP.

        Returns
        --------
        float
            The probability of the MPE.
        dict
            A dictionary representing the MPE as Variable:Outcome pairs for all
            variables in the network.
    """
    raise NotImplementedError("TODO Exercise 3.4")
    



######
#
# Example networks
#
######


def get_simple_net():
    """
        Helper function to generate a simple BayesianNetwork with binary
        variables.
    """
    net = BayesianNetwork()

    #Create the discrete variables that should be contained in the network
    node_winter = DiscreteVariable("winter", ["True", "False"])
    node_sprinkler = DiscreteVariable("sprinkler", ["True", "False"])
    node_rain = DiscreteVariable("rain", ["True", "False"])
    node_grass = DiscreteVariable("wet_grass", ["True", "False"])
    node_road = DiscreteVariable("slippery_road", ["True", "False"])

    #Add the nodes to the network
    net.add_node(node_winter)
    net.add_node(node_sprinkler)
    net.add_node(node_rain)
    net.add_node(node_grass)
    net.add_node(node_road)

    #Setup the relationships between the variables
    net.add_edge(node_winter, node_sprinkler)
    net.add_edge(node_winter, node_rain)
    net.add_edge(node_sprinkler, node_grass)
    net.add_edge(node_rain, node_grass)
    net.add_edge(node_rain, node_road)
    
    #Setup the (conditional) probability tables.
    #Make sure that you set these tables AFTER you specify the edges, as adding
    #an edge would require changes to the cpts!
    #Also note, that currently you need ot be careful to specify the table in
    #the correct format, as mentioned in tutorial session 3!
    
    # This corresponds to P(winter=True) = 0.6 and P(winter=False) = 0.4
    node_winter.set_probability_table(np.array([0.6, 0.4]))
    
    # As sprinkler has 1 parent (winter) this corresponds to:
    # P(sprinkler=True|winter=True) = 0.2
    # P(sprinkler=True|winter=False) = 0.75
    # P(sprinkler=False|winter=True) = 0.8
    # P(sprinkler=False|winter=False) = 0.25
    
    node_sprinkler.set_probability_table(np.array([[0.2, 0.75], 
                                                   [0.8, 0.25]]))
    
    # Analogue to the sprinkler node
    node_rain.set_probability_table(np.array([[0.8, 0.1], 
                                              [0.2, 0.9]]))
    
    # Analogue to the sprinkler node, just with rain as parent
    node_road.set_probability_table(np.array([[0.7, 0.0], 
                                              [0.3, 1.0]]))
    
    # Grass has 2 parents, sprinkler and rain (in that order as specified above!)
    # Accordingly this corresponds to:
    # P(grass=True|sprinkler=True, rain=True)= 0.95
    # P(grass=True|sprinkler=True, rain=False)= 0.1
    # P(grass=True|sprinkler=False, rain=True)= 0.8
    # P(grass=True|sprinkler=False, rain=False)= 0.0
    # P(grass=False|sprinkler=True, rain=True)= 0.05
    # P(grass=False|sprinkler=True, rain=False)= 0.9
    # P(grass=False|sprinkler=False, rain=True)= 0.2
    # P(grass=False|sprinkler=False, rain=False)= 1.0
    node_grass.set_probability_table(np.array([
                                            [ #Block for grass=True 
                                                [0.95, 0.1], #sprinkler=True
                                                [0.8, 0.0 ] #sprinkler = False
                                            ], 
                                            [ # Block for grass=False
                                                [0.05, 0.9], #sprinkler=True
                                                [0.2, 1.0] #sprinkler=False
                                            ]]))
    
    
    
    return net

def get_non_binary_net():
    """
        Helper function to generate a simple BayesianNetwork with
        non-binary variables.
    """
    net = BayesianNetwork()
    
    node_john = DiscreteVariable("john", ["Calling", "Not_calling"])
    node_burglary = DiscreteVariable("burglary", ["Intruder", "Safe"])
    node_alarm = DiscreteVariable("alarm", ["Ringing", "Silent", "Broken"])
    
    net.add_node(node_john)
    net.add_node(node_burglary)
    net.add_node(node_alarm)
    
    net.add_edge(node_alarm, node_john)
    net.add_edge(node_burglary, node_john)
    
    node_burglary.set_probability_table(np.array([0.4,0.6]))
    node_alarm.set_probability_table(np.array([0.2,0.3,0.5]))
    node_john.set_probability_table(np.array([
                                                [
                                                    [0.8, 0.6], #alarm=ringing
                                                    [0.7, 0.1], #alarm=silent
                                                    [0.5, 0.2] #alarm=broken
                                                ],
                                                [
                                                    [0.2, 0.4],
                                                    [0.3, 0.9],
                                                    [0.5, 0.8]
                                                ]]))
    
    return net


## test cases
if __name__ == "__main__":
    
    net1 = get_simple_net()

    print("Elimination order: ", get_elimination_ordering(net1))
    pass
    # Example of how to construct factors from a DiscreteVariables
    node_rain = net1.nodes["rain"]
    # Note that I am using the classmethod here, i.e. I call the method on
    # the class, not on any instance of it!
    rain_factor = Factor.from_node(node_rain)
    winter_factor = Factor.from_node(net1.nodes["winter"])
    
    # Calling sum_product_elim_var only with factors not containing the
    # variable should not change anything
    assert sum_product_elim_var([rain_factor], "wet_grass")[0] == rain_factor
    # The trivial case of having only 1 factor with only 1 variable, results in an
    # empty factor with value 1 in this case.
    assert sum_product_elim_var([winter_factor], "winter")[0].potential({}) == 1
    
    #Simplest testcase. We use allclose instead of equal to avoid precisiion errors.
    res = calculate_probabilities(net1, ["winter"])
    np.testing.assert_allclose(res.potential({"winter":"True"}), 0.6)
    # The reference Factor class stores the values in a np.array called "potentials", 
    # we can check the entrire result using:
    np.testing.assert_allclose(res.potentials, np.array([0.6,0.4]))

    # maximize_out will remove variables from the factors
    assert rain_factor.variable_order == ["rain", "winter"]
    res_factor = maximize_out(rain_factor, "winter")
    assert res_factor.variable_order == ["rain"]

    # Max product will also only influence factors that contain the variable
    assert max_product_elim_var([rain_factor], "wet_grass")[0][0] == rain_factor
    # Similarly to sum_product_elim_var, max will also produce an empty factor
    # when the last variable is removed, but the potential will not be 1 but the
    # max
    assert max_product_elim_var([winter_factor], "winter")[0][0].potential({}) == 0.6

    # The traceback function is more difficult to test by itself as it requires
    # suitable factors.

    # You should test your MAP results using your calculate_probabilities function
    mpe_prob, mpe = calculate_MAP(net1)
    print("The MAP is {} with probability: {}".format(mpe, mpe_prob))
    joint_posterior_factor = calculate_probabilities(net1, list(mpe.keys()))
    print("Probability for the mpe: {}".format(joint_posterior_factor.potential(mpe)))
    # Similarly with evidence!

    # Some more interesting examples, you would need to calculate the correct
    # results yourself, or use, e.g. samIam to compare
    
    print("Tests for net 1")
    print("="*20)
    
    prior_slippery = calculate_probabilities(net1, ["slippery_road"])
    # We can call a Factor just like a function, which will call the "potential" function.
    print("Prior marginal for node slippery_road=False: {}".format(prior_slippery({"slippery_road":"False"})))

    posterior_grass = calculate_probabilities(net1, ["wet_grass"], {"slippery_road":"True"})
    print("Posterior marginal for node wet_grass=False given slippery_road=True: {}".format(posterior_grass({"wet_grass": "False"})))
    
    
    posterior_rain_winter = calculate_probabilities(net1, ["rain", "winter"], {"sprinkler":"True"})
    print("Posterior marginal for nodes rain=True and winter=False, given sprinkler=True: {}".format(posterior_rain_winter({"rain":"True","winter":"False"})))


    # Feel free to construct more testcases, e.g. with the non_binary, multivariate network 

    # print("Tests for net 2")
    # print("===============")
    
    # net2 =  get_non_binary_net()
    
    # print("Prior for John=Not_calling: ", calculate_probabilities(net2, ["john"])({"john":"Not_calling"}))
    # print("Prior for burglary=Intruder: ", calculate_probabilities(net2, ["burglary"])({"burglary":"Intruder"}))
    # print("Prior for alarm=Broken: ", calculate_probabilities(net2, ["alarm"])({"alarm":"Broken"}))