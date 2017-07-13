import csv
import os
import time

from algorithms import (
    all_pairs_bds,
    construct_bds,
    create_graph_with_backbone,
    heuristic_scbds
)
from common import (
    header_format,
    keys,
    row_format,
    sequence,
    text
)
from graph import Graph
from setting import (
    cases,
    input_folder,
    nums,
    output_folder,
    rhos,
    r_mins,
)


def simulate(G, algorithm, max_hop):

    def statistic():
        routing_lengths = []
        max_ratio = -1
        for u in G.nodes():
            for v in G.nodes():
                if u != v:
                    length = len(shortest_path_via_backbone[u][v]) - 1
                    routing_lengths.append(length)
                    ratio = length / (len(shortest_path[u][v]) - 1)
                    if ratio > max_ratio:
                        max_ratio = ratio
        average_length = sum(routing_lengths) / len(routing_lengths)
        return average_length, max_ratio

    C = construct_bds(G)
    shortest_path = G.all_pairs_shortest_path()
    S = algorithm(G, C, shortest_path,  max_hop)

    G_backbone = create_graph_with_backbone(G, S)
    assert G_backbone.nodes() == G.nodes()

    shortest_path_via_backbone = G_backbone.all_pairs_shortest_path()
    average_length, max_ratio = statistic()
    assert max_ratio <= 5
    return len(C), len(S), average_length, max_ratio


def main():

    def print_header():
        print('{:=^92}'.format(
            ' Average Data r_min = {} rho = {} over {} testcases '.format(
                r_min, rho, cases)
        ))
        print(header_format.format(
            '', 'Max Hop', 'N', '|C|', '|S|', 'ARPL', 'Max Ratio', 'Time Used'
        ))

    def print_row(c, n, avgs, start, end):
        elapsed = end - start
        print(row_format.format(
            text(c), configs[c][1], n,
            *[avgs[k] / cases for k in keys[2:]],
            int(elapsed / 60),
            elapsed % 60
        ))

    def record():
        print_header()
        for c in sequence:
            path = os.path.join(output_folder,
                                'r_min{}rho{}'.format(r_min, rho),
                                'nums{}-{}'.format(nums[0], nums[-1]))
            if not os.path.isdir(path):
                os.makedirs(path)
            with open(
                    os.path.join(path, '{}.csv'.format(text(c))),
                    'w'
            ) as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=keys)
                writer.writeheader()
                for n in nums:
                    avgs = {k: 0 for k in keys[2:]}
                    start = time.time()
                    for t in range(1, cases + 1):
                        G = Graph(n, r_min, rho, t, input_folder)
                        data = dict(zip(keys[2:], simulate(G, *configs[c])))
                        for k, v in data.items():
                            avgs[k] += v
                        data.update({'N': n, 'Case': t})
                        writer.writerow(data)
                    end = time.time()
                    print_row(c, n, avgs, start, end)

    configs = {
        '$\\alpha$-MOC-SCBDS-C-4': (all_pairs_bds, 4),
        '$\\alpha$-MOC-SCBDS-C-3': (all_pairs_bds, 3),
        'Heuristic SCBDS 4 hops': (heuristic_scbds, 4),
        'Heuristic SCBDS 3 hops': (heuristic_scbds, 3),
    }
    assert set(sequence) == set(configs.keys())
    assert all(len(v) == 2 for v in configs.values())

    for r_min in r_mins:
        for rho in rhos:
            record()


if __name__ == '__main__':
    main()
