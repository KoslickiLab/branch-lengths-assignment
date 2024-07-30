#!/bin/bash
set -e

cd ../scripts

output_dir='../data/test_data/test2'
#mkdir "$output_dir"/results
#mkdir -p ../data/test_data/test2/r3
#mkdir -p ../data/test_data/test2/r5
#mkdir -p ../data/test_data/test2/r7
#r3_dir="../data/test_data/test2/r3"
#r5_dir="../data/test_data/test2/r5"
#r7_dir="../data/test_data/test2/r7"
all_input_dir=($r3_dir $r5_dir $r7_dir)
##generate trees
#for r in {3,5,7}
#do
#  for i in {1..10}
#  do
#    file_name="n1000_r"$r"_regular_"$i".txt"
#    echo "$file_name"
#    python generate_tree.py -n 1000 -r $r -od $output_dir/r"$r" -o $file_name
#  done
#done
#
##generate necessary inputs
#for dir in "${all_input_dir[@]}"
#do
#for p in 0.01 0.05 0.1 0.2 0.4 0.6 0.8
#do
#  for s in 0.1 0.2 0.4 0.5 0.7 0.9
#  do
#    for f in $dir/*.txt
#    do
#    base_name=$(basename $f .txt)"_perturbed"
#    echo $base_name
#    python make_lin_sys_input.py -t $f -od $dir -p $p -s $s
#    done
#  done
#  done
#done

#generate output
for input_dir in "${all_input_dir[@]}"
do
for tree in "$input_dir"/*.txt
do
  echo $tree
  base_name=$(basename $tree .txt)
  for p in 0.01 0.05 0.1 0.2 0.4 0.6 0.8
  do
    for s in 0.1 0.2 0.4 0.5 0.7 0.9
    do
       A_file="$input_dir"/"$base_name"_perturb-"$p"_threshold-"$s"_A.npz
       y_file="$input_dir"/"$base_name"_perturb-"$p"_threshold-"$s"_y.npy
       edge_file="$input_dir"/"$base_name"_perturb-"$p"_threshold-"$s"_edges.npy
       pd="$input_dir"/"$base_name"_perturb-"$p"_threshold-"$s"_pw-distance.npz
       basis_file="$input_dir"/"$base_name"_perturb-"$p"_threshold-"$s"_leaf-nodes.npy
       nnls_out_file="$output_dir"/results/"$base_name"_perturb-"$p"_threshold-"$s"_recover_nnls.txt
       python solve_branch_lengths.py -m nnls -t $tree -A $A_file -y $y_file -l $edge_file -o $nnls_out_file -f 5 -i 100 -pd $pd -b -1 0
       bu_out_file="$output_dir"/results/"$base_name"_perturb-"$p"_threshold-"$s"_recover_bottom-up.txt
       python solve_branch_lengths.py -m bottom-up -t $tree -pd $pd -l $basis_file -o $bu_out_file
    done
  done
  done
done

python compare_all_and_plot.py -i ../data/test_data/test2/results -r ../data/test_data/test2/r3 -x "Perturbation proportion" -y "Mean L1 error" -style "Perturbation likelihood" -o ../data/plots/line_perturb_vs_threshold_r3_complete.png -hue Method
python compare_all_and_plot.py -i ../data/test_data/test2/results -r ../data/test_data/test2/r5 -x "Perturbation proportion" -y "Mean L1 error" -style "Perturbation likelihood" -o ../data/plots/line_perturb_vs_threshold_r5_complete.png -hue Method
python compare_all_and_plot.py -i ../data/test_data/test2/results -r ../data/test_data/test2/r7 -x "Perturbation proportion" -y "Mean L1 error" -style "Perturbation likelihood" -o ../data/plots/line_perturb_vs_threshold_r7_complete.png -hue Method


