#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue, 07.12.2021.
Skeleton file for assignment5 about 
approximate inference and some initial decision making.

@author: jpoeppel
"""
from typing import Union, Optional, List, Dict, Iterable, Tuple

import numpy as np

import random

from ccbase.networks import BayesianNetwork
from ccbase.nodes import DiscreteVariable


"""
    For this assignment you can again use the BayesianNetwork implementation
    that you already saw in assignment4. The class was slightly extended
    by now including reference implementations for exact inference, primarily
    useable to compare your approximate results to the exact solutions and 
    the last exercise.
    You may want to consider DiscreteVariable's get_distribution function,
    which can be used for sampling (see 
    DiscreteVariable.get_distribution(self, evidence=None) or the example
    below). The function works similar to the factor's potential function
    in that it selects the appropraite elements of the numpy-array but 
    will create a dictionary as used by the sample-function in exercise 1.
    
    As always feel free to add tests of your own to check your code's functionality.
    Especially concerning the approximate inference methods, you can always compare
    their results with your exact results from the last assignment as they should
    be very close once you increase the number of samples.

    Automatic testing for these approximate solutions will consider certain margains that 
    your solutions should get close to the true probability/distribution, but I will also
    manually go over the different solutions in order to reduce the number of "false negatives".
"""


######
#
# Ex 1
#
######


def sample(distribution: Dict[str, float]) -> str:
    """
        Sample an outcome from a given probability distribution using the
        univariate sampling (also called roulette wheel selection) mentioned
        in the lecture.
        
        Parameters
        ----------
        distribution: dict
            A dictionary containing the possible outcomes of a random
            variable as keys and their respective probabilities as values.
        
        Returns
        -------
        String
            The sampled outcome
    """
    raise NotImplementedError("TODO, Exercise 1")
    


######
#
# Ex 2.1
#
######


def get_ancestral_ordering(bayesnet: BayesianNetwork) -> List[str]:
    """
        Generate an ancestral ordering for nodes of the given network.
        
        Parameters
        ----------
        bayesnet: ccbase.networks.BayesianNetwork
            The network whose nodes are to be ordered.
            
        Returns
        -------
        List[str]
            A list containing the names of the network's nodes in
            ancestral ordering (i.e. all parents of a node appear before that
            node in the list)
    """
    
    raise NotImplementedError("TODO, Exercise 2.1")
    
    
######
#
# Ex 2.2
# In case you are struggeling with exercise 2.1 you can still implemenet this
# function just using "get_ancestral_ordering" at the appropriate position.
# If you want to test the sampling, you could overwrite the result of 
# "get_ancestral_ordering" with an order you compute by hand for an example
# network. That way you can still complete this task without completing
# the previous one.
#
######

def do_forward_sampling(bayesnet: BayesianNetwork, var_name: str, num_samples: Optional[int]=1000) -> Dict[str, float]:
    """
        Calculate marginals using Forward Sampling without worrying about
        dealing with evidence.
        
        Parameters
        -----------
        bayesnet: ccbase.networks.BayesianNetwork
            The network to be sampled.
        var_name: string
            The name of the variable whose marginal is to be approximated.
        num_samples: int (optional)
            The number of samples to be generated to estimate the marginal. Default
            1000.
            
        Returns
        --------
        Dict[str, float]
            A dictionary containing the outcomes of the variable var_name
            as keys and those outcomes marginal probabilities as values.
    """    
    raise NotImplementedError("TODO, Exercise 2.2")


######
#
# Ex 3.1
#
######

def create_initial_sample(bayesnet: BayesianNetwork, evidence: Dict[str, str]) -> Dict[str,str]:
    """
        Create an initial sample useable for Gibbs sampling for the given network that
        takes the given evidence into account.

        Parameters
        ----------
        bayesnet: ccbase.networks.BayesianNetwork
            The network in which to sample.
        evidence: Dict[str,str]
            Node-name:outcome pairs specifying the observed evidence.

        Returns
        -------
        Dict[str,str]
            A dictionary containing node-name:outcome pairs for all nodes in the
            network required for Gibbs sampling.
    """
    raise NotImplementedError("TODO, Exercise 3.1")


######
#
# Ex 3.2
#
######

def get_markov_distr(node: DiscreteVariable, evidence: Dict[str, str]) -> Dict[str, float]:
    """
        Computes the local probability distribution for the random variable represented
        by the given node, given the provided evidence. 

        Parameters
        ----------
        node: ccbase.nodes.DiscreteVariable
            The DiscreteVariable from a BayesianNetwork for which the distribution
            is to be computed. 
        evidence: dict
            A dictionary containing node names as keys and their observed outcomes
            as values. You may assume that this dictionary contains key-value
            pairs for all nodes in the Bayesian network from which "node" came. 
        
        Returns
        -------
        Dict[str, float]
            A dictionary representation of a probability distribution with the outcomes
            of node as keys and their probabilities as values.  
    """
    raise NotImplementedError("TODO, Exercise 3.2")

######
#
# Ex 3.3
#
######

def do_gibbs_sampling(bayesnet: BayesianNetwork, var_name: str, evidence: Dict[str, str], 
                        num_samples: Optional[int] =1000, 
                        burn_in_period_length: Optional[int] =100, thinning: Optional[int] =1) -> Dict[str, float]:
    """
        Calculate marginals using Gibbs Sampling.
        Hint: Remember that you will have to sample from the local probability
        according to a node's MarkovBlanket instead of its local cpt!
        
        Parameters
        ---------
        bayesnet: ccbase.networks.BayesianNetwork
            The network from which the samples should be created.
        var_name: str
            The variable to calculate marginals for
        evidence: Dict[str, str]
            A dictionary containing node_name: outcome pairs to specify the
            evidence.
        num_samples: int (optional)
            Number of samples to be used for the marginal computation after the burn_in_period. 
            Default 1000.
        burn_in_period_length: int (optional) 
            Number of samples that are discarded at the beginning. Default 100.
        thinning: int (optional)
            Only take every nth sample for the calculation of the marginal. 
            Default 1.
         
        Returns
        -------
        Dict[str, float]
            A dictionary containing the outcome of the variable var_name
            as keys and those outcomes marginal probabilities as values
            obtained by gibbs sampling.
    """
    
    raise NotImplementedError("TODO, Exercise 3.3")


######
#
# Exercise 4
#
######

def expected_utility(net: BayesianNetwork, actions: Dict[str, str], 
                    evidence: Dict[str, str], utilities: Dict[str, List[float]], 
                    use_do: Optional[bool]=True) -> float:
    """
        Computes the expected utility of the given action in the given network, taking into account the given 
        evidence and utilities while applying the Do-Operator or not.

        Parameters
        ----------
        net: ccbase.networks.BayesianNetwork
            The BayesianNetwork in which to compute the expected utility.
        action: dict[str,str]
            A dictionary containing only 1 key-value pair specifying the intervention for 
            which the EU is to be computed. This pair represents a node-name: outcome
            pair for a node in the network.
        evidence: dict[str,str]
            A dictionary containing node-name: outcome pairs for observed evidence that
            should be considered when computed the EU.
        utilities: dict[str, List[float]]
            A dictionary specifying the utilities for different outcomes. The dictionary
            containes node-name: List pairs, where the list contains the utilities for
            the outcomes. You may assume that the order matches the outcome ordering of 
            the graph, i.e. if the node has outcomes [True, False], the first index in
            the utility list corresponds to the outcome "True" and the 2nd to "False.
        use_do: bool, Optional 
            If True, the Do-operator should be used to compute the EU.
            If False, the intervention/action should be considered as an additional
            observed evidence.

        Returns
        -------
        float
            The EU for the given action considering the evidence, utilities and potentially the Do-operator.
    
    """
    raise NotImplementedError("TODO, Exercise 4.1")


######
#
# An example network useable for all exercises.
#
######


def get_wetgrass_network():
    net = BayesianNetwork()

    #Create the discrete variables that should be contained in the network
    node_winter = DiscreteVariable("winter", ["True", "False"])
    node_sprinkler = DiscreteVariable("sprinkler", ["True", "False"])
    node_rain = DiscreteVariable("rain", ["True", "False"])
    node_grass = DiscreteVariable("wet_grass", ["True", "False"])
    node_fields = DiscreteVariable("dry_fields", ["True", "False"])

    #Add the nodes to the network
    net.add_node(node_winter)
    net.add_node(node_sprinkler)
    net.add_node(node_rain)
    net.add_node(node_grass)
    net.add_node(node_fields)

    #Setup the relationships between the variables
    net.add_edge(node_winter, node_sprinkler)
    net.add_edge(node_winter, node_rain)
    net.add_edge(node_sprinkler, node_grass)
    net.add_edge(node_rain, node_grass)
    net.add_edge(node_rain, node_fields)
    
    
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
    node_fields.set_probability_table(np.array([[0.01, 0.8], 
                                              [0.99, 0.2]]))
    
    # Grass has 2 parents, sprinkler and rain (in that order as specified above!)
    # Accordingly this corresponds to:
    # P(grass=True|sprinkler=True, rain=True)= 0.99
    # P(grass=True|sprinkler=True, rain=False)= 0.7
    # P(grass=True|sprinkler=False, rain=True)= 0.9
    # P(grass=True|sprinkler=False, rain=False)= 0.1
    # P(grass=False|sprinkler=True, rain=True)= 0.01
    # P(grass=False|sprinkler=True, rain=False)= 0.3
    # P(grass=False|sprinkler=False, rain=True)= 0.1
    # P(grass=False|sprinkler=False, rain=False)= 0.9
    node_grass.set_probability_table(np.array([
                                            [ #Block for wet_grass=True 
                                                [0.99, 0.7], #sprinkler=True
                                                [0.9, 0.1 ] #sprinkler = False
                                            ], 
                                            [ # Block for wet_grass=False
                                                [0.01, 0.3], #sprinkler=True
                                                [0.1, 0.9] #sprinkler=False
                                            ]]))
    
    return net

if __name__ == "__main__":

    # Example call for exercise 1
    exampleNode = DiscreteVariable("color", 
                               ["red","green", "blue"], 
                               np.array([0.15,0.55,0.3]))

    print("Sample drawn from sample distribution: {}".format(
                            sample(exampleNode.get_distribution())))

    # Example call for exercise 2.1
    print("nodes in ancestral ordering: {}".format( 
                                    get_ancestral_ordering(get_wetgrass_network()) ))



    # Example call for exercise 2.2
    print("forward sampling variable wet_grass: {}".format(
                                do_forward_sampling(get_wetgrass_network(), 
                                                    "wet_grass", 10000 ) ))


    # Example call for exercise 3
    print("gibbs sampling variable wet_grass given slippery_road=True: {}".format( 
        do_gibbs_sampling(get_wetgrass_network(), "wet_grass", 
                          {"slippery_road": "True"}, 1000, 100, 1) ))
    print("Exact result for that marginal: ", get_wetgrass_network().marginals("wet_grass", {"slippery_road": "True"}))


    print("gibbs sampling variable alarm given john=Calling: {}".format( 
        do_gibbs_sampling(get_wetgrass_network(), "alarm", 
                          {"john": "Calling"}, 1000, 100, 1) ))
