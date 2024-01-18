import sys
import argparse
import numpy as np
sys.path.append('..')
sys.path.append('../src')
import trees as tr
import solvers as solvers


def main():
    parser = argparse.ArgumentParser(description="Recover branch lengths of a given tree.")
    parser.add_argument('-t', '--tree', help="Tree file")
    parser.add_argument('-A', '--A', help="A matrix file")
    parser.add_argument('-pd', '--pairwise_distance', help="PW distance file")
    parser.add_argument('-o', '--outfile_name', help="Output file name.")

    args = parser.parse_args()

    tree = tr.read_edge_list(args.tree)
    if not args.pairwise_distance:
        pw_matrix, labels = tr.make_distance_matrix(tree)
    #if not args.A:
    #    A, y, edges = tr.make_matrix_A(tree, pw_matrix, labels)
    solver = solvers.BranchLengthSolver()
    #y = np.asarray(y.T)[0]
    #x = solver.lsq_solver(A, y)
    #tr.save_edge_lengths_solution(edges, dict(zip(edges, x)), args.outfile_name)
    solution = solver.deterministic_solver(tree, pw_matrix, labels)
    print(solution)



main()