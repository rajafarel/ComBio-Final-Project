import tkinter as tk
from tkinter import filedialog, messagebox
from data_processing import process_sequences
from alignment import align_sequences
from distance_matrix import compute_distance_matrix
from tree_construction import build_tree
from visualization import visualize_tree
from Bio import AlignIO


class PhyloApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Phylogenetic Tree Builder")
        self.root.geometry("600x600")
        
        # Title Label
        self.label_title = tk.Label(root, text="Phylogenetic Tree Builder", font=("Arial", 16))
        self.label_title.pack(pady=10)
        
        # Upload Button
        self.btn_upload = tk.Button(root, text="Upload Sequence Files", command=self.upload_files)
        self.btn_upload.pack(pady=5)
        
        # Uploaded Files Listbox
        self.file_listbox_label = tk.Label(root, text="Uploaded Files:")
        self.file_listbox_label.pack(pady=5)
        
        self.file_listbox = tk.Listbox(root, width=70, height=8)
        self.file_listbox.pack(pady=5)
        
        # Algorithm Selection
        self.algorithm_label = tk.Label(root, text="Select Tree Construction Algorithm:")
        self.algorithm_label.pack(pady=5)
        
        self.algorithm_var = tk.StringVar(value="nj")
        self.radio_nj = tk.Radiobutton(root, text="Neighbor Joining (NJ)", variable=self.algorithm_var, value="nj")
        self.radio_upgma = tk.Radiobutton(root, text="UPGMA", variable=self.algorithm_var, value="upgma")
        self.radio_nj.pack()
        self.radio_upgma.pack()
        
        # Buttons
        self.btn_process = tk.Button(root, text="Build Tree", command=self.build_tree)
        self.btn_process.pack(pady=5)
        
        self.btn_view = tk.Button(root, text="View Tree", command=self.view_tree)
        self.btn_view.pack(pady=5)
        
        self.btn_save = tk.Button(root, text="Save Tree", command=self.save_tree)
        self.btn_save.pack(pady=5)
        
        # Status Label
        self.label_status = tk.Label(root, text="Status: Waiting for user input", fg="blue")
        self.label_status.pack(pady=10)
        
        # File Paths
        self.uploaded_files = []
        self.tree = None
    
    def upload_files(self):
        files = filedialog.askopenfilenames(filetypes=[("FASTA files", "*.fasta")])
        if files:
            self.uploaded_files = files
            self.file_listbox.delete(0, tk.END)
            
            for file in files:
                self.file_listbox.insert(tk.END, file)
            
            self.label_status.config(text=f"{len(files)} files uploaded successfully.")
        else:
            self.label_status.config(text="No files selected.")
    
    def build_tree(self):
        if not self.uploaded_files:
            messagebox.showerror("Error", "Please upload sequence files first!")
            return
        
        try:
            self.label_status.config(text="Processing sequences...")
            sequences = process_sequences(self.uploaded_files)

            self.label_status.config(text="Aligning sequences...")
            alignment = align_sequences(sequences)

            self.label_status.config(text="Computing distance matrix...")
            matrix = compute_distance_matrix(alignment)

            self.label_status.config(text="Constructing phylogenetic tree...")
            method = self.algorithm_var.get()
            self.tree = build_tree(alignment, matrix, method=method)

            self.label_status.config(text=f"Phylogenetic tree built using {method.upper()}!")
            messagebox.showinfo("Success", f"Tree construction with {method.upper()} completed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to build tree: {e}")
    
    def view_tree(self):
        if self.tree:
            visualize_tree(self.tree)
        else:
            messagebox.showerror("Error", "No tree available to view. Please build a tree first!")
    
    def save_tree(self):
        if self.tree:
            file_path = filedialog.asksaveasfilename(defaultextension=".nwk", filetypes=[("Newick Files", "*.nwk")])
            if file_path:
                from Bio import Phylo
                Phylo.write(self.tree, file_path, "newick")
                messagebox.showinfo("Success", f"Tree saved as {file_path}")
        else:
            messagebox.showerror("Error", "No tree available to save.")


# Main App Runner
if __name__ == "__main__":
    root = tk.Tk()
    app = PhyloApp(root)
    root.mainloop()
