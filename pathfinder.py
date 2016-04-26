# -*- coding:utf-8 -*-

import sys
from itertools import ifilter

MAX = 1000
MIN = 0


class TowerException(Exception):
    pass


class TowerGraph(object):
    """根据输入文件在地图指定位置建Tower, 并判断地图是否可以走通"""

    def __init__(self, graph_file):
        self._graph_file = graph_file
        self._M = 0
        self._N = 0
        self._start = (0, 0)
        self._target = ()
        self._graph = None
        self._visited_posi = {}
        self._visit_stack = [self._start]
        self._test_position = None

    @property
    def test_position(self):
        """返回最后建塔的位置"""
        return self._test_position

    def build(self):
        """建立地图"""
        try:
            self._M, self._N = map(int, self._graph_file.readline().split())

            if self._M < MIN or self._M > MAX or self._N < MIN or self._N > MAX:
                raise TowerException("out of graph scope")

            self._graph = [[0 for _ in range(self._N)] for _ in range(self._M)]
            for x in range(self._M):
                flags = self._graph_file.readline().split()
                if len(flags) != self._N:
                    raise TowerException("wrong flag's counter")
                for y, flag in enumerate(flags):
                    if flag not in ("-", "*"):
                        raise TowerException("invalid flag")
                    if flag == "*":
                        self._graph[x][y] = 1
            self._test_position = tuple(
                                        map(int,
                                            self._graph_file.readline().split()))
            towerx, towery = self._test_position
            if towerx > self._M or towery > self._N:
                raise TowerException("out of graph scope")
            self._graph[towerx][towery] = 1
            self._target = (self._M -1, self._N -1)
        except ValueError as valuex:
            raise TowerException(valuex)

    def check_position(self, position):
        """判断坐标是否有效
            :param position: 包含坐标的tuple,例如 : ``(1, 1)``
            :returns: 如果是有效坐标,返回 ``True``,否则返回``False``
        """
        try:
            x, y = position
            return position not in self._visited_posi \
                    and (x >= 0 and x < self._M) \
                    and (y >= 0 and y < self._N) \
                    and self._graph[x][y] == 0
        except ValueError:
            raise TowerException("invalid position format")

    def find_path(self):
        """遍历地图并判断地图是否可以走通
           :returns: 如果可以走通,返回 ``True``,否则返回 ``False``
        """
        while self._visit_stack:
            position = self._visit_stack.pop()
            if position not in self._visited_posi:
                if position == self._target:
                    return True

                self._visited_posi[position] = 1
                x, y = position
                valid_positions = ifilter(self.check_position, \
                                            [(x + 1, y), (x, y + 1)])
                self._visit_stack.extend(valid_positions)
        return False


if __name__ == '__main__':
    with open(sys.argv[1]) as graph_file:
        graph = TowerGraph(graph_file)
        graph.build()
        has_path = graph.find_path()
        if has_path: 
            print("%d %d YES" % graph.test_position)
        else:
            print("%d %d NO" % graph.test_position)
