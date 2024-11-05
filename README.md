## Setup
```bash
git clone https://github.com/KoslickiLab/branch-lengths-assignment.git
cd branch-lengths-assignment
pip install -r requirements.txt
```

## Experiment 1: recovering branch lengths using compatible distance matrices
The tests in this part correspond to section III.B of the manuscript. There are two tests in this section. The first evaluates the performance of bottom-up, naive NNLS and regularized NNLS methods in restoring branch lengths in the event when the distance matrix is completely compatible with the tree. 
```bash
mkdir -p data/test_data/test1
cd test_scripts
bash test1_perfect_scenario_method_performance.sh
bash test1_selection_factor_effect.sh
cd ..
```

## Experiment 2: recovering branch lengths using pairwise distances with errors
The test in this part corresponds to section III.C of the manuscript. 
```bash
mkdir -p data/test_data/test2
cd test_scripts
bash test2_distance_matrix_with_errors.sh
cd ..
```

## Experiment 3: comparing efficiency between NNLS and bottom-up methods
The test in this part corresponds to section III.D of the manuscript. 
```bash
mkdir -p data/test_data/test3
cd test_scripts
bash test2_efficiency.sh
cd ..
```

## Application: FunUniFrac
### Obtaining the KEGG data
The details for KEGG data extraction can be found in the [extraction repo](https://github.com/KoslickiLab/KEGG_data_extraction).
A cleaned version of KEGG tree rooted at `ko00001` can be found in `data/fununifrac_data/kegg_trees/kegg_ko00001_no_edge_lengths.txt`. 

### Obtaining pairwise distance matrix
To download a pre-built version of the pairwise distance matrix, do the following:
```bash
cd data/fununifrac_data/pw_distance_files
wget https://zenodo.org/records/13129003/files/KOs_sketched_scaled_10_k_5
```
