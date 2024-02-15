#!/bin/bash
set -e

input_dir='../data/test_data/test4/r5'
output_dir='../data/test_data/test5/results'

for tree in "$input_dir"/*.txt
do
  base_name=$(basename $tree .txt)
  for lambda in 1 5 10 20 30 100
  do
    A_file="$input_dir"/"$base_name"_perturb-0.2_threshold-0.5_A.npz
    y_file="$input_dir"/"$base_name"_perturb-0.2_threshold-0.5_y.npy
    edge_file="$input_dir"/"$base_name"_perturb-0.2_threshold-0.5_edges.npy
    regularized_nnls_out="$output_dir"/"$base_name"_perturb-0.2_threshold-0.5_lambda-"$lambda"_recover_regularized-nnls.txt
    echo $tree $lambda
    python solve_branch_lengths.py -m nnls -t $tree -A $A_file -y $y_file -l $edge_file -o $regularized_nnls_out -f 5 -r $lambda -i 100
  done
done