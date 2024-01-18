import sys
sys.path.append('../src')
import trees as tr
import argparse
from scipy.sparse import save_npz
import numpy as np


def main():
    parser = argparse.ArgumentParser(description="Produce matrix A, y and edges")
    parser.add_argument('-t', '--tree_file', type=str, help="tree file")
    parser.add_argument('-od', '--out_dir', type=str, help="outdir", default="../data/matlab_input")
    parser.add_argument('-o', '--out_prefix', type=str, help="output files basename")

    args = parser.parse_args()

    tree = tr.read_edge_list(args.tree_file)
    pw_dist_matrix, leaf_nodes = tr.make_distance_matrix(tree)
    A, y, edges = tr.make_matrix_A(tree, pw_dist_matrix, leaf_nodes)
    np.save(f"{args.out_dir}/{args.out_prefix}_y.npy", y)
    np.save(f"{args.out_dir}/{args.out_prefix}_basis.npy", edges)
    save_npz(f"{args.out_dir}/{args.out_prefix}_pw_distance.npz", pw_dist_matrix)
    save_npz(f"{args.out_dir}/{args.out_prefix}_A.npz", A)




    # with open(outfile, 'w') as f:
    #     f.write(f"A = [{tr.make_matlab_input_matrix(A)}]\n")
    #     f.write(f"y = [{tr.make_matlab_input_matrix(y)}]\n")
    #     f.write(f"edges = {edges}")


main()