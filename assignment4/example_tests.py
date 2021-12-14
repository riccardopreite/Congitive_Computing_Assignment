"""
Some test cases in a similar way to the ones used for grading your submissions.
The actual grading will test many corner cases not considered here.
Feel free to add more complex test cases here.
More information about the used testing framework can be found in the LernraumPlus as
well as the tutorial sessions.
This makes use of the unittest framework

author: Jan Pöppel
last modified. 23.11.2021
"""

import unittest
import assignment4 as solution

import numpy as np

class TestAssignment4(unittest.TestCase):

    def get_trivial_net(self):
        net = solution.BayesianNetwork()
        a = solution.DiscreteVariable("A", ["True", "False"])
        b = solution.DiscreteVariable("B", ["True", "False"])
        net.add_node(a)
        net.add_node(b)
        net.add_edge(b,a)
        a.set_probability_table(np.array([[0.2,0.3],[0.8,0.7]]))
        b.set_probability_table(np.array([0.4,0.6]))
        return net


    def test_initialize_factors(self):
        net = self.get_trivial_net()
        factors = solution.initialize_factors(net, None)
        self.assertEqual(len(factors), len(net.nodes))

    def test_sum_product_elim_var(self):
        f1 = solution.Factor(["A","B"], {"A":["True","False"], "B": ["True","False"]}, np.array([[0.2,0.3],[0.8,0.7]]))
        f2 = solution.Factor(["B"], {"B": ["True","False"]}, np.array([0.4,0.6]))
        res = solution.sum_product_elim_var([f1,f2], "B")
        self.assertEqual(len(res), 1)
        # Using almost equal to avoid rounding/precision errors
        np.testing.assert_almost_equal(res[0].potentials, np.array([0.26, 0.74]))

    def test_calculate_probabilities_single_no_evidence(self):
        net = self.get_trivial_net()
        nodes = list(net.nodes)
        true_res = {"A": np.array([0.26, 0.74]), "B": np.array([0.4, 0.6])}
        for n in nodes:
            res = solution.calculate_probabilities(net, [n])
            np.testing.assert_almost_equal(res.potentials, true_res[n])

    def test_calculate_probabilities_evidence(self):
        net = self.get_trivial_net()
        res = solution.calculate_probabilities(net, ["A"], {"B":"False"})
        np.testing.assert_almost_equal(res.potentials, np.array([3/10, 7/10]))

    def test_maximize_out(self):
        f = solution.Factor(["A","B"], {"A":["True","False"], "B": ["True","False"]}, np.array([[0.2,0.3],[0.8,0.7]]))
        res = solution.maximize_out(f, "B")
        np.testing.assert_almost_equal(res.potentials, np.array([0.3, 0.8]))

    def test_max_product_elim_var(self):
        f1 = solution.Factor(["A","B"], {"A":["True","False"], "B": ["True","False"]}, np.array([[0.2,0.3],[0.8,0.7]]))
        f2 = solution.Factor(["B"], {"B": ["True","False"]}, np.array([0.4,0.6]))
        res_list, res_f = solution.max_product_elim_var([f1,f2], "B")
        self.assertEqual(len(res_list), 1)
        np.testing.assert_almost_equal(res_list[0].potentials, np.array([0.18, 0.42]))
        np.testing.assert_almost_equal(res_f.potentials, np.array([[0.08, 0.18], [0.32, 0.42]]))

    def test_traceback(self):
        max_a_factor = solution.Factor(["A"], {"A": ["True","False"]}, np.array([0.18,0.42]))
        max_b_factor = solution.Factor(["A","B"], {"A":["True","False"], "B": ["True","False"]}, np.array([[0.08, 0.18], [0.32, 0.42]]))
        res = solution.traceback({"A": max_a_factor, "B": max_b_factor}, ["B", "A"])
        self.assertEqual(res, {"A": "False", "B":"False"})

    def test_calculate_MAP(self):
        net = self.get_trivial_net()
        res_prob, res_map = solution.calculate_MAP(net)
        self.assertEqual(res_prob, 0.42)
        self.assertEqual(res_map, {"A": "False", "B":"False"})

if __name__ == "__main__":
    unittest.main()
        