import sys
import argparse
import numpy as np
from scipy import sparse
sys.path.append('..')
sys.path.append('../src')
import trees as tr
import solvers as solvers



def main():
    parser = argparse.ArgumentParser(description="Recover branch lengths of a given tree.")
    parser.add_argument('-t', '--tree', help="Tree file")
    parser.add_argument('-A', '--A', help="A matrix file")
    parser.add_argument('-pd', '--pairwise_distance', help="PW distance file")
    parser.add_argument('-y', '--y', help="y vector file")
    parser.add_argument('-b', '--basis', help="Basis file")
    parser.add_argument('-o', '--outfile_name', help="Output file name.")
    parser.add_argument('-m', '--method', help="solving method", choices=['nnls', 'bottom-up'])
    parser.add_argument('-i', '--iter_num', help="Iteration number", default=1)

    args = parser.parse_args()

    tree = tr.read_edge_list(args.tree)
    if not args.pairwise_distance:
        pw_matrix, labels = tr.make_distance_matrix(tree)
    else:
        pw_matrix = np.load(args.pairwise_distance)
        labels = np.load(args.basis)
    if not args.A:
        A, y, edges = tr.make_matrix_A(tree, pw_matrix, labels)
    else:
        A = sparse.load_npz(args.A)
        y = np.load(args.y)
        edges = np.load(args.basis)
        print(edges)
        edges = list(map(tuple, edges))
        print(edges)
    y = np.asarray(y.T)[0]
    solver = solvers.BranchLengthSolver()
    if args.method == 'nnls':
        x = solver.lsq_solver(A.todense(), y)
        solution = dict(zip(edges, x))
        tr.save_edge_lengths_solution(edges, solution, args.outfile_name)
    else:
        solution = solver.deterministic_solver(tree, pw_matrix, labels)
        tr.save_edge_lengths_solution(edges, solution, args.outfile_name)


main()