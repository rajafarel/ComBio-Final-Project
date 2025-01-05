from Bio.Phylo.TreeConstruction import DistanceTreeConstructor, DistanceMatrix

def build_tree(alignment, matrix, method="nj"):
    taxa = [record.id for record in alignment]
    dm = DistanceMatrix(names=taxa, matrix=matrix)
    constructor = DistanceTreeConstructor()

    if method == "nj":
        tree = constructor.nj(dm)
    elif method == "upgma":
        tree = constructor.upgma(dm)
    else:
        raise ValueError(f"Unknown method '{method}'. Supported methods: 'nj', 'upgma'.")

    return tree
