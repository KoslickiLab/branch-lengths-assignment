#!/bin/bash
set -e

#generate trees
input_dir='../data/test_data/test6'
#for n in 100 500 1000 2000 3000 4000 5000
#do
#  for i in {1..10}
#  do
#    file_name=n"$n"_r10_regular_"$i".txt
#    echo "$file_name"
#    python generate_tree.py -n $n -r 10 -od $input_dir -o $file_name
#  done
#done

#generate necessary inputs
#{
#for i in {1..10}
#do
#  for f in "$input_dir"/*_"$i".txt
#  do
#    echo "time -l python make_lin_sys_input.py -t $f -od $input_dir -p 0.4 -s 0.5 > ${f%.txt}.log 2>&1"
#  done
#done
#} | xargs -I{} -P4 bash -c 'eval $1' -- {} &

for n in 100 500 1000 2000 3000 4000 5000
do
  for f in "$input_dir"/batch1/n"$n"_*.txt
  do
  echo $f
  python make_lin_sys_input.py -t $f -od "$input_dir"/batch1 -p 0.4 -s 0.5
  done
done

python time_solver.py -r ../data/test_data/test6/batch1 -i ../data/test_data/test6/results