from collections import deque
from networkx.utils import generate_unique_node

def negative_edge_cycle(G, weight='weight'):
    """
    If there is a negative edge cycle anywhere in G, returns True.
    Also returns the total weight of the cycle and the nodes in the cycle.

    Parameters
    ----------
    G : NetworkX graph

    weight: string, optional (default='weight')
       Edge data key corresponding to the edge weight

    Returns
    -------
    length : numeric
        Length of a negative edge cycle if one exists, otherwise None.

    nodes: list
        Nodes in a negative edge cycle (in order) if one exists,
        otherwise None.

    negative_cycle : bool
        True if a negative edge cycle exists, otherwise False.

    Examples
    --------
    >>> import networkx as nx
    >>> import bellmanford as bf
    >>> G = nx.cycle_graph(5, create_using = nx.DiGraph())
    >>> print(bf.negative_edge_cycle(G))
    (None, [], False)
    >>> G[1][2]['weight'] = -7
    >>> print(bf.negative_edge_cycle(G))
    (-3, [4, 0, 1, 2, 3, 4], True)

    Notes
    -----
    Edge weight attributes must be numerical.
    Distances are calculated as sums of weighted edges traversed.

    This algorithm uses bellman_ford() but finds negative cycles
    on any component by first adding a new node connected to
    every node, and starting bellman_ford on that node.  It then
    removes that extra node.
    """
    newnode = generate_unique_node()
    G.add_edges_from([(newnode, n) for n in G])

    try:
        pred, dist, negative_cycle_end = bellman_ford_tree(G, newnode, weight)

        if negative_cycle_end:
            nodes = []
            negative_cycle = True
            end = negative_cycle_end
            while True:
                nodes.insert(0, end)
                if nodes.count(end) > 1:
                    end_index = nodes[1:].index(end) + 2
                    nodes = nodes[:end_index]
                    break
                end = pred[end]
            length = sum(
                G[u][v].get(weight, 1) for (u, v) in zip(nodes, nodes[1:])
            )
        else:
            nodes = None
            negative_cycle = False
            length = None

        return length, nodes, negative_cycle
    finally:
        G.remove_node(newnode)


def bellman_ford(G, source, target, weight='weight'):
    """
    Compute shortest path and shortest path lengths between a source node
    and target node in weighted graphs using the Bellman-Ford algorithm.

    Parameters
    ----------
    G : NetworkX graph

    pred: dict
        Keyed by node to predecessor in the path

    dist: dict
        Keyed by node to the distance from the source

    source: node label
        Source node

    target: node label
        Target node

    weight: string
       Edge data key corresponding to the edge weight

    Returns
    -------
    length : numeric
        Length of a negative cycle if one exists.
        Otherwise, length of a shortest path.
        Length is inf if source and target are not connected.

    nodes: list
        List of nodes in a negative edge cycle (in order) if one exists.
        Otherwise, list of nodes in a shortest path.
        List is empty if source and target are not connected.

    negative_cycle : bool
        True if a negative edge cycle exists, otherwise False.

    Examples
    --------
    >>> import networkx as nx
    >>> G = nx.path_graph(5, create_using = nx.DiGraph())
    >>> bf.bellman_ford(G, source=0, target=4)
    (3, [1, 2, 3, 4], False)
    """
    # Get shortest path tree
    pred, dist, negative_cycle_end = bellman_ford_tree(G, source, weight)

    nodes = []

    if negative_cycle_end:
        negative_cycle = True
        end = negative_cycle_end
        while True:
            nodes.insert(0, end)
            if nodes.count(end) > 1:
                end_index = nodes[1:].index(end) + 2
                nodes = nodes[:end_index]
                break
            end = pred[end]
    else:
        negative_cycle = False
        end = target
        while True:
            nodes.insert(0, end)
            # If end has no predecessor
            if pred.get(end, None) is None:
                # If end is not s, then there is no s-t path
                if end != source:
                    nodes = []
                break
            end = pred[end]

    if nodes:
        length = sum(
            G[u][v].get(weight, 1) for (u, v) in zip(nodes, nodes[1:])
        )
    else:
        length = float('inf')

    return length, nodes, negative_cycle


