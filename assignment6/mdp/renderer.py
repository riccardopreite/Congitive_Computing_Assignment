#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 16:59:03 2017
Module containing simple "renderers" for the MDP code. Can print the
grid, including an agent, the utilities as well as the resulting policy.
Contains a simple console renderer that tries to pretty_print the different
results and a matplotlib based renderer that actually plots with colors.

Both renderers are currently working with rewards between -1 and 1. Other rewards
might confuse the renderers with the walls, which are currently represented as
-2.

@author: jpoeppel
Last modified: January, 12th 2022
"""

from __future__ import annotations, print_function
from typing import Optional, List, Tuple, Dict

try:
    import matplotlib
    matplotlib.use("TKAgg")
    import matplotlib.pyplot as plt
    
    matplotlibAvailable = True
except ImportError:
    matplotlibAvailable = False
    
import time

from .gridworld import WALL, GROUND

import sys


#Check for Python 2, because the arrow unicode escape characters are not 
#detected properly in Python 2
if sys.version[0] == "3":
    POLICY_MAP = {"N":"\u2191", "S":"\u2193", "E":"\u2192", "W":"\u2190"}
else:
    POLICY_MAP = {"N":"N", "S":"S", "E":"E", "W":"W"}

class ConsoleRenderer(object):
    """
        Simple experimental "renderer" which represents a gridworld in the 
        console. Can be used when matplotlib is not installed, but not work
        properly for all cases!
    """
    
    def __init__(self):
        """
            Hardcodes the symbols used for different grid-representations.
        """
        self.map = {WALL:"  ##  ", GROUND: " "*6}
    
    def plot(self, grid: List[List[int]], agent: Tuple[int,int]):
        """
            Pretty prints the gridworld and the agent.
            
            Parameters
            ---------
            grid: list of lists
                A list of lists representing the gridworld. -1 is used for 
                walls or obstacles, and 0 for passable fields.

            agent: tuple
                A tuple representing the current agent position.
        """
        grid = grid[::-1]
        rowOff = len(grid)-1
        for j, row in enumerate(grid):
            s = ""
            for i, cell in enumerate(row):
                if (i,rowOff-j) == agent:
                    s += "  AA  "
                else:
                    #If we have a value that is not in the mapping, just display
                    #that value
                    s += self.map.get(cell, "  {}  ".format(cell))
            print(s+"\n")
            
    def pause(self, duration: float):
        """
            Stops the executation for the given duration to be able to look
            at the current visualiation.
            
            Parameters
            ----------
            duration: float
                Duration of the pause in seconds.
        """
        time.sleep(duration)
            
    def plot_utilities(self, utils: Dict[Tuple[int,int], float], iteration: int, walls: Optional[bool] = False):
        """
            Pretty prints the utilities in a grid-like structure.
            If walls is True, it will add outer walls.
            
            Parameters
            ----------
            utils: dict(tuple:float)
                A dictionary containing state: expected utility pairs.

            iteration: int
                The current iteration in which these utilities where computed.

            walls: bool, optional
                If given, will print additional walls around the grid.
        """
        width, height = 0, 0
        for (i,j) in utils:
            width = max(width, i+1)
            height = max(height, j+1)
            
        gridLists = [[None]*width for i in range(height)]
        
        for (i,j), val in utils.items():
            gridLists[j][i] = val
            
            
        # Invert rows because we want to have the 0th row at the bottom
        gridLists = gridLists[::-1] 
        print("Iteration: ", iteration)
        if walls:
            print("  ##  " * (width+2))
            print()
            
        for row in gridLists:
            if walls:
                s = "  ##  "
            else:
                s = ""
            for cell in row:
                s += " {:0.2f} ".format(cell) if cell != None else "      "
            if walls:
                s += "  ##  "
            print(s+"\n")
            
        
        if walls:
            print("  ##  " * (width+2))
            
            
    def plot_policy(self, policy: Dict[Tuple[int,int], str], walls: Optional[bool] = False):
        """
            Pretty prints a policy in a grid-like structure.
            If walls is True, it will add outer walls.
            
            Parameters
            ----------
            policy: dict(tuple:string)
                A dictionary containing state: action pairs.

            walls: bool, optional
                If given, will print additional walls around the grid.
        """
        width, height = 0, 0
        for (i,j) in policy:
            width = max(width, i+1)
            height = max(height, j+1)
            
        gridLists = [[None]*width for i in range(height)]
        
        for (i,j), val in policy.items():
            gridLists[j][i] = val
            
        # Invert rows because we want to have the 0th row at the bottom
        gridLists = gridLists[::-1] 
            
        if walls:
            print("  #  " * (width+2))
            print()
            
        for row in gridLists:
            if walls:
                s = "  #  "
            else:
                s = ""
            for cell in row:
                s += "  {}  ".format(POLICY_MAP.get(cell, " "))
            if walls:
                s += "  #  "
            print(s+"\n")
        
        if walls:
            print("  #  " * (width+2))
        
        
                
            
class MatplotlibRenderer(object):
    """
        A simple matplotlib renderer for gridworlds. Needs to have matplotlib
        installed!
    """
    
    def __init__(self):
        plt.ion()
        plt.rcParams['toolbar'] = 'None'
        self.fig = self.ax = None
        self.cm = plt.cm.jet
        self.cm = matplotlib.colors.LinearSegmentedColormap.from_list(
                                "mycmap", ["gray","red", "white", "green"])
        self.texts = []
        self.arrows = []
        self.mesh = None
        
    def _setup_figure(self):
        """
            Prepares the figure to draw on and the agent sprite.
        """
        self.fig, self.ax = plt.subplots()
        self.ax.get_xaxis().set_visible(False)
        self.ax.get_yaxis().set_visible(False)
        self.agent = plt.Circle((0,0), radius = 0.4, color='y')
        
    def plot(self, grid: List[List[int]], agent: Tuple[int,int]):
        """
            Plots the grid and the agent position using matplotlibs 
            pcolormesh.
            
            Parameters
            ---------
            grid: list of lists
                A list of lists representing the gridworld. -1 is used for 
                walls or obstacles, and 0 for passable fields.

            agent: Tuple
                A tuple representing the current agent position.
        """
        
        if self.fig is None:
            self._setup_figure()
        
        plt.title("Agent is trying to reach the goal")
        self.ax.pcolormesh(grid, cmap = self.cm)
        self.agent.center = (agent[0]+0.5, agent[1]+0.5)
        
        self.ax.add_artist(self.agent)
        plt.draw()
        
    def pause(self, duration: float):
        """
            Stops the executation for the given duration to be able to look
            at the current visualiation.
            
            On some systems/backends, plt.pause might raise a DeprecatedWarning,
            the official solution is to use interaction and time.sleep directly,
            but at least for me, the figure will not be updated in this which
            is why I am using this here.
            
            Parameters
            ----------
            duration: float
                Duration of the pause in seconds.
        """
        plt.pause(duration)
            
    def plot_utilities(self, utils: Dict[Tuple[int,int], float], iteration: int, walls: Optional[bool] = False):
        """
            Plots the utilities on top of the grid. 
            If walls is True, it will add outer walls.
            
            Parameters
            ----------
            utils: dict(tuple:float)
                A dictionary containing state: expected utility pairs.

            iteration: int
                The current iteration in which these utilities where computed.       

            walls: bool, optional
                If given, will print additional walls around the grid.
        """
        
        if self.fig is None:
            self._setup_figure()
        
        width, height = 0, 0
        for (i,j) in utils:
            width = max(width, i+1)
            height = max(height, j+1)
            
        offs = 0
        if walls:
            width += 2
            height += 2
            offs = 1
            
        gridLists = [[WALL]*width for i in range(height)]
        
        for (i,j), val in utils.items():
            gridLists[j+offs][i+offs] = val
            
        self.mesh = self.ax.pcolormesh(gridLists, cmap = self.cm)
        
        plt.title("Iteration {}".format(iteration))
        for t in self.texts:
            t.remove()
        self.texts = []
        if walls:
            offs = 1.5
        else:
            offs = 0.5
        for (i,j), cell in utils.items():
            self.texts.append(self.ax.text(i+offs,j+offs, 
                                "{:0.2f}".format(cell), 
                                color="b", ha="center", va="center"))
        
        plt.draw()
        
        
    def plot_policy(self, policy: Dict[Tuple[int,int], str], walls: Optional[bool] = False):
        """
            Pretty prints a policy in a grid-like structure.
            If walls is True, it will add outer walls.
            
            Parameters
            ----------
            policy: dict(tuple:string)
                A dictionary containing state: action pairs.

            walls: bool, optional
                If given, will print additional walls around the grid.
        """
        
        if self.fig is None:
            self._setup_figure()
            
        #If the mesh has not already been plotted, we create a gridlist
        #from the policy values to display at least a map representing
        #the ground and walls.
        if self.mesh is None:
            width, height = 0, 0
            for (i,j) in policy:
                width = max(width, i+1)
                height = max(height, j+1)
                
            offs = 0
            if walls:
                width += 2
                height += 2
                offs = 1
                
            gridLists = [[WALL]*width for i in range(height)]
            
            for (i,j), val in policy.items():
                gridLists[j+offs][i+offs] = GROUND
                
            cm = matplotlib.colors.LinearSegmentedColormap.from_list(
                                    "mycmap", ["gray","red", "white"])
                
            #We need a different colormap here since we have no information about 
            #the utilities at this point
            self.mesh = self.ax.pcolormesh(gridLists, cmap = cm)
        
        plt.title("Policy map")
        for a in self.arrows:
            a.remove()
        self.arrows = []
        if walls:
            offs = 1.5
        else:
            offs = 0.5
        for (i,j), cell in policy.items():
            self.arrows.append(self.ax.text(i+offs,j+offs-0.25, 
                                "{}".format(POLICY_MAP[cell]), 
                                color="b", ha="center", va="center"))
        plt.draw()
    
    
def show():
    if matplotlibAvailable:
        plt.ioff()
        plt.show()