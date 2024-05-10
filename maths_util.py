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

def neighbouring_spins_S(sigma: nx.Graph, w: int):
    return sum([sigma.nodes[nbhr]["spin"] for nbhr in sigma.neighbors(w)])

def choose_vertex(sigma: nx.Graph):
    return np.random.choice(list(sigma.nodes))

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

    numerator = exp(beta * np.dot(get_e_k(k, d), neighbouring_spins_S(sigma, w))  )
    denominator = sum([ exp(beta * np.dot(get_e_k(k, d), neighbouring_spins_S(sigma, w))) for k in range(-d, d+1)])

    return  numerator/denominator 


def compute_transition_probabilities(sigma: nx.Graph, w: int, d: int, beta: float) -> dict:
    result = dict()
    for k in range(-d, d+1):
        p_k = transition_probability_p_k(k, sigma, w, d, beta)
        result[k] = p_k
    
    return result