def bellman_ford_tree(G, source, weight='weight'):
    """
    Compute shortest path lengths and predecessors on shortest paths
    in weighted graphs using the Bellman-Ford algorithm.

    The algorithm has a running time of O(mn) where n is the number of
    nodes and m is the number of edges.  It is slower than Dijkstra but
    can handle negative edge weights.

    Parameters
    ----------
    G : NetworkX graph
       The algorithm works for all types of graphs, including directed
       graphs and multigraphs.

    source: node label
       Starting node for path

    weight: string, optional (default='weight')
       Edge data key corresponding to the edge weight

    Returns
    -------
    pred, dist : dictionaries
       Returns two dictionaries keyed by node to predecessor in the
       path and to the distance from the source respectively.
       Distance labels are invalid if a negative cycle exists.

    negative_cycle_end : node label
        Backtrack from this node using pred to find a negative cycle, if
        one exists; otherwise None.

    Examples
    --------
    >>> import networkx as nx
    >>> G = nx.path_graph(5, create_using = nx.DiGraph())
    >>> pred, dist, negative_cycle_end = bf.bellman_ford_tree(G, 0)
    >>> sorted(pred.items())
    [(0, None), (1, 0), (2, 1), (3, 2), (4, 3)]
    >>> sorted(dist.items())
    [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]

    >>> G = nx.cycle_graph(5, create_using = nx.DiGraph())
    >>> G[1][2]['weight'] = -7
    >>> bf_bellman_ford_tree(G, 0)
    ({0: 4, 1: 0, 2: 1, 3: 2, 4: 3}, {0: -12, 1: -11, 2: -15, 3: -14, 4: -13}, 0)

    Notes
    -----
    Edge weight attributes must be numerical.
    Distances are calculated as sums of weighted edges traversed.

    The dictionaries returned only have keys for nodes reachable from
    the source.

    In the case where the (di)graph is not connected, if a component
    not containing the source contains a negative cost (di)cycle, it
    will not be detected.

    """
    if source not in G:
        raise KeyError("Node %s is not found in the graph" % source)

    dist = {source: 0}
    pred = {source: None}

    return _bellman_ford_relaxation(G, pred, dist, [source], weight)


def _bellman_ford_relaxation(G, pred, dist, source, weight):
    """
    Relaxation loop for Bellman–Ford algorithm

    Parameters
    ----------
    G : NetworkX graph

    pred: dict
        Keyed by node to predecessor in the path

    dist: dict
        Keyed by node to the distance from the source

    source: list
        List of source nodes

    weight: string
       Edge data key corresponding to the edge weight

    Returns
    -------
    pred, dist : dict
        Returns two dictionaries keyed by node to predecessor in the
        path and to the distance from the source respectively.

    negative_cycle_end : node label
        Backtrack from this node using pred to find a negative cycle, if
        one exists; otherwise None.
    """
    if G.is_multigraph():
        def get_weight(edge_dict):
            return min(eattr.get(weight, 1) for eattr in edge_dict.values())
    else:
        def get_weight(edge_dict):
            return edge_dict.get(weight, 1)

    G_succ = G.succ if G.is_directed() else G.adj
    inf = float('inf')
    n = len(G)

    count = {}
    q = deque(source)
    in_q = set(source)
    while q:
        u = q.popleft()
        in_q.remove(u)

        # Skip relaxations if the predecessor of u is in the queue.
        if pred[u] not in in_q:
            dist_u = dist[u]

            for v, e in G_succ[u].items():
                dist_v = dist_u + get_weight(e)

                if dist_v < dist.get(v, inf):
                    dist[v] = dist_v
                    pred[v] = u

                    if v not in in_q:
                        q.append(v)
                        in_q.add(v)
                        count_v = count.get(v, 0) + 1

                        if count_v == n:
                            negative_cycle_end = u
                            return pred, dist, negative_cycle_end

                        count[v] = count_v

    negative_cycle_end = None
    return pred, dist, negative_cycle_end
