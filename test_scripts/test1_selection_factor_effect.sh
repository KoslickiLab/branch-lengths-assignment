#!/bin/bash
set -e

#generate trees
output_dir='../data/test_data/test1'
for tree in "$output_dir"/*.txt
do
  for factor in 5 10 15 20 25 30 50 100 150 200
  do
    echo $tree $factor
    base_name=$(basename $tree .txt)
    A_file="$output_dir"/"$base_name"_perturb-0_A.npz
    y_file="$output_dir"/"$base_name"_perturb-0_y.npy
    edge_file="$output_dir"/"$base_name"_perturb-0_edges.npy
    out_file_prefix="$output_dir"/results/"$base_name"_perturb-0_factor-"$factor"_recover
    python solve_branch_lengths.py -m nnls -t $tree -A $A_file -y $y_file -l $edge_file -o "$out_file_prefix"_naive_nnls.txt -f $factor -i 100
  done
done

python compare_all_and_plot.py -i ../data/test_data/test1/results -r ../data/test_data/test1 -x 'Selection factor' -y 'Mean L1 error' -o ../data/plots/line_factor.png -hue r-ary