import pandas as pd
import matplotlib.pyplot as plt
from skbio import DistanceMatrix
from skbio.stats.ordination import pcoa

# Input files
distance_matrix_path = "../data/fununifrac_data/body_sites/pairwise_bray_curtis.csv"
metadata_path = "../data/fununifrac_data/body_sites/hmgdb_selected_dataset_reduced_col_20240321_164054.csv"

# Load Bray-Curtis matrix
dist_df = pd.read_csv(distance_matrix_path, index_col=0)

# Ensure sample order is consistent
dm = DistanceMatrix(dist_df.values, ids=dist_df.index.tolist())
pcoa_results = pcoa(dm)

# Load metadata
metadata = pd.read_csv(metadata_path)

# Filter to only samples in the Bray-Curtis matrix
# Filter metadata and distance matrix to overlapping samples
common_ids = metadata['library_id'].isin(dist_df.index)
metadata = metadata[common_ids].set_index('library_id')
dist_df = dist_df.loc[metadata.index, metadata.index]

# Re-run PCoA on filtered matrix
dm = DistanceMatrix(dist_df.values, ids=dist_df.index.tolist())
pcoa_results = pcoa(dm)

# Map body site colors
color_map = {
    "gut": "blue",
    "oral": "orange",
    "skin": "green",
    "vaginal": "red"
}
colors = metadata['HMgDB_sample_site_1'].map(color_map)

# Combine for plotting
merged = pd.DataFrame({
    'PC1': pcoa_results.samples['PC1'],
    'PC2': pcoa_results.samples['PC2'],
    'BodySite': metadata['HMgDB_sample_site_1'],
    'Color': colors
}, index=metadata.index)

# Plot
plt.figure(figsize=(10, 8))
for site, group in merged.groupby('BodySite'):
    plt.scatter(group['PC1'], group['PC2'], label=site, c=group['Color'], alpha=0.7)

plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title("PCoA based on Bray-Curtis Distance")
plt.legend(title="PCoA based on Bray-Curtis Distance")
plt.grid(True)
plt.tight_layout()
plt.savefig("../data/fununifrac_data/body_sites/pcoa_bray_curtis.pdf", dpi=300)
plt.show()
