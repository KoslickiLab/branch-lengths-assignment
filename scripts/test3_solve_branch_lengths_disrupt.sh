#!/bin/bash
set -e

#generate trees
output_dir='../data/test_data/test3'
#for r in {3,5,7}
#do
#  for i in {1..10}
#  do
#    file_name="n1000_r"$r"_disrupt_"$i".txt"
#    echo "$file_name"
#    python generate_tree.py -n 1000 -r $r -od $output_dir -o $file_name -d
#  done
#done

#generate necessary inputs
#for f in $output_dir/*.txt
#do
#  for perturb in 0.1 0.2 0.4 0.6 0.8
#  do
#    base_name=$(basename $f .txt)"_perturbed_"$perturb
#    echo $base_name
#    python make_lin_sys_input.py -t $f -od $output_dir -o "$base_name" -p "$perturb"
#  done
#done

#generate output using nnls method
#mkdir "$output_dir"/results
for tree in "$output_dir"/*.txt
do
  echo $tree
  base_name=$(basename $tree .txt)
  for perturb in 0.1 0.2 0.4 0.6 0.8
  do
   A_file="$output_dir"/"$base_name"_perturb-"$perturb"_A.npz
   y_file="$output_dir"/"$base_name"_perturb-"$perturb"_y.npy
   edge_file="$output_dir"/"$base_name"_perturb-"$perturb"_edges.npy
   pd="$output_dir"/"$base_name"_perturb-"$perturb"_pw-distance.npz
   basis_file="$output_dir"/"$base_name"_perturb-"$perturb"_leaf-nodes.npy
   naive_nnls_out="$output_dir"/results/"$base_name"_perturb-"$perturb"_recover_naive-nnls.txt
  regularized_nnls_out="$output_dir"/results/"$base_name"_perturb-"$perturb"_recover_regularized-nnls_lambda-1.txt
  bu_out="$output_dir"/results/"$base_name"_perturb-"$perturb"_recover_bottom-up.txt
   echo "naive"
   python solve_branch_lengths.py -m nnls -t $tree -A $A_file -y $y_file -l $edge_file -o $naive_nnls_out -f 5 -i 100
   echo "regularized"
   python solve_branch_lengths.py -m nnls -t $tree -A $A_file -y $y_file -l $edge_file -o $regularized_nnls_out -f 5 -r 1 -i 100
   echo "bottom-up"
   python solve_branch_lengths.py -m bottom-up -t $tree -pd $pd -l $basis_file -o $bu_out -i 100
  done
done

#plot scatterplot
#for ref in "$output_dir"/*.txt
#do
#  for perturb in 0.1 0.2 0.4 0.6 0.8
#  do
#    base_name=$(basename $ref .txt)
#    echo $base_name
#    bu_result="$output_dir"/results/"$base_name"_perturbed_"$perturb"_recover_bottom-up.txt
#    bu_out="$output_dir"/results/"$base_name"_"$perturb"_compare_bottom-up.png
#    bu_result_no_repeat="$output_dir"/results/"$base_name"_perturbed_"$perturb"_recover_bottom-up_no_repeat.txt
#    bu_out_no_repeat="$output_dir"/results/"$base_name"_"$perturb"_compare_bottom-up_no_repeat.png
#    #python compare_edge_lists.py -r $ref -i $bu_result -o $bu_out -c dodgerblue
#    python compare_edge_lists.py -r $ref -i $bu_result_no_repeat -o $bu_out_no_repeat -c slateblue
#    nnls_result="$output_dir"/results/"$base_name"_perturbed_"$perturb"_recover_nnls.txt
#    nnls_result_r1="$output_dir"/results/"$base_name"_perturbed_"$perturb"_recover_nnls_r1.txt
#    nnls_out="$output_dir"/results/"$base_name"_perturbed_"$perturb"_compare_nnls.png
#    nnls_out_r1="$output_dir"/results/"$base_name"_perturbed_"$perturb"_compare_nnls_r1.png
#    #python compare_edge_lists.py -r $ref -i $nnls_result -o $nnls_out -c coral
#    #python compare_edge_lists.py -r $ref -i $nnls_result_r1 -o $nnls_out_r1 -c seagreen
#  done
#done
