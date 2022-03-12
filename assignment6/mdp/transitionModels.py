#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 11:06:50 2017
Module for different kinds of transition models. For now we only look at our
simple transition model described in the lecture and the assignment sheet.
@author: jpoeppel
Last modified: January, 12th 2022
"""
from __future__ import annotations
from typing import Optional, List, Tuple, Dict

import random

from .gridworld import Gridworld

__pdoc__ = {"SimpleTransitionModel.__call__": True}

class SimpleTransitionModel(object):
    """
        Represents a simple transition model which is constant for all 
        states in that the probability of reaching the next state with an
        action happens with probability accuracy. Deviations from the desired
        transition happens with the remaining probability, split according 
        to the specified ratio.
        See __call__ docs for details about how the actual probability is
        computed, especially with respect to running into walls.
    """
    
    def __init__(self, accuracy: float, gridworld: Gridworld, ratio: Optional[float] = 0.5):
        self.accuracy = accuracy
        self.ratio = ratio
        self.world = gridworld

    def __call__(self, state: Tuple[int,int], action: str, new_state: Tuple[int,int]) -> float:
        """
            The __call__ overwrite allows to use the transitionModel object as a 
            function:
            
            tm = TransitionModel(0.8, environment) #Creates a new transitionModel

            prob = tm((1,1), "N", (1,2)) #Queries the transition model for the
                                         #probability fo reaching state (1,2)
                                         #coming from state (1,1) with action "N"
            
            Returns the probability of reaching newState from state when
            trying to perform action, according to the gridworld provided
            in the constructor.
                        
            This follows the description on the assignment: When performing
            an action, it has a certain chance to succeed (given by the accuracy
            parameter specified in the constructor). When it does not 
            succeed, the agent moves to the adjacent directions instead, 
            but never in the completely opposite direction.
            The probabilities for the two possible accidental directions is
            given by the remaining probability (1-accuracy) and the specified
            ratio. The first accidental direction (which is clockwise direction)
            is given by (1-accuracy)*ratio while the other direction is given
            by the remaining probability: (1-accuracy)*(1-ratio).
            
            Example:
            accuracy = 0.8
            ratio = 0.2
            action = N
            
            Considering no walls: Reaching the state/tile directly above the
            current state, is 0.8, while the tile to the right of the current
            one has a probability of 0.2*0.2 = 0.04 and the tile to the left
            has a probability of 0.2*0.8 = 0.16.
            
            Any action (accidental or not) that would bumb into a wall (non-
            passable tile) remains in the initial state. Therefore the 
            probability of remaining in the current state sums up the 
            probabilities of the cases where the agent could voluntarily or
            accidental run into a wall.           
            
            
            Parameters
            ---------
            state: tuple
                The initial state.

            action: string
                One of the allowed actions N,S,E,W.

            new_state: tuple
                The resulting state.
                
            Returns
            -------
                float
                The probability of reaching the new state from the old one,
                using the given action.
        """
        
        if action == "E":
            true_new = (state[0]+1, state[1])
            acc1 = (state[0], state[1]-1)
            acc2 = (state[0], state[1]+1)
        elif action == "W":
            true_new = (state[0]-1, state[1])
            acc1 = (state[0], state[1]+1)
            acc2 = (state[0], state[1]-1)
        elif action == "N":
            true_new = (state[0], state[1]+1)
            acc1 = (state[0]+1, state[1])
            acc2 = (state[0]-1, state[1])
        elif action == "S":
            true_new = (state[0], state[1]-1)
            acc1 = (state[0]-1, state[1])
            acc2 = (state[0]+1, state[1])
        else:
            raise ValueError("Unknown action: {}".format(action))
            
        resProb = 0
        if self.world.check_passable(new_state):
            # We add our accuracy probability when the new desired state has
            # actually been reached, or by following that action we run into a wall.
            if true_new == new_state or (new_state == state and \
                    not self.world.check_passable(true_new)):
                resProb += self.accuracy
                
            # If we reach an accidantal state, we add (1-noise)*ratio for the 
            # first accident
            # we also add this if the accidental state would run into a wall
            if new_state == acc1 or (new_state == state and \
                     not self.world.check_passable(acc1)):
                resProb += (1-self.accuracy)*self.ratio
                
            # If we reach an accidantal state, we add the remaining 
            # probability [ (1-noise)*(1-ratio)] for the second accident
            # we also add this if the accidental state would run into a wall    
            if new_state == acc2 or (new_state == state and \
                     not self.world.check_passable(acc2)):
                resProb += (1-self.accuracy)*(1-self.ratio)
            
        return resProb

    
    def sample_action(self, state: Tuple[int,int], action: str) -> str:
        """
            Samples the action the agent actually performs when he tries to
            perform the given action. Does not yet produce the actual effect,
            as this will depend on the environment (e.g. does the agent
            run into a wall). Hard codes our model of inaccuracy.
            
            Parameters
            ---------
            state: tuple
                The current state of the agent. Is ignored in this case since
                we have a constant transition probability.
            
            action: String
                The intended action.
                
            Returns
            -------
            String
                The action that will be performed.
        """
        u = random.random()
        if u <= self.accuracy:
            return action
        else:
            if u <= self.accuracy+(1-self.accuracy)*self.ratio:
                acc1 = True
            else:
                acc1 = False
                
            if action == "N":
                if acc1:
                    return "E"
                else:
                    return "W"
            if action == "S":
                if acc1:
                    return "W"
                else:
                    return "E"
            if action == "E":
                if acc1:
                    return "S"
                else:
                    return "N"
            if action == "W":
                if acc1:
                    return "N"
                else:
                    return "S"