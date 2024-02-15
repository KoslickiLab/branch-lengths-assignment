#!/bin/bash
set -e

#generate trees
output_dir='../data/test_data/test2'
#for r in {3,5,7}
#do
#  for i in {1..10}
#  do
#    file_name="n1000_r"$r"_regular_"$i".txt"
#    echo "$file_name"
#    python generate_tree.py -n 1000 -r $r -od $output_dir -o $file_name
#  done
#done

#generate necessary inputs
#for f in $output_dir/*.txt
#do
#  base_name=$(basename $f .txt)"_perturbed"
#  echo $base_name
#  python make_lin_sys_input.py -t $f -od $output_dir -o "$base_name" -p
#done

#generate output using nnls method
#mkdir "$output_dir"/results
#for tree in "$output_dir"/*.txt
#do
#  echo $tree
#  base_name=$(basename $tree .txt)
#  A_file="$output_dir"/"$base_name"_perturbed_A.npz
#  y_file="$output_dir"/"$base_name"_perturbed_y.npy
#  edge_file="$output_dir"/"$base_name"_perturbed_edges.npy
#  out_file="$output_dir"/results/"$base_name"_perturbed_recover_nnls.txt
#  python solve_branch_lengths.py -m nnls -t $tree -A $A_file -y $y_file -l $edge_file -o $out_file -f 10 -b 1 10
#done

#echo "bottom up"
##generate output using bottom-up method
#for tree in "$output_dir"/*.txt
#do
#  base_name=$(basename $tree .txt)
#  echo $base_name
#  pd="$output_dir"/"$base_name"_perturbed_pw_distance.npz
#  basis_file="$output_dir"/"$base_name"_perturbed_leaf_nodes.npy
#  out_file="$output_dir"/results/"$base_name"_perturbed_recover_bottom-up.txt
#  python solve_branch_lengths.py -m bottom-up -t $tree -pd $pd -l $basis_file -o $out_file
#done

#plot scatterplot
for ref in "$output_dir"/*.txt
do
  base_name=$(basename $ref .txt)
  echo $base_name
  bu_result="$output_dir"/results/"$base_name"_perturbed_recover_bottom-up.txt
  bu_out="$output_dir"/results/"$base_name"_compare_bottom-up.png
  python compare_edge_lists.py -r $ref -i $bu_result -o $bu_out -c dodgerblue
  nnls_result="$output_dir"/results/"$base_name"_perturbed_recover_nnls.txt
  nnls_out="$output_dir"/results/"$base_name"_compare_nnls.png
  python compare_edge_lists.py -r $ref -i $nnls_result -o $nnls_out -c coral
done


