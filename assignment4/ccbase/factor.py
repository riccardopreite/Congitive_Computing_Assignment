#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Last modified on Tue Nov 23 18:55:37 2021
A reference implementation of a factor classed used for 
probabilistic inferences in graphical models.
@author: jpoeppel
"""
from __future__ import annotations

import numpy as np
from typing import Union, Optional, List, Dict, Iterable
from .nodes import DiscreteVariable

class Factor(object):
    
    def __init__(self, variables: Optional[List[str]] = None, 
                    outcomes: Optional[Dict[str,List[str]]] = None, 
                    potentials: Optional[np.array] = None):
        """
            Constructor for a new factor. Without any parameters a trivial, 
            empty (unit) factor should be created which does not modify 
            another factor through multiplication. Otherwise, the factor is 
            created suitable for the provided variables and confirming to the 
            provided potentials.
            
            Parameters
            ----------
            variables: [String,] (optional)
                A list containing the variable names of all variables this 
                factor should represent.
            outcomes: dict (optional)
                A dictionary containing the variable names as keys and a list
                containing the possible outcomes of said variable as values.
            potentials: np.array (optional)
                A multidimensional array containing the potentials or factor values.
                The array must be ordered according to the variable and outcome lists.
                These could be conditional or marginal probabilities of a random variable
                (see `Factor.from_probabilities` function).
                
            Raises
            -------
            TypeError
                If some but not all three arguments were given, as the class requires
                either no argument or all three to work properly. 
        """
        parameters_none = [p is None for p in (variables, outcomes, potentials)]
        if not all(parameters_none):
            if any(parameters_none):
                raise TypeError("Some but not all arguments were given " \
                    "(variables: {}, outcomes: {}, probabilities: {})".format(variables, outcomes, potentials))
        if variables is None:
            variables = []
        if outcomes is None:
            outcomes = {}
        if potentials is None:
            potentials = 1
        #Store the actual potentials as numpy array
        self.potentials = np.copy(potentials)
        #Store all contained variables in a list. The index of each variable
        #corresponds to the dimension of that variable in the array.
        self.variable_order = list(variables)
        # Use a dictionary for the outcomes (as tuple) with the variables as keys.
        self.outcomes = {}
        for v,o in outcomes.items():
            self.outcomes[v] = tuple(o)
    
    
    # @classmethod is a decorator, that changes an object's function, so that
    # instead of it getting the object instance as the first argument
    # (usually references as "self"), a reference to the actual class, i.e. 
    # Factor in this case is passed as first argument (one usually denotes this
    # as "cls") instead. cls will therefore be equivalent to "Factor" (i.e. 
    # the class), which allows one to create a new instance of a factor by using
    # new_factor = cls(), which can then be returned.
    # For those interested on this: 
    # https://julien.danjou.info/blog/2013/guide-python-static-class-abstract-methods
    @classmethod
    def from_probabilities(cls, variables: List[str], 
                                outcomes: Dict[str, List[str]], 
                                probabilities: np.array):
        """
            Classmethod to directly create a new factor from variables, 
            their outcomes and according conditional or marginal probabilities.
            
            Parameters
            ----------
            variables: [String,] 
                A list containing the variable names of all variables this 
                factor should represent.
            outcomes: dict 
                A dictionary containing the variable names as keys and a list
                containing the possible outcomes of said variable as values.
            probabilities: np.array 
                A multidimensional array containing the conditional or marginal
                probabilities of a random variable. The array should be ordered
                according to the variable and outcome lists.
                
            Returns
            -------
            Factor
                The factor over the specified variables with potentials 
                initialized to the given probabilities.
        """
        return cls(variables, outcomes, probabilities)
    
    @classmethod
    def from_node(cls, node: DiscreteVariable):
        """
            Classmethod to directly create a new factor from a DiscreteVariable
            
            Parameters
            ----------
            node: ccbase.nodes.DiscreteVariable
                The DiscreteVariable that should be used to initialize this
                factor.
                
            Returns
            -------
            Factor
                The factor over the specified variables with potentials 
                initialized to the given probabilities.
        """
        variables = [node.name] + node.parent_order
        outcomes = {node.name: node.outcomes}
        for p in node.parent_order:
            outcomes[p] = node.parents[p].outcomes
        return cls(variables, outcomes, node.cpt)
    
    def __call__(self, instantiation: Dict[str, str]) -> Union[float, np.array]:
        """
            Returns the current potential for the specified instantiation of 
            all contained variables by calling the potential function.
            
            Parameters
            ----------
            instantiations: dict
                A dictionary containing the variable names as keys and their
                desired instantiation as value.
                
            Returns
            -------
            float or np.array
                The potential for that specified instantiation. In case of
                partial instantiations, a np.array is returned instead
        """
        return self.potential(instantiation)
        
    def potential(self, instantiation: Dict[str, str]) -> Union[float, np.array]:
        """
            Returns the current potential for the specified instantiation of 
            all contained variables.
            
            Parameter
            --------
            instantiation: dict
                A dictionary containing the variable names as keys and their
                desired instantiation as value.
                
            Returns
            -------
            float or np.array
                The potential for that specified instantiation. In case of
                partial instantiations, a np.array is returned instead.
        """
        
        #Construct the index for the desired potential
        index = []        
        for v in self.variable_order:
            if v in instantiation:
                try:
                    index.append([self.outcomes[v].index(instantiation[v])])
                except ValueError:
                    raise ValueError("There is no potential for variable {} " + \
                                     "with outcomes {} in this factor.".format(v, instantiation[v]))
            else:
                index.append(range(len(self.outcomes[v])))
                    
        #np.ix_ constructs an access mask which allows efficient access
        #to the desired cells. This approach allows underspecification of the
        #instantiation (i.e. not all variables are specified) which will
        #result in returning a matrix for the remaining variables
        return np.squeeze(np.copy(self.potentials[np.ix_(*index)]))
        
    def marginalize(self, variables: List[str]) -> Factor:
        """
            Creates a new factor where the specified variables are summed out.
            
            Parameters
            ----------
            variables: [String,]
                A list containing the names of all the variables that should be
                summed out.
                
            Returns
            -------
            Factor
                A factor where the specified variables have been summed out 
                from this factor.
        """
        if not isinstance(variables, (list,set)):
            variables = [variables]
            
        res = self.copy()
        for v in variables:
            #Simply sum out the corresponding dimension for each variable
            res.potentials = np.sum(res.potentials, axis=res.variable_order.index(v))
            #Make sure to upadte the outcome dictionary and variable_order list
            # as to not mess up the next iteration.
            del res.outcomes[v]
            res.variable_order.remove(v)
            
        return res

    def multiply(self, other_factor: Factor) -> Factor:
        """
            Creates a new factor, which is the resulting product of multiplying
            this factor with the given other factor. The initial factors are
            not modified.

            Parameters
            ----------
                other: Factor
                    The factor to multiply this factor with.

            Returns
            -------
            Factor
                The resulting factor.
        """
        # Shortcuts for trivial factors
        if len(self.variable_order) == 0:
            res = other_factor.copy()
            res.potentials = self.potentials * res.potentials
            return res
            
        if len(other_factor.variable_order) == 0:
            res = self.copy()
            res.potentials = res.potentials * other_factor.potentials
            return res
        
        res = Factor()
        res.variable_order = list(self.variable_order)
        res.outcomes = dict(self.outcomes)
        
        # Compute the variables that are not yet contained in this factor
        extra_vars = set(other_factor.variable_order) - set(self.variable_order)
        #Setup res factor based on self, extended by the missing variables from other
        if extra_vars:
            #Create new dimensions for each missing variable, using slice-objects
            #and np.newaxis
            slice_ = [slice(None)] * len(self.variable_order)
            slice_.extend([np.newaxis] * len(extra_vars))
            res.potentials = self.potentials[tuple(slice_)]
            
            res.variable_order.extend(extra_vars)
            
            #Update the outcome dictionary for the new variables!
            for var in extra_vars:
                res.outcomes[var] = tuple(other_factor.outcomes[var])
                
        else:
            #This view is ok, since we will overwrite res.potentials below 
            #when we compute the actual multiplication!
            res.potentials = self.potentials[:]
            
        #modify other_factor:
        #In the end we simply want to multiply to matrices cell wise, for that
        #these matrices need to have the same shape!
        f2 = other_factor.copy()
        extra_vars = set(res.variable_order) - set(f2.variable_order)
        if extra_vars:
            slice_ = [slice(None)] * len(f2.variable_order)
            slice_.extend([np.newaxis] * len(extra_vars))
            f2.potentials = f2.potentials[tuple(slice_)]
            #We update the variable order here because we need the swap indices
            #next
            f2.variable_order.extend(extra_vars)
            
        #Rearrange f2 potentials so that dimensions align to the order in res
        swaparray = [f2.variable_order.index(var) for var in res.variable_order]
        f2.potentials = np.transpose(f2.potentials, swaparray)
        
        # Pointwise multiplication which results in a factor where all instantiations
        # are compatible to the instantiations of res and factor2
        # See Definition 6.3 in "Modeling and Reasoning with Bayesian Networks" - Adnan Darwiche Chapter 6    
        res.potentials = res.potentials * f2.potentials
        
        return res

    def __mul__(self, other: Factor) -> Factor:
        """
            Overwrite the internal __mul__ operator to allow using special
            character "*", as in f1 * f2 instead of f1.multiply(f2).
            This does not change the initial factors but creates a new factor
            as the resulting product.

            Parameters
            ----------
            other: Factor
                The factor to multiply this factor with.

            Returns
            -------
            Factor
                The resulting factor.
        """
        return self.multiply(other)

    def reduce(self, evidence: Dict[str, str]) -> Factor:
        """
            Creates a new factor which has been reduced to conform to the 
            provided evidence.
            
            Parameters
            ----------
            evidence: dict
                A dictionary containing variable:outcome pairs specifying the
                evidence.
                
            Returns
            -------
            Factor
                A factor that has been reduced to conform to the given 
                evidence.
        """
        #Note: There are multiple ways to represent a reduced factor, make 
        # sure that all other functions can still be used, even on reduced 
        # factors.
        
        # This solution is a somewhat inefficient solution, where reduced 
        # computations are not more efficient then non-reduced computations
        # since we do not prune empty cells from the matrix, thus not changing
        # the actual size.
        
        #Construct the index for the desired potential
        res = self.copy()
        index = []        
        for v in self.variable_order:
            if v in evidence:
                try:
                    index.append([self.outcomes[v].index(evidence[v])])
                except ValueError:
                    raise ValueError("There is no potential for variable {} " + \
                                     "with outcomes {} in this factor.".format(v, evidence[v]))
            else:
                index.append(range(len(self.outcomes[v])))
                    
        #We use here the same logic as in the potential function, as this already
        #allows partial instantiations, as is the case with the evidence here.
        #We use the access mask provided by np.ix_ to prevent the cells conforming
        #to the evidence from being multiplied by 0.
        tmp = np.zeros(res.potentials.shape)
        tmp[np.ix_(*index)] = 1
        res.potentials *= tmp
        return res
        
    def copy(self) -> Factor:
        """
            Creates a (deep) copy of this factor.
            
            Returns
            -------
            Factor
                An exact copy of self.
        """
        res = Factor()
        res.potentials = np.copy(self.potentials)
        #Creating a shallow copy with dict() is enough here as factors
        #should convert the value lists to tuples upon creation, which makes
        #modification of these lists impossible.
        res.outcomes = dict(self.outcomes)
        res.variable_order = list(self.variable_order)
        return res

