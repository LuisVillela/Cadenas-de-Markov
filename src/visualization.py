#src/visualization.py
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plot_transition_matrix(matrix):
    states = list(matrix.keys())
    state_indices = {state: i for i, state in enumerate(states)}
    size = len(states)

    # Crear matriz para visualización
    transition_array = np.zeros((size, size))
    for state, transitions in matrix.items():
        for move, prob in transitions.items():
            next_state = state_indices.get(move, None)
            if next_state is not None:
                transition_array[state_indices[state], next_state] = prob

    # Crear heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(transition_array, xticklabels=states, yticklabels=states, cmap='coolwarm')
    plt.title("Matriz de Transición")
    plt.xlabel("Siguiente Estado")
    plt.ylabel("Estado Actual")
    plt.show()
