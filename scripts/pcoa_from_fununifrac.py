import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skbio import DistanceMatrix
from skbio.stats.ordination import pcoa

# === File paths ===
distance_file = '../data/fununifrac_data/body_sites/fununifrac_out_pw_distance_nnls.main.npy'
label_file = '../data/fununifrac_data/body_sites/fununifrac_out_pw_distance_nnls_labels.txt'
metadata_file = '../data/fununifrac_data/body_sites/hmgdb_selected_dataset_reduced_col_20240321_164054.csv'

# === Load distance matrix ===
distance_matrix = np.load(distance_file)

# === Load labels ===
with open(label_file, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

# === Load and filter metadata ===
metadata = pd.read_csv(metadata_file)
metadata = metadata.set_index('library_id')

# Keep only samples present in metadata
valid_labels = [label for label in labels if label in metadata.index]
indices = [i for i, label in enumerate(labels) if label in valid_labels]

# Subset matrix and metadata
filtered_distance_matrix = distance_matrix[np.ix_(indices, indices)]
metadata = metadata.loc[valid_labels]

# === Create DistanceMatrix and run PCoA ===
dm = DistanceMatrix(filtered_distance_matrix, ids=valid_labels)
pcoa_results = pcoa(dm)

# === Color map ===
color_map = {
    "gut": "blue",
    "oral": "orange",
    "skin": "green",
    "vaginal": "red"
}
colors = metadata['HMgDB_sample_site_1'].map(color_map)

# === Combine PCoA with metadata ===
merged = pd.DataFrame({
    'PC1': pcoa_results.samples['PC1'],
    'PC2': pcoa_results.samples['PC2'],
    'BodySite': metadata['HMgDB_sample_site_1'],
    'Color': colors
}, index=metadata.index)

# === Plot ===
plt.figure(figsize=(10, 8))
for site, group in merged.groupby('BodySite'):
    plt.scatter(group['PC1'], group['PC2'], label=site, c=group['Color'], alpha=0.7)

plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title("PCoA based on FunUniFrac Distance")
plt.legend(title="PCoA based on FunUniFrac Distance")
plt.grid(True)
plt.tight_layout()
plt.savefig("../data/fununifrac_data/body_sites/pcoa_fununifrac.png", dpi=300)
plt.show()
