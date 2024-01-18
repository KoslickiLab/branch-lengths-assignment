import networkx as nx
import random
import numpy as np
import itertools as it


# create random solvable tree
def make_tree(r, n, disrupt=False):
    if r <= 2:
        print("Warning: tree not solvable.")
    tree = nx.full_rary_tree(r, n)
    nx.set_edge_attributes(tree, values=1, name="edge_length")
    weighted_tree = nx.DiGraph()
    for edge in tree.edges.data():
        new_edge = random.random()
        weighted_tree.add_edge(edge[0], edge[1], edge_length=new_edge)
    root = [node for node in tree if weighted_tree.in_degree(node) == 0][0]
    weighted_tree = nx.relabel_nodes(weighted_tree, {root: 'root'})
    if disrupt:
        #remove some random edges while keeping the tree still solvable
        removable_num = r-2
        remove_num = random.randint(1, removable_num)
        root = get_root(weighted_tree)
        root_edges = weighted_tree.out_edges(root)
        removable_edges = [e for e in weighted_tree.edges if e not in root_edges]
        remove_nodes = {n for (n, _) in random.sample(removable_edges, remove_num)}
        remove_trees = set()
        for n in remove_nodes:
            remove_trees.update({n for n in nx.dfs_tree(weighted_tree, n).nodes})
        weighted_tree.remove_nodes_from(remove_trees)
    if check_solvable(weighted_tree):
        return weighted_tree
    else:
        print("tree no longer solvable, check again")


def check_solvable(tree:nx.DiGraph):
    root = [node for node in tree if tree.in_degree(node) == 0]
    if sum(1 for _ in tree.successors(root[0])) < 3:
        return False
    for node in tree.nodes:
        if 0 < sum(1 for _ in tree.successors(node)) < 2:
            return False
    return True

def read_edge_list(file):
    tree = nx.read_edgelist(file, comments='#', create_using=nx.DiGraph,
                            delimiter='\t', nodetype=str, data=(('edge_length', float),))
    return tree

def get_root(tree):
    root = [node for node in tree if tree.in_degree(node) == 0]
    return root


def save_tree_as_edge_list(tree, file_name):
    with open(file_name, 'w') as f:
        f.write("#parent\tchild\tedge_length\n")
        for edge in tree.edges(data=True):
            parent = edge[0]
            child = edge[1]
            edge_length = edge[2]['edge_length']
            f.write(f"{parent}\t{child}\t{edge_length}\n")


# make distance matrix
def make_distance_matrix(tree: nx.DiGraph, perturb=False):
    leaf_nodes = [node for node in tree if tree.out_degree(node) == 0]
    undir_tree = tree.to_undirected()
    pw_dist = dict(nx.shortest_path_length(undir_tree, weight='edge_length'))
    pw_dist_matrix = np.ndarray((len(leaf_nodes), len(leaf_nodes)))
    for i, node in enumerate(leaf_nodes):
        for j, another_node in enumerate(leaf_nodes):
            if perturb:
                pw_dist_matrix[i][j] = pw_dist_matrix[j][i] = pw_dist[node][another_node] + np.random.lognormal()
            else:
                pw_dist_matrix[i][j] = pw_dist_matrix[j][i] = pw_dist[node][another_node]
    return pw_dist_matrix, leaf_nodes


# find respective A matrix
def make_matrix_A(tree, pw_dist_matrix, pw_dist_labels):
    edges = tree.edges  # all edges
    undir_tree = tree.to_undirected()
    all_paths = nx.shortest_path(undir_tree)
    leaf_paths = {k: v for (k, v) in all_paths.items() if k in pw_dist_labels}
    node_index_dict = {k: v for v, k in enumerate(pw_dist_labels)}
    pw_dist_vector = list(it.combinations(pw_dist_labels, 2))
    y = [pw_dist_matrix[node_index_dict[i]][node_index_dict[j]] for (i, j) in it.combinations(pw_dist_labels, 2)]
    A = np.ndarray(shape=(len(y), len(edges)))
    for i, (a, b) in enumerate(pw_dist_vector):
        path = convert_path_to_edges(leaf_paths[a][b])
        bin_rep = [int(j in path) for j in edges]
        A[i] = np.array(bin_rep)
    return np.asmatrix(A), np.asmatrix(y).T, edges

def convert_path_to_edges(path):
    edges = []
    for i in range(len(path)-1):
        edges.append((path[i], path[i+1]))
        edges.append((path[i+1], path[i]))
    return edges


def make_matlab_input_matrix(matrix):
    '''
    Convert a matrix to an input suitable for MatLab. Excluding '[]'
    :param matrix: An numpy matrix
    :return: a string representation of the matrix, suitable for MatLab
    '''
    matrix_string = ""
    for row in matrix:
        row_str = str(row)
        row_str = row_str.replace("\n", "")
        row_str = row_str.replace('[[', ' ')
        row_str = row_str.replace(']]', ';')
        matrix_string += row_str
    return matrix_string


def save_edge_lengths_solution(edges, edge_solutions, outfile_name):
    with open(outfile_name, 'w') as f:
        f.write("#parent\tchild\tedge_length\n")
        for (a, b) in edges:
            f.write(f"{a}\t{b}\t{edge_solutions[(a, b)]}\n")