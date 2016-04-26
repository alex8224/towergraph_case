# -*- coding:utf-8 -*-
import unittest
from pathfinder import TowerGraph, TowerException
from StringIO import StringIO

def build_graph_file(m, n, test_posi):
    flags = [["-" for _ in range(n)] for _ in range(m)]
    iofile = StringIO()
    iofile.write("%d %d" % (m, n) + "\n")
    for flag in flags:
        iofile.write(" ".join(flag) + "\n")
    iofile.write("%d %d" % test_posi)
    iofile.seek(0)
    return iofile


class PathfinderTestCase(unittest.TestCase):

    def test_graph_build(self):
        M, N = 3, 4
        graph_file = build_graph_file(M, N, (1, 1))
        towergraph = TowerGraph(graph_file)
        self.assertIsNone(towergraph.build())

    def test_graph_build_outofscope_M(self):
        M, N = 1001, 4
        graph_file = build_graph_file(M, N, (1, 1))
        towergraph = TowerGraph(graph_file)
        self.assertRaises(TowerException, towergraph.build)

    def test_graph_build_outofscope_N(self):
        M, N = 3, 1001
        graph_file = build_graph_file(M, N, (1, 1))
        towergraph = TowerGraph(graph_file)
        self.assertRaises(TowerException, towergraph.build)

    def test_graph_build_boundary_M(self):
        M, N = 1000, 10
        graph_file = build_graph_file(M, N, (1, 1))
        towergraph = TowerGraph(graph_file)
        self.assertIsNone(towergraph.build())

    def test_graph_build_boundary_N(self):
        M, N = 10, 1000
        graph_file = build_graph_file(M, N, (1, 1))
        towergraph = TowerGraph(graph_file)
        self.assertIsNone(towergraph.build())

    def test_graph_build_wrong_flag(self):
        graph_file = StringIO("""3 4\n- + - -\n- - - -\n- - - -\n1 1""")
        towergraph = TowerGraph(graph_file)
        self.assertRaises(TowerException, towergraph.build)

    def test_graph_build_wrong_num_flags(self):
        graph_file = StringIO("""3 4\n- - - -\n- - - - -\n- - - -\n1 1""")
        towergraph = TowerGraph(graph_file)
        self.assertRaises(TowerException, towergraph.build)


    def test_graph_connected(self):
        graph_data = """3 4
        - - - -
        - * - -
        - * - -
        0 1"""
        graph_file = StringIO(graph_data)
        towergraph = TowerGraph(graph_file)
        towergraph.build()
        self.assertFalse(towergraph.find_path())

    def test_graph_not_connected(self):
        graph_data = """3 4
        - - - -
        - * - -
        - * - -
        1 1"""
        graph_file = StringIO(graph_data)
        towergraph = TowerGraph(graph_file)
        towergraph.build()
        self.assertTrue(towergraph.find_path())

    def test_valid_position_ok(self):
        graph_data = """3 4
        - - - -
        - * - -
        - * - -
        1 1"""
        graph_file = StringIO(graph_data)
        towergraph = TowerGraph(graph_file)
        towergraph.build()
        test_posi = (0, 1)
        self.assertTrue(towergraph.check_position(test_posi))

    def test_valid_position_outofscope_M(self):
        graph_data = """3 4
        - - - -
        - * - -
        - * - -
        1 1"""
        graph_file = StringIO(graph_data)
        towergraph = TowerGraph(graph_file)
        towergraph.build()
        test_posi = (4, 4)
        self.assertFalse(towergraph.check_position(test_posi))

    def test_valid_position_outofscope_N(self):
        graph_data = """3 4
        - - - -
        - * - -
        - * - -
        1 1"""
        graph_file = StringIO(graph_data)
        towergraph = TowerGraph(graph_file)
        towergraph.build()
        test_posi = (3, 5)
        self.assertFalse(towergraph.check_position(test_posi))

    def test_valid_position_towered(self):
        graph_data = """3 4
        - - - -
        - * - -
        - * - -
        1 1"""
        graph_file = StringIO(graph_data)
        towergraph = TowerGraph(graph_file)
        towergraph.build()
        test_posi = (2, 1)
        self.assertFalse(towergraph.check_position(test_posi))


if __name__ == '__main__':
    unittest.main()


