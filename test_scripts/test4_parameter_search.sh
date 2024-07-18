#!/bin/bash
set -e

#generate trees
#output_dir='../data/test_data/test4'
input_dir=$1
#for r in {3,5,7,10}
#do
#  for i in {1..10}
#  do
#    file_name="n1000_r"$r"_regular_"$i".txt"
#    echo "$file_name"
#    python generate_tree.py -n 1000 -r $r -od $input_dir -o $file_name
#  done
#done

##generate necessary inputs
#for f in $input_dir/*.txt
#do
#  for perturb in 0.1 0.2 0.4 0.6 0.8
#    do
#    for t in 0.1 0.2 0.4 0.5 0.7 0.9
#      do
#        echo $f
#        echo $perturb $t
#        python make_lin_sys_input.py -t $f -od $input_dir -p "$perturb" -s $t
#      done
#  done
#done

#generate output
output_dir="$input_dir"/../results
for tree in "$input_dir"/*.txt
do
  echo $tree
  base_name=$(basename $tree .txt)
  for perturb in 0.1 0.2 0.4 0.6 0.8
  do
    for t in 0.1 0.2 0.4 0.5 0.7 0.9
      do
        A_file="$input_dir"/"$base_name"_perturb-"$perturb"_threshold-"$t"_A.npz
        y_file="$input_dir"/"$base_name"_perturb-"$perturb"_threshold-"$t"_y.npy
        edge_file="$input_dir"/"$base_name"_perturb-"$perturb"_threshold-"$t"_edges.npy
        pd="$input_dir"/"$base_name"_perturb-"$perturb"_threshold-"$t"_pw-distance.npz
        basis_file="$input_dir"/"$base_name"_perturb-"$perturb"_threshold-"$t"_leaf-nodes.npy
        naive_nnls_out="$output_dir"/"$base_name"_perturb-"$perturb"_threshold-"$t"_recover_naive-nnls.txt
        regularized_nnls_out="$output_dir"/"$base_name"_perturb-"$perturb"_threshold-"$t"_recover_regularized-nnls.txt
        bu_out="$output_dir"/"$base_name"_perturb-"$perturb"_threshold-"$t"_recover_bottom-up.txt
        echo "naive"
        python solve_branch_lengths.py -m nnls -t $tree -A $A_file -y $y_file -l $edge_file -o $naive_nnls_out -f 5 -i 100
        echo "regularized"
        python solve_branch_lengths.py -m nnls -t $tree -A $A_file -y $y_file -l $edge_file -o $regularized_nnls_out -f 5 -r 1 -i 100
        echo "bottom-up"
        python solve_branch_lengths.py -m bottom-up -t $tree -pd $pd -l $basis_file -o $bu_out -i 100
   done
  done
done