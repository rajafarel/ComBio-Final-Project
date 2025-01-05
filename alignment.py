import os
from Bio import AlignIO
from Bio import SeqIO
import subprocess

def align_sequences(sequences):
    input_dir = "data"
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)

    input_file = os.path.join(input_dir, "combined_sequences.fasta")
    output_file = os.path.join(input_dir, "aligned_sequences.fasta")

    muscle_executable = r"C:\Users\Raja\Desktop\Semester 5\Computational Biology\Final Project\muscle-win64.v5.3.exe"

    try:
        SeqIO.write(sequences, input_file, "fasta")

        subprocess.run(
            [
                muscle_executable,
                "-align", input_file,
                "-output", output_file,
                "-threads", "4"
            ],
            check=True,
            capture_output=True,
            text=True
        )

        alignment = AlignIO.read(output_file, "fasta")
        seq_lengths = {len(record.seq) for record in alignment}

        if len(seq_lengths) != 1:
            raise ValueError(
                f"Aligned sequences have inconsistent lengths: {seq_lengths}"
            )

        return alignment

    except subprocess.CalledProcessError as e:
        print("MUSCLE Error Output:", e.stderr)
        raise RuntimeError(f"MUSCLE alignment failed: {e}")
    except ValueError as ve:
        print(f"Alignment error: {ve}")
        raise RuntimeError(f"Inconsistent sequence lengths detected: {ve}")
    except FileNotFoundError:
        raise RuntimeError("MUSCLE executable not found. Ensure it is installed and in the system PATH.")
