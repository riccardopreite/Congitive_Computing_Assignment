"""
Some test cases in a similar way to the ones used for grading your submissions.
The actual grading will test many corner cases not considered here.
Feel free to add more complex test cases here.
More information about the used testing framework can be found in the LernraumPlus as
well as the tutorial sessions.
This makes use of the unittest framework.
These tests use the values you already now from the lecture slides and/or the 
assignment sheet. You should experiment with different decision trees and
environments to make sure your solution works properly.

author: Jan Pöppel
last modified. 12.01.2022
"""

import unittest
import assignment6 as solution

class TestAssignment6(unittest.TestCase):

    ## Decision Tree Examples from the lecture
    def test_utility_node_get_eu(self):
        dt = solution.get_simple_dt()
        un = dt.nodes["Party:yes,Rain:no"]
        self.assertEqual(un.get_eu(), 500)

    def test_chance_node_get_eu(self):
        dt = solution.get_simple_dt()
        cn = dt.nodes["Party:yes,Rain"]
        self.assertEqual(cn.get_eu(), 140)

    def test_action_node_get_eu(self):
        dt = solution.get_simple_dt()
        an = dt.nodes["Party"]
        self.assertEqual(an.get_eu(), 140)
        self.assertEqual(an.best_action, "yes", "The best action for the node is 'yes'.")


    ## MDP
    def test_value_iteration(self):
        self.maxDiff = None
        environment, states, initial_state, reward_function = solution.testWorld1()
        accuracy = 0.8
        ratio = 0.5 #Both accidental directions are equally likely
        actions= ["N","S","E","W"]
        terminals = None
        #Set up our simple transition model with the specified parameters
        trans = solution.SimpleTransitionModel(accuracy, environment, ratio=ratio)
        discount = 0.9 #1
        #Set up our actual Markov Decision Process with all required variables
        mdp = solution.MarkovDecisionProcess(environment, list(states), initial_state, actions, 
                                    trans, dict(reward_function), discount, terminals)   

        utilities = mdp.value_iteration(num_max_iterations=1000, epsilon=0.0001, plot_delay=0.01)

        # Terminal rewards should not change
        self.assertEqual(utilities[(3,2)], 1)
        self.assertEqual(utilities[(3,1)], -1)
        # Utility of starting position as shown on the assignment.
        # IF this fails by a small margin, your solution may still be correct.
        # We did encounter small numerical variations on different systems before.
        self.assertAlmostEqual(utilities[(0,0)], 0.49, 1)


    def test_get_policy(self):
        environment, states, initial_state, reward_function = solution.testWorld1()
        accuracy = 0.8
        ratio = 0.5 #Both accidental directions are equally likely
        actions= ["N","S","E","W"]
        terminals = None
        #Set up our simple transition model with the specified parameters
        trans = solution.SimpleTransitionModel(accuracy, environment, ratio=ratio)
        discount = 0.9 
        #Set up our actual Markov Decision Process with all required variables
        mdp = solution.MarkovDecisionProcess(environment, states, initial_state, actions, 
                                    trans, reward_function, discount, terminals)   
        utilities = mdp.value_iteration(num_max_iterations=1000, epsilon=0.0001, plot_delay=0.01)
        policy = mdp.get_policy(utilities)

        # Right before the terminal state we want to go east!
        self.assertEqual(policy[(2,2)], "E")



if __name__ == "__main__":
    unittest.main()
        