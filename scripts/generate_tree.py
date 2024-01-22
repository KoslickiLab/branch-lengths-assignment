import sys
import argparse
sys.path.append('../src')
import trees as tr


out_dir = '../data/simulated_trees'

def main():
    parser = argparse.ArgumentParser(description="Generate a tree based on user given n and r.")
    parser.add_argument('-n', '--n', type=int, help="number of nodes.")
    parser.add_argument('-r', '--r', type=int, help="max num of nodes at a given node.")
    parser.add_argument('-o', '--out', type=str, help="output name. No need directory.")
    parser.add_argument('-od', '--out_dir', type=str, help="output directory.", default=out_dir)
    parser.add_argument('-d', '--disrupt', action="store_true")

    args = parser.parse_args()
    n = args.n
    r = args.r
    save_file = args.out
    output_path = f"{args.out_dir}/{save_file}"
    disrupt = args.disrupt

    tree = tr.make_tree(r=r, n=n, disrupt=disrupt)
    tr.save_tree_as_edge_list(tree, output_path)



main()