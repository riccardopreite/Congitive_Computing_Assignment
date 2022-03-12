#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 10:59:58 2017
A module containing two classes to represent a simple 2D gridworld.
@author: jpoeppel
Last modified: January, 12th 2022
"""
from __future__ import annotations
from typing import Union, Optional, List, Tuple, Set

PASSABLES = {"g": True, "#": False}

WALL = -2
GROUND = 0

class Tile(object):
    """
        Minimal class representing a grid/tile in the gridworld.
        Consists of a position in the 2d grid, a flag specifying if it is 
        passable or not as well as a set of neighbours.
    """
    
    def __init__(self):
        self.pos = (0,0)
        self.passable = True
        self.neighbours = set([])
        
    @classmethod
    def get_wall(cls) -> Tile:
        """
            Classmethod to return a dummy tile which is not passable. Is used
            as default value in the gridworld, when someone tries to access
            a tile position, which is out of bounds.
        """
        res= cls()
        res.passable = False
        return res

class Gridworld(object):
    """
        A simple class representing 2D gridworlds consisiting of different
        tiles which can be passable or not.
    """
    
    def __init__(self):
        self.tiles = {}
        self.size = 0
        
    def parse_environment(self, env_string: str, get_passable_states: Optional[bool] = False) -> Union[None, List[Tuple(int)]]:
        r"""
            Parses an environment string, containing "#" for walls and "g"
            for ground/free space. Rows are separated by "\n". Although it
            is not checked, but the provided world string should have a 
            rectangular shape.
            
            
            Parameters
            ---------
            env_string: str
                A string representation of the gridworld containing '#','g' and
                '\n'.
            get_passable_states: bool, optional
                If given, a list of all parsed passable states is returned, 
                which can be used as state-space for an MDP. Default: False
                
            Returns
            -------
            list
                A list of passable states (as position tuples) if get_passable_states
                 was specified, otherwise returns None.
        """
        states = []
        for j, row in enumerate(env_string.split("\n")[::-1]):
            for i, element in enumerate(row):
                tile = Tile()
                tile.pos = (i,j)
                tile.passable = PASSABLES[element]
                self.tiles[tile.pos] = tile
                if tile.passable:
                    states.append(tile.pos)
        
        #Pretty bad hack, but should work since the string represents
        #the world from top left to bottom right
        maxPos = (i,j)
        #Add all neighbours
        for tile in self.tiles.values():
            for i,j in [(-1,0),(1,0),(0,-1),(0,1)]:
                newPos = (min(max(tile.pos[0]+i,0), maxPos[0]), 
                          min(max(tile.pos[1]+j,0),maxPos[1]))
                tile.neighbours.add(self.tiles[newPos])
        self.size = (maxPos[0]+1,maxPos[1]+1)
        if get_passable_states:
            return states
        
    def get_neighbour_states(self, pos: Tuple[int,int]) -> Set[Tuple[int,int]]:
        """
            Computes all reachable positions of the given position.
            If a neighbour is of the given position is not passable (i.e.
            it is an obstacle/wall), the current position will be added to the
            resulting set.
            
            Parameters
            ----------
            pos: tuple
                The current state
        
            Returns
            --------
            set(tuple)
                All reachable neighbour positions/states.
        """
        res = set([])
        for n in self.tiles[pos].neighbours:
            if not n.passable:
                res.add(pos)
            else:
                res.add(n.pos)
        return res
    
    
    def get_grid_representation(self, add_outer: Optional[bool] = False) -> List[List[int]]:
        """
            Creates a grid representation of the world in the form
            of a list of lists. Walls will be represented by -1 and free
            spaces by 0s.
            
            Parameters
            ----------
            add_outer: bool, optional
                If true, will add an outer ring of walls around the environment.
                
            Returns
            -------
            list of lists
                WALL/GROUND (-2/0) representation of the world in a 2d list.
        """
        res = []
        if add_outer:
            res.append([WALL]*(self.size[0]+2))
        for j in range(self.size[1]):
            tmp = []
            
            if add_outer:
                tmp.append(WALL)
                
            for i in range(self.size[0]):
                if self.tiles[(i,j)].passable:
                    tmp.append(GROUND)
                else:
                    tmp.append(WALL)
            
            if add_outer:
                tmp.append(WALL)
            res.append(tmp)
        
        if add_outer:
            res.append([WALL]*(self.size[0]+2))
        return res
    
    def check_passable(self, position: Tuple[int,int]) -> bool:
        """
            Will check if the given position is a passable tile or not.
            For positions out of bounds this will return False.
            
            Parameters
            ---------
            position: tuple
                The position to be checked
                
            Returns
            -------
            bool
                True, if the position is contained in this gridworld and the 
                corresponding tile is passable, False otherwise
        """
        return self.tiles.get(position, Tile.get_wall()).passable
    
    def act(self, start_pos: Tuple[int,int], action: str) -> Tuple[int,int]:
        """
            Computes the action of an agent that performs the given action from
            the given start position. This will be the new position according
            to the action as long as the agent can reach the new position (i.e.
            there is no wall), otherwise this will be the start position.

            Parameters
            ---------
            start_pos: tuple
                The position from which to perform the given action.

            action: str
                The action to be performed.

            Returns
            -------
            tuple
                The resulting position when executing the action from the
                given position.
        """
        if action == "N":
            dif= (0,1)
        if action == "S":
            dif = (0,-1)
        if action == "E":
            dif = (1,0)
        if action == "W":
            dif = (-1,0)
        new_pos = (start_pos[0]+dif[0], start_pos[1]+dif[1])
        if self.check_passable(new_pos):
            return new_pos 
        else:
            return start_pos