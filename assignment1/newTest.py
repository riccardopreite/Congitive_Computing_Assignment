"""
Some test cases in a similar way to the ones used for grading your submissions.
Feel free to add more complex test cases here.
More information about the used testing framework can be found in the LernraumPlus as
well as the tutorial sessions.
This makes use of the unittest framework

author: Jan Pöppel
last modified. 11.10.2021
"""

import unittest
import numpy as np
import assignment1 as solution

class TestAssignment1(unittest.TestCase):

    def test_fibonacci(self):
        # EX 1.1 
        self.assertEqual(solution.fibonacci(1), 1)
        self.assertEqual(solution.fibonacci(5), 5)
        self.assertEqual(solution.fibonacci(6), 8)

    def test_random_array(self):
        # Ex 1.2
        size = 100
        res = solution.random_array(size)
        self.assertEqual(len(res), size)
        self.assertGreaterEqual(min(res), 0)
        self.assertLess(max(res), 1)
                
        size = 230
        res = solution.random_array(size, min_val=-23, max_val=100)
        self.assertEqual(len(res), size)
        self.assertGreaterEqual(min(res), -23)
        self.assertLess(max(res), 100)
        
    def test_analyze_return(self):
        # Ex 1.3
        array= [-5,-4,-3,-2,-1,0,1,2,4,5]
        res = solution.analyze(array)
        self.assertIsInstance(res, dict)
        self.assertEqual(res["minimum"], -5)
        self.assertEqual(res["maximum"], 5)
        self.assertEqual(res["median"], -0.5)
        self.assertEqual(res["mean"], -3/10)

    def test_list_ends(self):
        # Ex 1.5
        array = [1,2,3,4,5]
        self.assertEqual(solution.list_ends(array), [array[0], array[-1]])
        array = [1]
        self.assertEqual(solution.list_ends(array), [1,1])

        
    def test_matix_mul(self):
        # Ex 1.6
        a = np.array([[1,2],[3,4]])
        b = np.array([[1,0],[0,1]])
        true_res = np.array([[1,2],[3,4]])
        
        np.testing.assert_array_equal(solution.matrix_mul(a,b), true_res)


    # graph = DGraph()
    # assert graph.get_number_of_nodes() == 0, "A new graph should not have any nodes."
    # graph.add_node("A")
    # assert graph.num_nodes == 1, "The graph should now have one node"
    # graph.add_node("B")
    # graph.add_edge("A", "B")
    # assert graph.get_parents("B") == ["A"], "Node B should have node A has a parent"
    # assert graph.get_children("A") == ["B"], "Node A should have node B as a child"
    # assert graph.is_ancestor("A", "B") == True, "A parent is also an ancestor"
    # assert graph.is_descendant("B", "A") == True, "A child is also a descendant"
    # assert graph.is_acyclic() == True, "A graph with only 1 edge cannot be cyclic"
    # graph.remove_edge("A","B")
    # assert graph.is_ancestor("A","B") == False, "Removing the edge deletes any ancestry"

    def test_create_graph(self):
        g = solution.DGraph()
        self.assertEqual(g.get_number_of_nodes(), 0)

    def test_add_node(self):
        g = solution.DGraph()
        g.add_node("A")
        self.assertEqual(g.get_number_of_nodes(),1)

 
    def test_add_edge(self):
        g = solution.DGraph()
        g.add_node("A")
        g.add_node("B")
        g.add_edge("A","B")
        self.assertTrue("B" in g.get_children("A"))
        self.assertTrue("A" in g.get_parents("B"))
        
    def test_is_ancestor(self):
        g = solution.DGraph()
        g.add_node("A")
        g.add_node("B")
        g.add_node("C")
        g.add_edge("A","B")
        g.add_edge("B","C")
        self.assertTrue(g.is_ancestor("A", "C"))
        g.remove_edge("A","B")
        self.assertFalse(g.is_ancestor("A", "C"))

    def test_is_descendant(self):
        g = solution.DGraph()
        g.add_node("A")
        g.add_node("B")
        g.add_node("C")
        g.add_edge("A","B")
        g.add_edge("B","C")
        self.assertTrue(g.is_descendant("B", "A"))
        g.remove_edge("A","B")
        self.assertFalse(g.is_descendant("B", "A"))

    def test_get_number_of_nodes(self):
        g = solution.DGraph()
        g.add_node("A")
        g.add_node("B")
        self.assertEqual(g.get_number_of_nodes(), 2)

    def test_is_acyclic(self):
        g = solution.DGraph()
        g.add_node("2")
        g.add_node("3")
        g.add_node("5")
        g.add_node("7")
        g.add_node("8")
        g.add_node("9")
        g.add_node("10")
        g.add_node("11")

        g.add_edge("3","8")
        g.add_edge("3","10")

        g.add_edge("5","11")

        g.add_edge("7","8")
        g.add_edge("7","11")

        g.add_edge("8","9")

    
        g.add_edge("11","2")
        g.add_edge("11","7")
        g.add_edge("11","10")
        g.add_edge("11","9")

        self.assertFalse(g.is_acyclic())
        g.add_edge("9","7")
        self.assertFalse(g.is_acyclic())

        self.assertTrue(g.is_ancestor("7", "7"))
        self.assertTrue(g.is_ancestor("11", "7"))
        g.remove_edge("9","7")
        g.remove_edge("11","7")

        self.assertTrue(g.is_acyclic())

        self.assertFalse(g.is_ancestor("7", "7"))
        self.assertFalse(g.is_ancestor("9", "7"))



if __name__ == "__main__":
    unittest.main()
        