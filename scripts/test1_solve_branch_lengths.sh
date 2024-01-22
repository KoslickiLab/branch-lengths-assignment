#!/bin/bash

#generate trees
output_dir='../data/test_data'
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
for f in $output_dir/*
do
  base_name=$(basename $f .txt)"_no_perturb"
  echo $base_name
  python make_lin_sys_input.py -t $f -od $output_dir -o "$base_name"
done

