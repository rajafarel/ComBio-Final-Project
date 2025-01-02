from Bio import Phylo
import matplotlib.pyplot as plt

def visualize_tree(tree):
    plt.figure(figsize=(10, 8))
    Phylo.draw(tree)
    plt.show()
