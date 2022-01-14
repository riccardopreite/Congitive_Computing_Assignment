#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 2022
This is the skeleton file for assignment6. 
This assignment contains a lot of provided code since 
it covers different topics (DecisionTrees and Markov Decision Processes).
Do not be scared by the amount of code as you will not need to understand
most of it if you do not want to. The comments should highlight which parts
are important, which could be helpful to have a look at and which are just
helper/visualisation functions you can use with example calls at the end.
Let me know if anything is unclear or confusing when we go over this in the
tutorial sessions.

@author: jpoeppel
"""
from __future__ import annotations
from typing import Optional, List, Dict, Tuple

import numpy as np

# I provide quite a lot of code for this assignment. First for decision trees
# but even more for MDPs to get you going. The code for MDPs ranges from a basic
# environment implementation in Gridworld, the transition model you know
# from the lecture but which is also explained on the assignment itself
# to some basic renderers (console and matplotlib) to visualize 
# the MDP and its solutions. The MDP class itself also contains a lot of
# helper code within this file but the rest is moved to the mdp package.
# You do not necessarily need to worry about the 
# renderer or the gridworld beyond the functions described below as you should
# not need to worry about their implementation details. You should, however,
# look at the __call__ method of the SimpleTransitionModel!
# What may be important is that the gridworld has its origin in the bottom left.
# Coordinations (x,y) represent the horizontal (x) shift towards the right
# and vertical (y) shift up from there.

import mdp.renderer as renderer
from mdp.gridworld import Gridworld
from mdp.transitionModels import SimpleTransitionModel  


# =============================================================================
# Exercise 1
# =============================================================================

## In case you want to implement representations and functions for exercise 1
## you should to this here.

# =============================================================================
# Exercise 2 - DecisionTrees
# =============================================================================
    
# You should look at this base class, as it determines the attributes shared
# by the different TreeNode types you need to work with.
class TreeNode(object):
    """
        Base class for nodes in a simple decision tree. Each node in the tree 
        is either a root (no parent), a leave (no branches and no children)
        or an intermediate node, with a parent and named branches with child 
        nodes.
    """
    
    def __init__(self, name: str, branches: Optional[List[str]] =None, 
                        parent: Optional[TreeNode] =None):
        """
            Constructor of the base TreeNode. Should not be called directly but only by the 
            implementing classes (ActionNode, ChanceNode, UtilityNode).

            Parameters
            ----------
            name: str
                The name of the node.

            branches: List[str], optional
                A list of named branches. These names usually represent possible actions coming from
                ActionNodes or outcomes coming from UtilityNodes. These branches can represent possible
                children, that still need to be added with add_child.

            parent: TreeNode, optional
                The parent of the current node in the tree.
        """
        self.name = name
        self.parent = parent
        self.children = {}
        self.branches = branches
        
    def add_child(self, branch: str, child: TreeNode):
        """
            Adds a child to one of the branches of this TreeNode.
            A child can only be added to already existing branches.

            Parameters
            ----------
            branch: str
                The branch to add the child to.

            child: TreeNode
                A reference of the TreeNode that should be added as child.

            Raises
            ------
            AttributeError
                If the given branch was not initially specified when creating the TreeNode.
        """
        if branch in self.branches:
            self.children[branch] = child
        else:
            raise AttributeError("Node {} does not have branch {}".format(self, branch))
            
    def get_eu(self) -> float:
        """
            Need to be implemented by the inheriting classes. Should
            return the exptected utility for this node which is different
            depending on the node type.
        """
        raise NotImplementedError("Needs to be implemented by inheriting classes!")
        
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

# Relevant for exercise 2.1
class UtilityNode(TreeNode):
    
    def __init__(self, name: str, utility: float, parent: Optional[TreeNode] =None):
        """
        Constructor for a UtilityNode. These nodes represent the leave nodes
        of a decision tree, i.e. their utilities need to contain the sum
        of all partial utilities.
        
        Parameters
        ----------
        name: str
            A unique name for this UtilityNode.
            
        utility: float
            The utility associated with this node.
            
        parent: TreeNode (optional)
            The parent node of this node, usually not needed, as the add_child
            method of the dt will set the parent attribute correctly.
        """
        self.utility = utility
        super(UtilityNode,self).__init__(name, parent)
    
    def get_eu(self) -> float:
        """
            Returns the expected utility of this UtilityNode. 

            Returns
            -------
            float
                The EU of the UtilityNode.
        """
        raise NotImplementedError("TODO - Exercise 2 Task 1")

# Relevant for exercise 2.2
class ChanceNode(TreeNode):
    
    def __init__(self, name: str, probs: Dict[str, float], parent: Optional[TreeNode] =None):
        """
        Constructor for a ChanceNode. This is similar to our DiscreteVariables
        of a Bayesian network, but is simplyfied here for the sake of decision
        trees.
        
        Parameters
        ----------
        name: str
            A unique name for this ChanceNode.
            
        probs: dict
            A dictionary containing the possible outcomes as keys and their
            respective probabilities as values.
            
        parent: TreeNode (optional)
            The parent node of this node, usually not needed, as the add_child
            method of the DT will set the parent attribute correctly.
        """
        self.probs = dict(probs)
        super(ChanceNode, self).__init__(name, list(probs.keys()), parent)
        
    def get_eu(self) -> float:
        """
            Computes the expected utility of this ChanceNode. The EU of a
            ChanceNode represents the expectation with respect to the 
            possible outcomes of this node and their respective probabilities. 

            Returns
            -------
            float
                The EU of the ChanceNode
        """
        raise NotImplementedError("TODO - Exercise 2 Task 2")
        
# Relevant for exercise 2.3
class ActionNode(TreeNode):
    
    def __init__(self, name: str, options: List[str], parent: Optional[TreeNode] = None):
        """
        Constructor for an ActionNode. One can choose one action out of 
        multiple options. Also stores the best_action that was determined
        in the get_eu method.
        
        Parameters
        ----------
        name: str
            A unique name for this ActionNode.
            
        options: [str,]
            A list of possible options for this ActionNode.
            
        parent: TreeNode (optional)
            The parent node of this node, usually not needed, as the add_child
            method of the DT will set the parent attribute correctly.
        """
        self.best_action = None
        super(ActionNode, self).__init__(name, options, parent)
        
    def get_eu(self) -> float:
        """
            Computes the EU of the ActionNode. This EU should be the
            best possible EU corresponding to the action that has the
            highest EU. The action with the highest EU should also be stored
            in the best_action attribute so that it can be retrieved by the
            backward induction algorithm of the DecisionTree.

            Returns
            -------
            float
                The EU corresponding action that maximizes the EU.
        """
        raise NotImplementedError("TODO - Exercise 2 Task 3")
                
 
# A class you do not need to touch, but that allows us to actually 
# work with decision trees. The solution can be achieved using the 
# backward_induction algorithm that is implemented here. You can 
# check how the different nodes are used here and you can use the
# result from that function to check your get_eu implementations.
class DecisionTree(object):
    """
        Very simple implementation of a decision tree. Since we are using
        a dictionary to store all nodes (and all action_nodes for easier
        access) using their names, the nodes we are adding need to have 
        different names to avoid accidentially overwriting some nodes 
        (see get_simple_dt for an example of how you can name the nodes).
    """
    
    def __init__(self):
        self.root = None
        self.nodes = {}
        self.action_nodes = {}
        
    def set_root(self, node: TreeNode):
        """
            Method to set the root node of the decision tree.
            
            Parameter
            --------
            node: TreeNode
                The node which should be the root of the DT.
        """
        self.root = node
        self.nodes[node.name] = node
        if isinstance(node, ActionNode):
            self.action_nodes[node.name] = node
        
    def add_child(self, node: TreeNode, branch: str, child: TreeNode):
        """
            Method to add a new node as the child of another node.
            
            Parameters
            ---------
            node: TreeNode
                A node already contained in the dt under which to add the 
                child.

            branch: str
                Name of the branch the child should be added under.

            child: TreeNode
                The new child node which should be added.
        """
        if node.name in self.nodes:
            self.nodes[node.name].add_child(branch, child)
            self.nodes[child.name] = child
            if isinstance(child, ActionNode):
                self.action_nodes[child.name] = child
            child.parent = node
        else:
            raise AttributeError("Node {} does not exist.".format(node))
            
    def backward_induction(self, actions: Optional[Dict[str,str]] = None) -> Dict[str, Tuple[str, float]]:
        """
            Method to perform backward_induction on this decision tree (DT) to 
            compute for each action_node it's optimal decision and the
            corresponding eu.
            
            Parameter
            --------
            actions: dict (optional)
                If given, specifies certain actions as given, i.e. they should
                not be optimized. The dictionary should contain action_node 
                name: decision pairs, e.g. {"Party": "yes"} for the simple DT.
                
            Returns
            -------
            dict
                A dictionary containing the action node names as keys and a 
                tuple consisting of the action to choose and it's associated
                expected utility as value, e.g. {"Party": ("yes", 140)}
        """
        if actions is None:
            actions = {}
            
        # Reset best actions!
        for node in self.action_nodes.values():
            node.best_action = None
        
        for node in actions:
            self.action_nodes[node].best_action = actions[node]
            
        # Compute the EU for the entire tree so that all "best_actions"
        # are set in action nodes.
        eu = self.root.get_eu()
        for node in self.action_nodes.values():
            actions[node.name] = (node.best_action, node.get_eu())
            
        return actions

        
# =============================================================================
# Exercise 3 - Markov Decision Process
# =============================================================================

class MarkovDecisionProcess(object):
    """
        Main class you should be working on for exercise 3. 
        You will have to implement the "value_iteration" and "get_action"
        functions.
    """
    def __init__(self, environment: Gridworld, states: List[Tuple[int,int]], 
                        initial_state: Tuple[int,int], actions: List[str], 
                        transition_model: SimpleTransitionModel, reward_function: Dict[Tuple[int,int], float], 
                        discount: float, terminal_states: Optional[List[Tuple[int,int]]] = None):
        """
            Constructor for an MDP
            
            Parameters
            ----------
            environment: `mdp.gridworld.Gridworld`
                The environment this MDP lives in.
            states: [tuple,]
                A list of states, in this cases tuples representing positions
                within the environment
            initial_state: tuple
                A tuple representing the initial position of the agent
            actions: [string,]
                A list of possible actions, here we only consider the
                actions "N","S","E","W" as available actions.
            transition_model: `mdp.transitionModels.SimpleTransitionModel`
                The transition model representing the probabilities of going
                from one state to another using a certain action
            reward_function: dict(tuple:float)
                A dictionary containing rewards for all possible terminal
                states. Values should be between -1, 1 to not confuse the 
                visualizations
            discount: float
                Discounting factor to be used in the Bellmann equation during
                value iteration.
            terminal_states: list, optional
                List of terminalstates for the environment. If not given, the
                keys in the reward function are assumed to be the terminal 
                states. If these are given, the rewards are considered "intermediate"
                rewards that do not terminate an episode.
                
        """
        self.environment = environment        
        self.initial_state = initial_state
        self.states = states
        self.actions = actions
        self.transition_model = transition_model
        self.reward_function = reward_function
        self.discount = discount
        self.renderers = []
        if terminal_states is None:
            self.terminal_states = list(reward_function.keys())
        else:
            self.terminal_states = list(terminal_states)
        
        
    ######
    #
    # Task 1 and 2
    # Value Iteration
    #
    ######
    def value_iteration(self, num_max_iterations: Optional[int] =100, 
                                epsilon: Optional[float] =None, 
                                plot_delay: Optional[float] =None) -> Dict[Tuple[int,int], float]:
        """
            Computes the expected utilities for each state of the MDP using
            value iteration!
            
            Parameters
            ----------
            num_max_iterations: int, optional
                The maximum number of iterations that should be performed.
                Default: 100
                
            epsilon: float, optional
                Threshold for the changes in the expected utility values.
                Required for exercise 2.
            
            plot_delay: float, optional
                If this is given, the current utilities will be plotted by all
                registered renderers, pausing the given delay (in seconds)
                before continuing with the next iteration. Default: None
            
            Returns
            --------
            dict(tuple:float)
                A dictionary containing state:expected utility pairs for 
                each state of the MDP.
        """
        
        #Hint: The MDP object already contains the required variables, such
        # as the transition_model or the reward_function, see the constructor
        # for their respective names.
        
        #Hint: Remember that the reward function is only a dictionary, where
        # only the terminal states are specified! You will need to consider
        # how you deal with the not-specified states!
        
        #Hint: You might want to use the "get_neighbour_states" function
        # provided by the environment. 
        
        #Hint: You can use the transition_model like a function. Look at the
        # documentation of the "__call__" method in 
        # transitionModels.SimpleTransitionModel for more information.
        
        raise NotImplementedError("TODO Exercise 3, Tasks 1 and 2")
        
        #Hint: You can can use "render_utilities" within your loop if you want 
        # to have online visualization of your computed utilities
        
        
    ######
    #
    # Task 3
    # Policy computation
    # Hint: In case you have problems with exercise 1, you can compute
    # utility values by hand, and use those for task 3.
    #
    ######       
    def get_policy(self, utilities: Dict[Tuple[int,int], float]) -> Dict[Tuple[int,int], str]:
        """
            Computes an optimal policy based on the given utilities and 
            the internal transitionModel.
            
            Parameters
            ----------
            utilities: dict(tuple:float)
                A dictionary containing state:expected utility pairs for all
                states of the MDP
                
            Returns
            --------
            dict(tuple:string)
                A dictionary containing state:action pairs. The actions should
                be one of "N","S","E","W" and represent the optimal action
                given the utilities and the transition probabilities!
        """
        raise NotImplementedError("TODO Exercise 3, Task 3")
            
    
    ######
    #
    # Helper functions that can be used to visualize the computed results!
    # You would normally not have to make any changes here, but feel free to
    # modify the code if you want to do things differently.
    #
    ######
    
    def render_utilities(self, utilities: Dict[Tuple[int,int], float], 
                                iteration: Optional[int] =0, 
                                pause: Optional[float] =0.0):
        """
            Calls all registered renderers to plot the given utilities in
            the grid. Will pause the execution for pause
            seconds after plotting.
            
            Parameters
            ----------
            utilities: dict(tuple:float)
                A dictionary containing state:expected utility pairs for all
                states of the MDP

            iteration: int, optional
                The current iteration these utilities were produced at. Will
                be displayed in the plot. Default: 0

            pause: float, optional
                The time in seconds the program should pause after plotting.
                Default: 0.0
        """
        for rend in self.renderers:
            rend.plot_utilities(utilities, iteration, walls=True)
            #This will pause twice if you use both renderers!
            rend.pause(pause) 
         
    
    def render_policy(self, policy: Dict[Tuple[int,int], str]):
        """
            Calls all registered renderers to plot the given policy.
            
            Parameters
            ----------
            policy: dict(tuple:string)
                A dictionary containing state:action pairs.
            
        """
        for rend in self.renderers:
            rend.plot_policy(policy, walls=True)
            
    def render_agent(self, agent_pos: Tuple[int,int], pause: Optional[float] =0.0):
        """
            Calls all registered renderers to plot the grid with the agent
            at the specified position. Will pause the execution for pause
            seconds after plotting.
            
            Parameters
            ----------
            agent_pos: tuple
                The current position of the agent in the world.

            pause: float, optional
                The time in seconds the program should pause after plotting.
                Default: 0.0
        """
        grid =self.environment.get_grid_representation(add_outer=True)
        for pos in self.reward_function:
            grid[pos[1]+1][pos[0]+1] = self.reward_function[pos]
        for rend in self.renderers:
            #Do +1 on the agent pos, because we added the walls here
            #which means the agent needs to be shifted in the visualization
            #to account for the walls
            rend.plot(grid, (agent_pos[0]+1,agent_pos[1]+1))
            rend.pause(pause)
            
    def use_policy(self, policy: Dict[Tuple[int,int], str], step_delay: Optional[float] =0.5):
        """
            Uses the given policy in order to reach a terminal state as given
            by the reward function. In case the agent reaches a state with a 
            positive reward, it is a success, otherwise it is a failure.
            The agent's intended and actual action will be printed and it's
            progress rendered by all registered renderers.
            
            Parameters
            ----------
            policy: dict(tuple:String)
                The policy to follow in the form as returned by get_policy
            
            step_delay: float, optional
                Delay (in seconds) between two steps. Default: 0.5
        """
        agent_pos = self.initial_state
        
        #Plot initial state
        self.render_agent(agent_pos, step_delay)
        
        reached = False
        while not reached:
            intended_action = policy[agent_pos]
            print("Agent wants to perform: {}".format(intended_action))
            performed_action = self.transitionModel.sample_action(agent_pos, intended_action)
            print("Agent performs: {}".format(performed_action))
            
            agent_pos = self.environment.act(agent_pos, performed_action)
            
            #The reward Function only holds values for terminal states
            if agent_pos in self.terminal_states:
                reached = True
                
            #Render resulting state
            self.render_agent(agent_pos, step_delay)
                    
        if self.rewardFunction[agent_pos] > 0: 
            print("Agent reached positive state! Success!")
        else:
            print("Agent reached negative state! Failure!")
          



# Some example decision trees that are used in the example calls.
# I suggest working through them by hand to compare your implementation's
# solution with your manual solution.   
def get_simple_dt():
    """
        Creates a simple 1 decision tree to show how the classes
        are meant to be used and how the nodes can be named to allow easy
        distinction of the different nodes. The problem basically boils
        down to throwing a party or not which takes into account the
        probability of it raining.
    """
    dt = DecisionTree()
    dt.set_root(ActionNode("Party", ["yes", "no"]))
    
    c1 = ChanceNode("Party:yes,Rain", {"yes": 0.6, "no": 0.4})
    dt.add_child(dt.root, "yes", c1)
    dt.add_child(c1, "yes", UtilityNode("Party:yes,Rain:yes", -100))
    dt.add_child(c1, "no", UtilityNode("Party:yes,Rain:no", 500))
    
    c2 = ChanceNode("Party:no,Rain", {"yes": 0.6, "no": 0.4})
    dt.add_child(dt.root, "no", c2)
    dt.add_child(c2, "yes", UtilityNode("Party:no,Rain:yes", 0))
    dt.add_child(c2, "no", UtilityNode("Party:no,Rain:no", 50))
    
    return dt

def get_two_decision_dt():
    """
        A more complex DecisionTree with 2 hierarchical actions:
        You can choose to perform a survey regarding the market situation
        of your startup idea. If you choose to perform a survey you can
        find out something about the likely demand for your product. 
        Regardless of whether you perform the survey or not you can then decide
        to do your start-up. The market has a certain probability to be low, medium
        or high which determines your final utilities.
        In this example you can already see that decision trees can become fairly unwieldy 
        quickly.
    """
    dt = DecisionTree()
    dt.set_root(ActionNode("Survey", ["yes", "no"]))
    
    c1 = ChanceNode("Survey:yes,Demand", {"low": 0.25, "medium":0.45, "huge":0.3})
    dt.add_child(dt.root, "yes", c1)
    
    a2 = ActionNode("Survey:no,Start-up", ["yes", "no"])
    dt.add_child(dt.root, "no", a2)
    
    c2 = ChanceNode("Survey:no,Start-up:yes,Market", {"low":0.3, "medium":0.5, "high": 0.2})
    dt.add_child(a2, "yes", c2)
    
    dt.add_child(a2, "no", UtilityNode("Survey:no,Start-up:no", 0))
    dt.add_child(c2, "low", UtilityNode("Survey:no,Start-up:yes,Market:low", -15))
    dt.add_child(c2, "medium", UtilityNode("Survey:no,Start-up:yes,Market:medium", 5))
    dt.add_child(c2, "high", UtilityNode("Survey:no,Start-up:yes,Market:high", 25))
    
    a3 = ActionNode("Survey:yes,Demand:low,Start-up", ["yes", "no"])
    dt.add_child(c1, "low", a3)
    c3 = ChanceNode("Survey:yes,Demand:low,Start-up:yes,Market", {"low":0.75, "medium":0.2, "high": 0.05})
    dt.add_child(a3, "yes", c3)
    dt.add_child(a3, "no", UtilityNode("Survey:yes,Demand:low,Start-up:no",-5))
    dt.add_child(c3, "low", UtilityNode("Survey:yes,Demand:low,Start-up:yes:Market:low",-20))
    dt.add_child(c3, "medium", UtilityNode("Survey:yes,Demand:low,Start-up:yes:Market:medium",0))
    dt.add_child(c3, "high", UtilityNode("Survey:yes,Demand:low,Start-up:yes:Market:high",20))
    
    a4 = ActionNode("Survey:yes,Demand:medium,Start-up", ["yes", "no"])
    dt.add_child(c1, "medium", a4)
    c4 = ChanceNode("Survey:yes,Demand:medium,Start-up:yes,Market", {"low":0.15, "medium":0.6, "high": 0.25})
    dt.add_child(a4, "yes", c4)
    dt.add_child(a4, "no", UtilityNode("Survey:yes,Demand:medium,Start-up:no",-5))
    dt.add_child(c4, "low", UtilityNode("Survey:yes,Demand:medium,Start-up:yes:Market:low",-20))
    dt.add_child(c4, "medium", UtilityNode("Survey:yes,Demand:medium,Start-up:yes:Market:medium",0))
    dt.add_child(c4, "high", UtilityNode("Survey:yes,Demand:medium,Start-up:yes:Market:high",20))
    
    a5 = ActionNode("Survey:yes,Demand:huge,Start-up", ["yes", "no"])
    dt.add_child(c1, "huge", a5)
    c5 = ChanceNode("Survey:yes,Demand:huge,Start-up:yes,Market", {"low":0.05, "medium":0.3, "high": 0.65})
    dt.add_child(a5, "yes", c5)
    dt.add_child(a5, "no", UtilityNode("Survey:yes,Demand:huge,Start-up:no",-5))
    dt.add_child(c5, "low", UtilityNode("Survey:yes,Demand:huge,Start-up:yes:Market:low",-20))
    dt.add_child(c5, "medium", UtilityNode("Survey:yes,Demand:huge,Start-up:yes:Market:medium",0))
    dt.add_child(c5, "high", UtilityNode("Survey:yes,Demand:huge,Start-up:yes:Market:high",20))
    
    return dt
  
            
#####
#
# Specification of some simple testworlds for the MDP
#
#####
def testWorld1():
    """
        The simple example from the lecture and the assignment sheet.
    """
    
    #Specify a gridworld using "g" for free ground and "#" for walls/obstacles.
    #We could also specify the outer walls here, but then we need to not
    #addOuter when getting a grid representation, or adding walls when plotting!
    world_string = "gggg\n" + \
                  "g#gg\n" + \
                  "gggg"
                  
    environment = Gridworld()
    states = environment.parse_environment(world_string, get_passable_states=True)
    
    initial_state = (0,0)
    
    #We use a simple dictionary as reword function where we only specify the 
    #terminal states.
    rewards = dict()
    rewards[(3,2)] = 1
    rewards[(3,1)] = -1
    
    return environment, states, initial_state, rewards


def testWorld2():
    world_string = "ggggg\n" + \
                  "g#ggg\n" + \
                  "g#ggg\n" + \
                  "ggggg\n" + \
                  "ggggg"
                  
    environment = Gridworld()
    states = environment.parse_environment(world_string, get_passable_states=True)
    
    initial_state = (0,1)
    
    #We use a simple dictionary as reword function where we only specify the 
    #terminal states.
    rewards = dict()
    rewards[(0,0)] = -1
    rewards[(1,0)] = -1
    rewards[(2,0)] = -1
    rewards[(3,0)] = -1
    rewards[(4,0)] = -1
    rewards[(2,2)] = 0.1
    rewards[(4,2)] = 1
    
    return environment, states, initial_state, rewards


def testWorld3():
    world_string = "gg#gggg\n" + \
                  "gg#gggg\n" + \
                  "gg#gggg\n" + \
                  "ggggggg\n" + \
                  "gggg##g\n" + \
                  "ggggggg"
                  
    environment = Gridworld()
    states = environment.parse_environment(world_string, get_passable_states=True)
    
    initial_state = (6,5)
    
    #We use a simple dictionary as reword function where we only specify the 
    #terminal states.
    rewards = dict()
    rewards[(2,2)] = -1
    rewards[(6,4)] = -1
    rewards[(1,3)] = -0.5
    rewards[(0,5)] = 1
    rewards[(0,1)] = 0.5
    
    # You might want to experiment what happens if you do not specify all
    # states giving rewards as terminal states, e.g. by omitting (0,1) from
    # the list below    
    terminals = [(2,2),(6,4),(1,3),(0,5),(0,1)] 
    
    return environment, states, initial_state, rewards, terminals

        

if __name__ == "__main__":
    

# =============================================================================
#   Exercise 2 - Example calls of using the Decision Tree
# =============================================================================
    
    dt = get_simple_dt()
    print("Optimal action sequence for the simple DT: ", dt.backward_induction())
    
    dt2 = get_two_decision_dt()
    print("Optimal action sequence for the two decision DT: ", dt2.backward_induction())
    
# =============================================================================
#   Exercise 3 - Example calls for using the MDP
# =============================================================================
    #We are currently only supporting these 4 actions    
    actions= ["N","S","E","W"]
    
    environment, states, initial_state, reward_function = testWorld1()
#    environment, states, initial_state, reward_function = testWorld2()
#    environment, states, initial_state, reward_function, terminals = testWorld3()

    # Feel free to create your own testworlds or try different parameters for
    # the transition model
    accuracy = 0.8
    ratio = 0.5 #Both accidental directions are equally likely
    discount = 0.9

    # Set up our simple transition model with the specified parameters
    trans = SimpleTransitionModel(accuracy, environment, ratio=ratio)
    
    
    # Set up our actual Markov Decision Process with all required variables
    mdp = MarkovDecisionProcess(environment, states, initial_state, actions, 
                                trans, reward_function, discount)
    
    # Add the basic console renderer
    mdp.renderers.append(renderer.ConsoleRenderer())
    # If matplotlib is installed, we will add the matplotlib renderer as well
    if renderer.matplotlibAvailable:
        mdp.renderers.append(renderer.MatplotlibRenderer())
    
    
    # After implementing Exercise 3.1, you can get your computed utilities like this
    # If you do not want to plot intermediate steps, just set plot_delay to
    # None or just omit it.
    utilities = mdp.value_iteration(num_max_iterations=100, plot_delay=0.1)
    
    # After implementing Exercise 3.2, you can also use a threshold epsilon which
    # stops the computation upon convergence.
#    utilities = mdp.value_iteration(num_max_iterations=1000, epsilon=0.001, plot_delay=0.1)
    
    # After implementing Exercise 3.3, you can get your computed policy like this
#    policy = mdp.get_policy(utilities)
    
    # This line can be used to render your policy
#    mdp.render_policy(policy)
    
    # If you want to let the agent follow the computed policy you can 
    # uncomment this line here
#    mdp.use_policy(policy, stepDelay=0.5)

    # This is here to prevent the program from finishing at the end as long as
    # a figure is still shown.    
    if renderer.matplotlibAvailable:
        renderer.show()
