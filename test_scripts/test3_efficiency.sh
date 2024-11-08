#!/bin/bash
set -e

cd ../scripts
#generate trees
input_dir='../data/test_data/test3'
mkdir -p "${input_dir}"
for n in 100 500 1000 2000 3000 4000 5000
do
  for i in {1..10}
  do
    file_name=n"$n"_r10_regular_"$i".txt
    echo "$file_name"
    python generate_tree.py -n $n -r 10 -od $input_dir -o $file_name
  done
done

#generate necessary inputs
{
for i in {1..10}
do
  for f in "$input_dir"/*_"$i".txt
  do
    echo "python make_lin_sys_input.py -t $f -od $input_dir -p 0.4 -s 0.5"
  done
done
} | xargs -I{} -P4 bash -c 'eval $1' -- {} &

mkdir -p ../data/test_data/test3/results
python time_solver.py -r ../data/test_data/test3 -i ../data/test_data/test/results

#python plot_from_df.py -df ../data/plots/time_results_1710817642.csv -y "Time" -x "Tree size" -hue Method -o ../data/plots/time_vs_size.png -t line
#python plot_from_df.py -df ../data/plots/time_results_1710817642.csv -y "L1 error" -x "Tree size" -hue Method -o ../data/plots/L1_error_vs_size.png -t line
