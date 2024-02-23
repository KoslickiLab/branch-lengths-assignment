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
    parser.add_argument('-A', '--A', help="A matrix file. Only needced for nnls method.")
    parser.add_argument('-pd', '--pairwise_distance', help="PW distance file")
    parser.add_argument('-y', '--y', help="y vector file. Only needed for nnls method")
    parser.add_argument('-l', '--labels', help="Label file. For bottom-up method, leaf nodes. For nnls, edges "
                                              "corresponding to y")
    parser.add_argument('-o', '--outfile_name', help="Output file path.")
    parser.add_argument('-m', '--method', help="solving method", choices=['nnls', 'bottom-up'], default='nnls')
    parser.add_argument('-i', '--itr_num', type=int, help="Iteration number", default=1)
    parser.add_argument('-f', '--factor', type=int, help='Selects <--factor>*(A.shape[1]) rows for which to do the NNLS', default=5)
    parser.add_argument('-r', '--reg_factor', type=float, help='Regularization factor for the NNLS')
    parser.add_argument('-b', '--bounds', nargs=2, default=[0, 1])

    args = parser.parse_args()

    tree = tr.read_edge_list(args.tree)
    solver = solvers.BranchLengthSolver()
    if args.method == 'nnls':
        if not args.A:
            if not args.pairwise_distance:
                pw_matrix, labels = tr.make_distance_matrix(tree)
            else:
                pw_matrix = np.load(args.pairwise_distance)
                if args.labels.endswith('.txt'):
                    with open(args.labels) as f:
                        leaf_nodes = f.readlines()
                        leaf_nodes = [l.strip() for l in leaf_nodes]
                        leaf_nodes = [l.replace('ko:', '') for l in leaf_nodes]
                else:
                    leaf_nodes = np.load(args.labels)
            A, y, edges = tr.make_matrix_A(tree, pw_matrix, leaf_nodes)
        else:
            A = sparse.load_npz(args.A)
            y = np.load(args.y)
            edges = np.load(args.labels)
            edges = list(map(tuple, edges))
        y = np.asarray(y.T)[0]
        if args.reg_factor:
            x = solver.lsq_solver(A.todense(), y, factor=args.factor, reg_factor=args.reg_factor,
                                  bounds=tuple(args.bounds), regularize=True, itr_num=args.itr_num)
        else:
            x = solver.lsq_solver(A.todense(), y, factor=args.factor, reg_factor=args.reg_factor,
                                  bounds=tuple(args.bounds), itr_num=args.itr_num)
        solution = dict(zip(edges, x))
        tr.save_edge_lengths_solution(edges, solution, args.outfile_name)
    elif args.method == 'bottom-up':
        if not args.pairwise_distance:
            pw_matrix, labels = tr.make_distance_matrix(tree)
        else:
            pw_matrix = np.load(args.pairwise_distance)
            if args.labels.endswith('.txt'):
                with open(args.labels) as f:
                    leaf_nodes = f.readlines()
                    leaf_nodes = [l.strip() for l in leaf_nodes]
                    leaf_nodes = [l.replace('ko:', '') for l in leaf_nodes]
            else:
                leaf_nodes = np.load(args.labels)
        solution = solver.deterministic_solver(tree, pw_matrix, leaf_nodes, args.itr_num)
        tr.save_edge_lengths_solution(solution.keys(), solution, args.outfile_name)
    else:
        print("unrecognized method.")


main()