def create_graph_with_backbone(G, backbone):
    V = G.nodes()
    G_backbone = G.subgraph(backbone)
    assert G_backbone.is_strongly_connected()
    others = set(V) - backbone
    for u in others:
        G_backbone.add_node(u)
        G_backbone.node[u] = G.node[u].copy()
    G_backbone.create_edges({u: V[u] for u in others},
                            bidirection=True)
    return G_backbone


def construct_bds(G):

    def select_node(q):
        while q[-1][1] not in V:
            q.pop()
        return q[-1][1]

    C = set()  # set of bidirectional dominating set
    q = sorted([(u['r'], i) for i, u in G.nodes().items()])
    V = set(G.nodes())
    while len(V) > 0:
        v = select_node(q)
        C = C | {v}
        neighbor_v = {w for w in G[v] if v in G[w]}
        V = V - neighbor_v - {v}
    return C


def all_pairs_bds(G, C, shortest_path, max_hop=3):
    S = C.copy()  # set of strongly connected bidirectional dominating set
    for i in C:
        for j in C:
            if i != j and len(shortest_path[i][j]) <= max_hop + 1:
                S = S.union(shortest_path[i][j])
    return S


def heuristic_scbds(G, C, shortest_path, max_hop=3):

    INF = 999999999999999

    def retrieve_path(u, v, parent, min_cost):
        h_min = INF
        for h in range(max_hop + 1):
            if min_cost[v].get(h, INF) < min_cost[v].get(h_min, INF) and \
               (h <= 3 or h == min(min_cost[v])):
                h_min = h
        w = parent[v][h_min]
        path = []
        while w != u:
            path.append(w)
            h_min -= 1
            w = parent[w][h_min]
        path.append(u)
        path.reverse()
        assert len(path) - 1 <= max_hop
        return path

    def heuristic_path(u, cost):
        min_cost = {u: {0: 0}}
        parent = {u: {0: u}}
        frontier = {u}
        for h in range(max_hop):
            next_frontier = set()
            for v in frontier:
                for w in G[v]:
                    if min_cost[v][h] + cost[w] < \
                       min_cost.get(w, {}).get(h + 1, INF):
                        if w not in min_cost:
                            min_cost[w] = {}
                            parent[w] = {}

                        min_cost[w][h + 1] = min_cost[v][h] + cost[w]
                        parent[w][h + 1] = v
                        next_frontier.add(w)
                assert max(
                    {h for u in parent for h in parent[u]}) < max_hop + 1

            frontier = next_frontier

        D = {v for v in parent if min(parent[v]) <= max_hop and v in C}
        assert D == {v for v in C if len(shortest_path[u][v]) - 1 <= max_hop}
        M = set()
        for v in D:
            M.update(retrieve_path(u, v, parent, min_cost))
        return M

    def construct_scbds():
        S = C.copy()  # set of strongly connected bidirectional dominating set
        cost = {u: 0 if u in C else 1 for u in G.nodes()}
        for u in C:
            M = heuristic_path(u, cost)
            S.update(M)
            cost.update({u: 0 for u in M})
        return S

    return construct_scbds()
