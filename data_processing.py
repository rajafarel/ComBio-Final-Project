from Bio import SeqIO

def process_sequences(file_paths):
    sequences = []
    for file_path in file_paths:
        seqs = list(SeqIO.parse(file_path, "fasta"))
        sequences.extend(seqs)
    return sequences
