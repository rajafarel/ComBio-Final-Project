from Bio.Phylo.TreeConstruction import DistanceTreeConstructor, DistanceMatrix

def build_tree(alignment, matrix):
    taxa = [record.id for record in alignment]
    dm = DistanceMatrix(names=taxa, matrix=matrix)
    
    constructor = DistanceTreeConstructor()
    tree = constructor.nj(dm)  
    
    return tree
