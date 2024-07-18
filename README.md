## Setup
```bash
git clone https://github.com/KoslickiLab/branch-lengths-assignment.git
cd branch-lengths-assignment
```

## 1. Experiment 1: recovering branch lengths using compatible distance matrices
The tests in this part corresponds to section III.B of the manuscript. There are two tests in this section. The first evaluates the performance of bottom-up, naive NNLS and regularized NNLS methods in restoring branch lengths in the event when the distance matrix is completely compatible with the tree. 
```bash
mkdir -p data/test_data/test1
cd test_scripts
bash test1_solve_branch_lengths.sh
cd ..
```
