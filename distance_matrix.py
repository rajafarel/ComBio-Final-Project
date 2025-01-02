import math
import numpy as np
from Bio import AlignIO

def calculate_transversion_transition(seq1, seq2):
    transitions = 0
    transversions = 0
    total_sites = 0

    pairs_of_transitions = {("A", "G"), ("G", "A"), ("C", "T"), ("T", "C")}

    for a, b in zip(seq1, seq2):
        if a == "-" or b == "-":
            continue
        total_sites += 1
        if a != b:
            if (a, b) in pairs_of_transitions:
                transitions += 1
            else:
                transversions += 1

    return transitions, transversions, total_sites


def k2p_distance(seq1, seq2):
    ts, tv, total_sites = calculate_transversion_transition(seq1, seq2)
    if total_sites == 0:
        return float("inf")  

    p = ts / total_sites  
    q = tv / total_sites  

    try:
        return -0.5 * math.log(1 - 2 * p - q)
    except ValueError:
        return float("inf")  


def compute_distance_matrix(alignment):
    num_of_sequences = len(alignment)
    distance_matrix = np.zeros((num_of_sequences, num_of_sequences))

    for i in range(num_of_sequences):
        for j in range(i + 1, num_of_sequences):
            seq1 = str(alignment[i].seq)
            seq2 = str(alignment[j].seq)
            distance_matrix[i][j] = k2p_distance(seq1, seq2)
            distance_matrix[j][i] = distance_matrix[i][j]  

    np.fill_diagonal(distance_matrix, 0.0)

    lower_triangle = []
    for i in range(num_of_sequences):
        row = []
        for j in range(i + 1):
            row.append(distance_matrix[i][j])
        lower_triangle.append(row)

    return lower_triangle
