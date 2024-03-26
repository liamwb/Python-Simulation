import networkx as nx
from math import exp
import numpy as np


def get_e_k(k: int, d: int):
    """
    returns the basis vector e_k under the convention e_k = e_{-k}. Follows the mathematical convention of indexing from 1.

    Args:
        k (int): which basis vector you want, under the convention e_k = e_{-k}
        d (int): dimension

    Returns:
        the desired vector : ndarray
    """
    e_k = np.zeros(d)
    e_k[abs(k)-1] = 1.0 * np.sign(k) # type: ignore
    return e_k

def neighbouring_spins_S(k: int, sigma: nx.Graph, w: int):
    nbhrs = sigma.adj[w]

    return sum([sigma.nodes[nbhr]["spin"] for nbhr in sigma.neighbors(k)])

def transition_probability_p_k(k: int, sigma: nx.Graph, w: int, d: int, beta: float):
    """returns the probability that the vertex w has its spin updated to e_k.

    Args:
        k (int): update hypothesis
        sigma (nx.Graph): prior configuration
        w (int): vertex being updated
        d (int): face-cubic dimension
        beta (float): inverse temperature

    Returns:
        probability: float
    """
    return # exp() / exp()

def simulate_one_step(graph: nx.Graph):
    pass