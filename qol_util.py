import numpy as np

def label_from_vector(v: np.ndarray):
    for i in range(len(v)):
        if v[i] != 0:
            return f"e_{int(i * v[i])}"
    
