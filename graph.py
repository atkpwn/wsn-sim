from math import sqrt
import networkx as nx
import os
from progress.bar import IncrementalBar as Bar
import random

from setting import (
    cases,
    input_folder,
    nums,
    rhos,
    r_mins
)


def dist(u, v):
    return sqrt(sum((x - y)**2 for x, y in zip(u, v)))


class Graph(nx.DiGraph):

    def __init__(self, n, r_min, rho, i=None, folder='input', empty=False):
        super().__init__(self)
        self.n = n
        self.r_min = r_min
        self.rho = rho
        if not empty:
            if i:
                self.read(i, folder)
            else:
                self.create_connected_digraph()

    def all_pairs_shortest_path(self):
        return nx.all_pairs_shortest_path(self)

    def create_connected_digraph(self):
        self.add_nodes_from([0, 1])
        while not nx.is_strongly_connected(self):
            self.clear()
            self.add_nodes_from(range(self.n))
            positions = self._get_random_positions()
            for i, p in enumerate(positions):
                self.node[i]['pos'] = p
                self.node[i]['r'] = random.uniform(
                    self.r_min, self.rho * self.r_min
                )
            self.create_edges()

    def draw(self, C=set(), S=set(), label=False, node_size=50):
        positions = {i: u['pos'] for i, u in self.nodes().items()}
        nx.draw_networkx_edges(self,
                               positions,
                               alpha=0.3)
        nx.draw_networkx_nodes(self,
                               positions,
                               nodelist=set(self.nodes()) - S,
                               node_size=node_size,
                               node_color='blue',
                               alpha=0.7)
        nx.draw_networkx_nodes(self,
                               positions,
                               nodelist=S - C,
                               node_size=node_size,
                               node_color='yellow',
                               alpha=0.7)
        nx.draw_networkx_nodes(self,
                               positions,
                               nodelist=C,
                               node_size=node_size,
                               node_color='red',
                               alpha=0.7)

        if label:
            nx.draw_networkx_labels(self,
                                    positions,
                                    font_size=10)

    def create_edges(self, V=None, bidirection=False):
        E = set()
        for i, u in self.nodes().items():
            for j, v in (V.items() if V else None) or self.nodes().items():
                if i == j:
                    continue
                d = dist(u['pos'], v['pos'])
                if bidirection:
                    if d <= u['r'] and d <= v['r']:
                        E.add((i, j))
                        E.add((j, i))
                else:
                    if d <= u['r']:
                        E.add((i, j))
        self.add_edges_from(E)

    def is_strongly_connected(self):
        return nx.is_strongly_connected(self)

    def nodes(self):
        return dict(super().nodes(data=True))

    def subgraph(self, V):
        G = self.__class__(self.n, self.r_min, self.rho, empty=True)
        G.add_nodes_from(V)
        for u in V:
            G.node[u] = self.node[u].copy()
        G.create_edges()
        return G

    def read(self, i, folder='input'):
        self.clear()
        path = os.path.join(folder,
                            self._get_directory(),
                            self._get_filename(i))
        with open(path, 'r') as reader:
            self.add_nodes_from(range(self.n))
            for i, line in enumerate(reader.readlines()):
                data = line.split()
                self.node[i]['pos'] = tuple(map(float, data[:2]))
                self.node[i]['r'] = float(data[2])
        self.create_edges()

    def write(self, folder='input'):
        def get_filenumber():
            i = 1
            while os.path.exists(
                    os.path.join(path, self._get_filename(i))
            ):
                i += 1
            return i
        path = os.path.join(folder,
                            self._get_directory())
        if not os.path.isdir(path):
            os.makedirs(path)
        filename = self._get_filename(get_filenumber())
        with open(os.path.join(path, filename), 'w') as writer:
            writer.write('\n'.join('{} {} {}'.format(u['pos'][0],
                                                     u['pos'][1],
                                                     u['r'])
                                   for u in self.nodes().values()))

    def _get_directory(self):
        return 'r_min{}rho{:.2f}'.format(self.r_min, self.rho)

    def _get_filename(self, i):
        return '{}-{:03d}.in'.format(self.n, i)

    def _get_random_positions(self, width=100, height=100):
        positions = []
        for i in range(self.n):
            positions.append(
                (random.uniform(0, width), random.uniform(0, height))
            )
        return positions


def main():
    print('Generating graph')
    for r_min in r_mins:
        for rho in rhos:
            print('r_min = {:.2f}, rho = {:.2f}'.format(r_min, rho))
            for n in nums:
                bar = Bar('  n = {}'.format(n), max=cases)
                for t in range(cases):
                    G = Graph(n, r_min, rho)
                    G.write(input_folder)
                    bar.next()
                bar.finish()


if __name__ == '__main__':
    main()
