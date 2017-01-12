# bellmanford

This package provides a few small extensions of the Bellman-Ford routines in [NetworkX](https://networkx.github.io), primarily for convenience.

## Installation

`bellmanford` is available on PyPI:

```bash
pip install bellmanford
```

## Usage

### bellman_ford

```python
length, nodes, negative_cycle = bellman_ford(G, source, target, weight='weight')
```

Compute shortest path and shortest path lengths between a source node and target node in weighted graphs using the Bellman-Ford algorithm.

#### Parameters
* `G` : NetworkX graph
* `pred` : dict - Keyed by node to predecessor in the path
* `dist` : dict - Keyed by node to the distance from the source
* `source`: node label - Source node
* `target`: node label - Target node
* `weight` : string - Edge data key corresponding to the edge weight

#### Returns
* `length` : numeric - Length of a negative cycle if one exists; otherwise length of a shortest path.
* `nodes` : list - Nodes in a negative edge cycle (in order) if one exists; otherwise nodes in a shortest path.
* `negative_cycle` : bool - `True` if a negative edge cycle exists, otherwise `False`.

#### Examples
```python
>>> import networkx as nx
>>> G = nx.path_graph(5, create_using = nx.DiGraph())
>>> bf.bellman_ford(G, source=0, target=4)
(3, [1, 2, 3, 4], False)
```

### negative_edge_cycle

```python
length, nodes, negative_cycle = negative_edge_cycle(G, weight='weight')
```

If there is a negative edge cycle anywhere in `G`, returns `True`. Also returns the total weight of the cycle and the nodes in the cycle.

#### Parameters
* `G` : NetworkX graph
* `weight` : string, optional (default = `'weight'`) - Edge data key corresponding to the edge weight

#### Returns
* `length` : numeric - Length of a negative edge cycle if one exists, otherwise `None`.
* `nodes` : list - Nodes in a negative edge cycle (in order) if one exists, otherwise `None`.
* `negative_cycle` : bool - `True` if a negative edge cycle exists, otherwise `False`.

#### Examples

```python
>>> import networkx as nx
>>> import bellmanford as bf
>>> G = nx.cycle_graph(5, create_using = nx.DiGraph())
>>> print(bf.negative_edge_cycle(G))
(None, [], False)
>>> G[1][2]['weight'] = -7
>>> print(bf.negative_edge_cycle(G))
(-3, [4, 0, 1, 2, 3, 4], True)
```
