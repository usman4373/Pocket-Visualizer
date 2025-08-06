import os
import csv

def write_interacting_residues_csv(csv_path, complex_name, residues):
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    
    with open(csv_path, "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header only if file is empty
        if csvfile.tell() == 0:
            writer.writerow(["Complex", "Interacting Residues"])
        if residues:
            writer.writerow([complex_name, ", ".join(residues)])
