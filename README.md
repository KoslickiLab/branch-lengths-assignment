## Setup
```bash
git clone https://github.com/KoslickiLab/branch-lengths-assignment.git
cd branch-lengths-assignment
pip install -r requirements.txt
```

## Experiment 1: recovering branch lengths using compatible distance matrices
The tests in this part corresponds to section III.B of the manuscript. There are two tests in this section. The first evaluates the performance of bottom-up, naive NNLS and regularized NNLS methods in restoring branch lengths in the event when the distance matrix is completely compatible with the tree. 
```bash
mkdir -p data/test_data/test1
cd test_scripts
bash test1_perfect_scenario_method_performance.sh
bash test1_selection_factor_effect.sh
cd ..
```

## Experiment 2: recovering branch lengths using pairwise distances with errors
The tests in this part corresponds to section III.C of the manuscript. 
```bash
mkdir -p data/test_data/test2
cd test_scripts
bash test2_distance_matrix_with_errors.sh
cd ..
```


