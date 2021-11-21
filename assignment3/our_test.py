"""
Some test cases in a similar way to the ones used for grading your submissions.
The actual grading will test many corner cases not considered here.
Feel free to add more complex test cases here.
More information about the used testing framework can be found in the LernraumPlus as
well as the tutorial sessions.
This makes use of the unittest framework

author: Jan Pöppel
last modified. 11.11.2021
"""

import unittest
import assignment3 as solution
from ccbase.networks import Graph

class TestAssignment3(unittest.TestCase):


    def test_find_forks(self):
        graph = self._create_example_graph()
        forks = solution.find_forks(graph)
        # Ensure we allow both string and node returns
        try:
            forks = [n.name for n in forks]
        except AttributeError:
            pass 

        self.assertEqual(set(forks), {"E"}, "Incorrect forks found.")

    def test_find_chains(self):
        graph = self._create_example_graph()
        chains = solution.find_chains(graph)
        # Ensure we allow both string and node returns
        try:
            chains = [n.name for n in chains]
        except AttributeError:
            pass 
        self.assertEqual(set(chains), set([]), "The graph does not have chains.")
        # Let us add achain
        graph.add_edge("R", "A")
        chains = solution.find_chains(graph)
        # Ensure we allow both string and node returns
        try:
            chains = [n.name for n in chains]
        except AttributeError:
            pass 
        self.assertEqual(set(chains), {"R"}, "The new graph does have the chain R.")

    def test_find_collider(self):
        graph = self._create_example_graph()
        collider = solution.find_collider(graph)
        # Ensure we allow both string and node returns
        try:
            collider = [n.name for n in collider]
        except AttributeError:
            pass 
        self.assertEqual(set(collider), {"A"}, "Incorrect collider found.")


    def test_find_immoralities(self):
        graph1 = self._create_example_graph()
        graph2 = graph1.copy()
        graph2.remove_edge("E","R")
        graph2.add_edge("R","E")
        print("Immoralities of graph1: ", solution.find_immoralities(graph1))
        print("Immoralities of graph2: ", solution.find_immoralities(graph2))
        self.assertEqual(solution.find_immoralities(graph1),solution.find_immoralities(graph2), "The graphs have the same immoralities")

        # You would need to define your own test here since the return
        # type is up to you!
        

    def test_same_skeleton(self):
        graph1 = self._create_example_graph()
        graph2 = graph1.copy()
        graph2.remove_edge("E","R")
        graph2.add_edge("R","E")
        self.assertTrue(solution.same_skeleton(graph1, graph2), "The graphs have the same skeletons")


    def test_markov_equivalent(self):
        graph1 = self._create_example_graph()
        graph2 = graph1.copy()
        graph2.remove_edge("E","R")
        graph2.add_edge("R","E")
        self.assertTrue(solution.markov_equivalent(graph1, graph2), "Graphs are ME")

    def test_get_paths(self):
        graph = self._create_example_graph()
        paths = solution.get_paths(graph, "A", "R")
        true_paths = [["A","E","R"]]
        for p in true_paths:
            self.assertIn(p, paths)

    def test_is_collider(self):
        graph = self._create_example_graph()
        path = ["B","A","E"]
        self.assertTrue(solution.is_collider(graph, "A", path), "A is a collider on this path.")

    def test_is_path_open(self):
        graph = self._create_example_graph()
        path = ["B","A","E"]
        self.assertTrue(solution.is_path_open(graph, path, ["A"]), "Path BAE is open if A is given.")

    def test_unblocked_path_exists_collider_given(self):
        graph = self._create_example_graph()
        self.assertFalse(solution.unblocked_path_exists(graph, "B", "E", []), "The only path is blocked by the collider.")
        self.assertTrue(solution.unblocked_path_exists(graph, "B", "E", ["A"]), "The evidence of the collider opens the path.")
        
    def test_check_indepedence_dsep(self):
        graph = self._create_example_graph()
        self.assertTrue(solution.check_independence(graph, ["B"], ["E"], ["R"]), "B and E are conditionally indepedent given E")
        self.assertFalse(solution.check_independence(graph, ["B"], ["E"], ["A"]), "B and E are conditionally dependent given A")

    def test_ancestral_graph(self):
        graph = self._create_lecture_graph()
        query_nodes = ["A","I","F","L"]
        ancestral_graph =solution.make_ancestral_graph(graph, query_nodes)
        self.assertFalse("G" in ancestral_graph.nodes, "G is not part of the ancestral graph")
    
    def test_moral_graph(self):
        graph = self._create_lecture_graph()

        # query_nodes = ["A","I","F","L"]
        # ancestor_graph: Graph = solution.make_ancestral_graph(graph, query_nodes)

        moral_graph = solution.make_moral_graph(graph)
        self.assertFalse(moral_graph.is_directed, "The moral graph should no longer be directed.")
        self.assertEqual(set(graph.nodes.keys()), set(moral_graph.nodes.keys()), "A moral graph should not lose any nodes")

    def test_separation(self):
        graph = self._create_lecture_graph()
        moral_graph = graph

        query_nodes = ["A","I","F","L"]
        ancestor_graph: Graph = solution.make_ancestral_graph(graph, query_nodes)
        moral_graph = solution.make_moral_graph(ancestor_graph)
        
        res = solution.separation(moral_graph, ["F", "L"])

        self.assertFalse("F" in res.nodes["H"].children, "There should no longer be an edge between F and H")
        self.assertFalse("F" in res.nodes["D"].children, "There should no longer be an edge between F and D")
        self.assertFalse("L" in res.nodes["H"].children, "There should no longer be an edge between L and H")

    def test_check_independence_general(self):
        graph = self._create_lecture_graph()
        self.assertFalse(solution.check_independence_general(graph, ["A"], ["I"], ["L","F"]), "A and I are conditionnaly dependent given L and F")
        self.assertTrue(solution.check_independence_general(graph, ["A"], ["B"], ["C"]), "A and B are conditionnaly independent given C")
        self.assertTrue(solution.check_independence_general(graph, ["A"], ["B"], ["F"]), "A and B are conditionnaly independent given F")
        self.assertTrue(solution.check_independence_general(graph, ["A"], ["E"], ["C"]), "A and E are conditionnaly independent given C")
        self.assertFalse(solution.check_independence_general(graph, ["A"], ["B"], ["M"]), "A and E are conditionnaly dependent given M")

    def _create_example_graph(self):
        dg = solution.Graph()
        dg.add_node("A")
        dg.add_node("B")
        dg.add_node("E")
        dg.add_node("R")
        dg.add_edge("B","A")
        dg.add_edge("E","A")
        dg.add_edge("E","R")
        return dg

    def _create_lecture_graph(self):
        graph = solution.Graph()

        graph.add_node("A")
        graph.add_node("B")
        graph.add_node("C")
        graph.add_node("D")
        graph.add_node("E")
        graph.add_node("F")
        graph.add_node("G")
        graph.add_node("H")
        graph.add_node("I")
        graph.add_node("L")
        graph.add_node("M")

        graph.add_edge("A", "C")
        graph.add_edge("C", "E")
        graph.add_edge("E", "G")
        graph.add_edge("E", "H")
        graph.add_edge("B", "D")
        graph.add_edge("D", "F")
        graph.add_edge("F", "H")
        graph.add_edge("F", "I")
        graph.add_edge("H", "L")
        graph.add_edge("I", "M")
        graph.add_edge("M", "H")

        return graph

if __name__ == "__main__":
    unittest.main()
        