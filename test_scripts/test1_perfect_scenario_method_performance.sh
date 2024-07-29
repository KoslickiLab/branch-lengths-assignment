#!/bin/bash
set -e

cd ../scripts
#generate trees
output_dir='../data/test_data/test1'
for r in {3,5,7}
do
  for i in {1..10}
  do
    file_name="n1000_r"$r"_regular_"$i".txt"
    echo "$file_name"
    python generate_tree.py -n 1000 -r $r -od $output_dir -o $file_name
  done
done

#generate necessary inputs
for f in $output_dir/*.txt
do
  base_name=$(basename $f .txt)"_no_perturb"
  echo $base_name
  python make_lin_sys_input.py -t $f -od $output_dir -o "$base_name"
done

#generate output using 3 methods
mkdir -p ../data/test_data/test1/results
for tree in "$output_dir"/*.txt
do
  echo $tree
  base_name=$(basename $tree .txt)
  pd="$output_dir"/"$base_name"_no_perturb_pw-distance.npz
  A_file="$output_dir"/"$base_name"_no_perturb_A.npz
  y_file="$output_dir"/"$base_name"_no_perturb_y.npy
  edge_file="$output_dir"/"$base_name"_no_perturb_edges.npy
  leaf_nodes_file="$output_dir"/"$base_name"_no_perturb_leaf-nodes.npy
  out_file_prefix="$output_dir"/results/"$base_name"_no_perturb_recover
  python solve_branch_lengths.py -m nnls -t $tree -A $A_file -y $y_file -l $edge_file -o "$out_file_prefix"_naive_nnls.txt -f 5 -i 100
  python solve_branch_lengths.py -m nnls -t $tree -A $A_file -y $y_file -l $edge_file -o "$out_file_prefix"_regularized_nnls.txt -f 5 -i 100 -r 1
  python solve_branch_lengths.py -m bottom-up -t $tree -pd $pd -l $leaf_nodes_file -o "$out_file_prefix"_bottom-up.txt
done

#plot scatterplot
for ref in "$output_dir"/*.txt
do
  base_name=$(basename $ref .txt)
  echo $base_name
  bu_result="$output_dir"/results/"$base_name"_perturb-0_recover_bottom-up.txt
  bu_out="$output_dir"/results/"$base_name"_compare_bottom-up.png
  python compare_edge_lists.py -r $ref -i $bu_result -o $bu_out -c dodgerblue -s 20
  naive_nnls_result="$output_dir"/results/"$base_name"_perturb-0_recover_naive-nnls.txt
  naive_nnls_out="$output_dir"/results/"$base_name"_compare_naive-nnls.png
  python compare_edge_lists.py -r $ref -i $naive_nnls_result -o $naive_nnls_out -c coral -s 20
  regularized_nnls_result="$output_dir"/results/"$base_name"_perturb-0_recover_regularized-nnls.txt
  regularized_nnls_out="$output_dir"/results/"$base_name"_compare_regularized-nnls.png
  python compare_edge_lists.py -r $ref -i $regularized_nnls_result -o $regularized_nnls_out -c seagreen -s 20
done
