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
        # self.assertEqual(solution.fibonacci(10000), 33644764876431783266621612005107543310302148460680063906564769974680081442166662368155595513633734025582065332680836159373734790483865268263040892463056431887354544369559827491606602099884183933864652731300088830269235673613135117579297437854413752130520504347701602264758318906527890855154366159582987279682987510631200575428783453215515103870818298969791613127856265033195487140214287532698187962046936097879900350962302291026368131493195275630227837628441540360584402572114334961180023091208287046088923962328835461505776583271252546093591128203925285393434620904245248929403901706233888991085841065183173360437470737908552631764325733993712871937587746897479926305837065742830161637408969178426378624212835258112820516370298089332099905707920064367426202389783111470054074998459250360633560933883831923386783056136435351892133279732908133732642652633989763922723407882928177953580570993691049175470808931841056146322338217465637321248226383092103297701648054726243842374862411453093812206564914032751086643394517512161526545361333111314042436854805106765843493523836959653428071768775328348234345557366719731392746273629108210679280784718035329131176778924659089938635459327894523777674406192240337638674004021330343297496902028328145933418826817683893072003634795623117103101291953169794607632737589253530772552375943788434504067715555779056450443016640119462580972216729758615026968443146952034614932291105970676243268515992834709891284706740862008587135016260312071903172086094081298321581077282076353186624611278245537208532365305775956430072517744315051539600905168603220349163222640885248852433158051534849622434848299380905070483482449327453732624567755879089187190803662058009594743150052402532709746995318770724376825907419939632265984147498193609285223945039707165443156421328157688908058783183404917434556270520223564846495196112460268313970975069382648706613264507665074611512677522748621598642530711298441182622661057163515069260029861704945425047491378115154139941550671256271197133252763631939606902895650288268608362241082050562430701794976171121233066073310059947366875 )

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
        g.add_node("A")
        g.add_node("B")
        g.add_edge("A","B")
        self.assertTrue(g.is_acyclic()) # A graph with only 1 (directed) edge cannot be cyclic

if __name__ == "__main__":
    unittest.main()
        