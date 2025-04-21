import numpy as np
import pandas as pd
from skbio import DistanceMatrix
from skbio.stats.distance import permanova

# === File paths ===
bray_path = "../data/fununifrac_data/body_sites/pairwise_bray_curtis.csv"
fununifrac_path = "../data/fununifrac_data/body_sites/fununifrac_out_pw_distance_nnls.main.npy"
fununifrac_labels_path = "../data/fununifrac_data/body_sites/fununifrac_out_pw_distance_nnls_labels.txt"
metadata_path = "../data/fununifrac_data/body_sites/hmgdb_selected_dataset_reduced_col_20240321_164054.csv"

# === Load metadata ===
metadata = pd.read_csv(metadata_path, low_memory=False)
metadata = metadata.set_index("library_id")

# === Bray-Curtis PERMANOVA ===
bray_df = pd.read_csv(bray_path, index_col=0)
bray_ids = [idx for idx in bray_df.index if idx in metadata.index]
bray_df = bray_df.loc[bray_ids, bray_ids]
bray_meta = metadata.loc[bray_ids]
bray_dm = DistanceMatrix(np.ascontiguousarray(bray_df.values), ids=bray_df.index)

bray_permanova = permanova(distance_matrix=bray_dm, grouping=bray_meta["HMgDB_sample_site_1"])
print("\n=== PERMANOVA (Bray-Curtis) ===")
print(bray_permanova)

# === FunUniFrac PERMANOVA ===
fununi_matrix = np.load(fununifrac_path)
with open(fununifrac_labels_path, "r") as f:
    fununi_labels = [line.strip() for line in f.readlines()]

valid_labels = [lbl for lbl in fununi_labels if lbl in metadata.index]
indices = [i for i, lbl in enumerate(fununi_labels) if lbl in valid_labels]
filtered_matrix = np.ascontiguousarray(fununi_matrix[np.ix_(indices, indices)])
fununi_meta = metadata.loc[valid_labels]

fununi_dm = DistanceMatrix(filtered_matrix, ids=valid_labels)
fununi_permanova = permanova(distance_matrix=fununi_dm, grouping=fununi_meta["HMgDB_sample_site_1"])
print("\n=== PERMANOVA (FunUniFrac) ===")
print(fununi_permanova)
