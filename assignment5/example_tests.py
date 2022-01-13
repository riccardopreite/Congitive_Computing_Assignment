"""
Some test cases in a similar way to the ones used for grading your submissions.
The actual grading will test many corner cases not considered here.
Feel free to add more complex test cases here.
More information about the used testing framework can be found in the LernraumPlus as
well as the tutorial sessions.
This makes use of the unittest framework.
In general, testing approximate sampling is a lot more tricky than other assignments
as there is randomness in the approximate methods, these tests thus may
report failures due to slight inaccuracies. I will need to manually
revise each submission manually regardless of test outcome but you can still
check if your solution works in general. 

author: Jan Pöppel
last modified. 23.11.2021
"""

import unittest
import random
import assignment5 as solution

import numpy as np

class TestAssignment5(unittest.TestCase):

    def get_trivial_net(self):
        net = solution.BayesianNetwork()
        a = solution.DiscreteVariable("A", ["True", "False"])
        b = solution.DiscreteVariable("B", ["True", "False"])
        c = solution.DiscreteVariable("C", ["True", "False"])
        d = solution.DiscreteVariable("D", ["True", "False"])
        net.add_node(a)
        net.add_node(b)
        net.add_node(c)
        net.add_node(d)
        net.add_edge(b,a)
        net.add_edge(c,b)
        net.add_edge(b,d)
        a.set_probability_table(np.array([[0.2,0.3],[0.8,0.7]]))
        b.set_probability_table(np.array([[0.6,0.8],[0.4,0.2]]))
        c.set_probability_table(np.array([0.4,0.6]))
        d.set_probability_table(np.array([[0.4,0.2],[0.6,0.8]]))
        return net

    def test_sample(self):
        net = solution.get_wetgrass_network()
        nodes = list(net.nodes.keys())
        node = net.nodes[random.choice(nodes)]
        evidence = {}
        for p in node.parents:
            evidence[p] = random.choice(list(node.parents[p].outcomes))
        distr = node.get_distribution(evidence)
        num_samples = 10000
        samples = []
        for i in range(num_samples):
            samples.append(solution.sample(distr))

        outcome = random.choice(list(distr.keys()))
        counts = len([i for i in filter(lambda x: x == outcome, samples)])
        self.assertAlmostEqual(counts/num_samples, distr[outcome], 1, "Sample frequency not matching actual distribution")

    def test_get_ancestral_ordering(self):
        net = solution.get_wetgrass_network()
        ancestral_ordering = solution.get_ancestral_ordering(net)
        for i,n in enumerate(ancestral_ordering):
            for n2 in ancestral_ordering[i+1:]:
                self.assertFalse(net.is_ancestor(n2,n))


    def test_do_forward_sampling(self):
        net = solution.get_wetgrass_network()
        query = "sprinkler"
        query_node = net.nodes[query]
        num_samples = 1000
        true_res = net.marginals(query)
        res = solution.do_forward_sampling(net, query, num_samples)
        for i, outcome in enumerate(query_node.outcomes):
            self.assertAlmostEqual(res[outcome], true_res[i], 1, "Probability for {} wrong.".format(outcome))

    def test_get_markov_distr_simple(self):
        net = self.get_trivial_net()
        a = net.nodes["A"]
        evidence = {"A":"True", "B":"False", "C":"True", "D":"False"}
        true_distr = {"True": 0.3, "False": 0.7}
        distr = solution.get_markov_distr(a, evidence)
        norm = sum(distr.values())
        distr = {k:v/norm for k,v in distr.items()}
        for key in distr:
            self.assertAlmostEqual(distr[key], true_distr.get(key,0), 5, "The local distr for A={} needs to be this".format(key))

    def test_do_gibbs_sampling(self):
        net = solution.get_wetgrass_network()
        query = "sprinkler"
        query_node = net.nodes[query]
        num_samples = 1000
        evidence = {}
        true_res = net.marginals(query)
        res = solution.do_gibbs_sampling(net, query, evidence, num_samples)
        for i, outcome in enumerate(query_node.outcomes):
            self.assertAlmostEqual(res[outcome], true_res[i], 1, "Probability for {} wrong.".format(outcome))

    def test_expected_utility(self):
        utilities = {"wet_grass": [20,-10], "dry_fields": [-20, 10]}
        net = solution.get_wetgrass_network()
        eu_sprinkler_no_do_no_winter_False = solution.expected_utility(net, {"sprinkler":"True"}, {}, utilities, use_do=False)
        print("sprinkler=True,  use_do=False,  evidence={''}:",eu_sprinkler_no_do_no_winter_False)
        eu_sprinkler_no_do_winter_False = solution.expected_utility(net, {"sprinkler":"True"}, {"winter":"False"}, utilities, use_do=False)
        print("sprinkler=True,  use_do=False,  evidence={'winter:false'}:",eu_sprinkler_no_do_winter_False)


        eu_not_sprinkler_no_do_no_winter_False = solution.expected_utility(net, {"sprinkler":"False"}, {}, utilities, use_do=False)
        print("sprinkler=False,  use_do=False,  evidence={''}:",eu_not_sprinkler_no_do_no_winter_False)
        eu_not_sprinkler_no_do_winter_False = solution.expected_utility(net, {"sprinkler":"False"}, {"winter":"False"}, utilities, use_do=False)
        print("sprinkler=False,  use_do=False,  evidence={'winter:false'}:",eu_not_sprinkler_no_do_winter_False)

        eu_sprinkler_do_no_winter_False = solution.expected_utility(net, {"sprinkler":"True"}, {}, utilities, use_do=True)
        print("sprinkler=True,  use_do=True,  evidence={''}:",eu_sprinkler_do_no_winter_False)
        eu_sprinkler_do_winter_False = solution.expected_utility(net, {"sprinkler":"True"}, {"winter":"False"}, utilities, use_do=True)
        print("sprinkler=True,  use_do=True,  evidence={'winter:false'}:",eu_sprinkler_do_winter_False)

        eu_not_sprinkler_do_no_winter_False = solution.expected_utility(net, {"sprinkler":"False"}, {}, utilities, use_do=True)
        print("sprinkler=False,  use_do=True,  evidence={''}:",eu_not_sprinkler_do_no_winter_False)
        eu_not_sprinkler_do_winter_False = solution.expected_utility(net, {"sprinkler":"False"}, {"winter":"False"}, utilities, use_do=True)
        print("sprinkler=False,  use_do=True,  evidence={'winter:false'}:",eu_not_sprinkler_do_winter_False)
        
        self.assertTrue(True, "I will not provide the correct result here, as this is part of the assignment.")

if __name__ == "__main__":
    unittest.main()
        