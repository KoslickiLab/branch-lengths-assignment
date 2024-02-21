from scipy.optimize import lsq_linear
import networkx as nx
import random
from itertools import combinations
import numpy as np
import sys
from scipy import sparse
import multiprocessing
from itertools import repeat


class BranchLengthSolver:
    def __init__(self) -> None:
        pass

    def lsq_solver(self, A, y, factor=5, reg_factor=1, bounds=(0, 1), verbose=2, regularize=False, itr_num=1):
        num_rows = int(factor * A.shape[1])
        if num_rows > A.shape[0]:
            num_rows = A.shape[0]
        all_x = []
        for i in range(itr_num):
            row_indices = np.random.choice(A.shape[0], num_rows, replace=False)
            A_small = A[row_indices, :]
            y_small = y[row_indices]
            if regularize:
                #append a row of 1's to A_small
                A_small = sparse.vstack([reg_factor * A_small, sparse.csr_matrix(np.ones(A_small.shape[1]))])
                # append a 0 to y_small
                y_small = np.append(reg_factor * y_small, 0)
            res = lsq_linear(A=A_small, b=y_small, bounds=bounds, verbose=verbose)
            all_x.append(res.x)
        final_x = np.mean(all_x, axis=0)
        return final_x


    # def compute_edges_nnls(self, A, y, bounds, num_iter, factor, reg_factor):
    #     num_threads = 1
    #     pool = multiprocessing.Pool(num_threads)
    #     xs = np.array(pool.map(self.least_square_parallel, zip(range(num_iter), repeat(A), repeat(y), repeat(bounds), repeat(factor),
    #                                                            repeat(reg_factor)), chunksize=num_iter // num_threads))
    #     x = np.mean(xs, axis=0)
    #     return x

    def deterministic_solver(self, tree, pw_dist, labels, iter_num=1):
        s_tree = self.SolvableTree(tree)
        s_tree.group_nodes_by_depth()
        s_tree.make_full_tree()
        final_solution = dict()
        all_solutions = []
        for i in range(iter_num):
            edge_lengths_solution = dict()
            s_tree.get_needed_pairs()
            s_tree.fill_leaf_pairs_distances(pw_dist, labels)
            s_tree.solve_branch_lengths(edge_lengths_solution, len(s_tree.nodes_by_depth) - 1)
            for (a, b) in list(edge_lengths_solution.keys()):
                if a.startswith('dummy') or b.startswith('dummy'):
                    del edge_lengths_solution[(a, b)]
            all_solutions.append(edge_lengths_solution)
        for (a, b) in all_solutions[0].keys():
            all_solutions_ab = [solution[(a, b)] for solution in all_solutions]
            final_solution[(a, b)] = np.sum(all_solutions_ab)/len(all_solutions_ab)
        return final_solution

    class SolvableTree:
        def __init__(self, tree:nx.DiGraph):
            self.tree = tree
            self.root = [node for node in self.tree if self.tree.in_degree(node) == 0][0]
            self.nodes_by_depth = dict()
            self.needed_pairs = dict()
            self.partners = dict()
            self.single_child = []
            self.first_child = dict()

        def get_parent(self, node):
            return next(self.tree.predecessors(node))

        def get_sibling(self, node):
            parent = self.get_parent(node)
            siblings = list(self.tree._succ[parent].keys())
            sibling = random.choice(siblings)
            while sibling == node:
                sibling = random.choice(siblings)
            return sibling

        def get_child(self, node):
            # get one child
            children = list(self.tree._succ[node].keys())
            if len(children) > 0:
                return random.choice(children)
            else:
                return None

        def group_nodes_by_depth(self):
            for node in self.tree.nodes():
                depth = nx.shortest_path_length(self.tree, self.root, node)
                if depth in self.nodes_by_depth:
                    self.nodes_by_depth[depth].append(node)
                else:
                    self.nodes_by_depth[depth] = [node]

        def make_full_tree(self):
            # process tree from root down until the deepest level, if any node has no child, add a dummy node
            dummy_node_count = 0
            for i in range(len(self.nodes_by_depth) - 1):
                for node in self.nodes_by_depth[i]:
                    if not self.get_child(node):
                        self.single_child.append((i, node))
                        dummy_node = 'dummy' + str(dummy_node_count)
                        self.tree.add_edge(node, dummy_node, edge_length=0)
                        self.nodes_by_depth[i + 1].append(dummy_node)
                        dummy_node_count += 1
                        dummy_node = 'dummy' + str(dummy_node_count)
                        self.tree.add_edge(node, dummy_node, edge_length=0)
                        self.nodes_by_depth[i + 1].append(dummy_node)
                        dummy_node_count += 1

        def get_needed_pairs(self):
            # loop over each level from the root and get needed parents of the level below
            for i in range(len(self.nodes_by_depth) - 1):
                if i == 0:  # all siblings
                    self.needed_pairs[1] = dict()
                    self.partners[1] = dict()
                    if len(self.nodes_by_depth[1]) == 1:
                        self.partners[1] = 1
                    elif len(self.nodes_by_depth[1]) == 2:
                        self.needed_pairs[1][(self.nodes_by_depth[1][0], self.nodes_by_depth[1][1])] = 0
                    elif len(self.nodes_by_depth[1]) == 3:
                        (node1, node2, node3) = (self.nodes_by_depth[1][0],
                                                 self.nodes_by_depth[1][1],
                                                 self.nodes_by_depth[1][2])
                        self.needed_pairs[1][(node1, node2)] = 0
                        self.needed_pairs[1][(node2, node3)] = 0
                        self.needed_pairs[1][(node1, node3)] = 0
                        self.needed_pairs[1][(node3, node1)] = 0
                        self.needed_pairs[1][(node3, node2)] = 0
                        self.needed_pairs[1][(node2, node1)] = 0
                        self.partners[1][node1] = [node2, node3]
                        self.partners[1][node3] = [node2, node1]
                    else:  # >= 4
                        node_set = set(self.nodes_by_depth[1])
                        first_node = self.nodes_by_depth[1][0]
                        last_node = self.nodes_by_depth[1][-1]
                        second_node = self.nodes_by_depth[1][1]
                        self.needed_pairs[1][(first_node, second_node)] = 0
                        self.needed_pairs[1][(first_node, last_node)] = 0
                        self.needed_pairs[1][(second_node, last_node)] = 0
                        self.partners[1][first_node] = [second_node, last_node]
                        node_set.discard(first_node)
                        node_set.discard(second_node)
                        while len(node_set) > 1:
                            cur_node = node_set.pop()
                            sib = node_set.pop()
                            self.needed_pairs[1][(cur_node, sib)] = 0
                            self.needed_pairs[1][(cur_node, first_node)] = 0
                            self.needed_pairs[1][(sib, first_node)] = 0
                            self.partners[1][cur_node] = [sib, first_node]
                        if len(node_set) == 1:
                            cur_node = node_set.pop()  # could be last node, but not first nor second
                            self.needed_pairs[1][(cur_node, second_node)] = 0
                            self.needed_pairs[1][(cur_node, first_node)] = 0
                            self.partners[1][cur_node] = [first_node, second_node]
                else:  # i>0 not all children nodes are siblings
                    first_children = set()
                    self.needed_pairs[i + 1] = dict()
                    self.partners[i + 1] = dict()
                    first_node = self.nodes_by_depth[i + 1][0]
                    last_node = self.nodes_by_depth[i + 1][-1]
                    backup_node = self.nodes_by_depth[i + 1][1]
                    node_set = set(self.nodes_by_depth[i + 1])
                    # handle first node
                    sib = self.get_sibling(first_node)
                    if not sib:
                        self.partners[i + 1][first_node] = 0
                    else:
                        self.needed_pairs[i + 1][(first_node, sib)] = 0
                        if sib == last_node:
                            self.needed_pairs[i + 1][(first_node, backup_node)] = 0
                            self.needed_pairs[i + 1][(sib, backup_node)] = 0
                            self.partners[i + 1][first_node] = [sib, backup_node]
                        else:
                            self.needed_pairs[i + 1][(first_node, last_node)] = 0
                            self.needed_pairs[i + 1][(sib, last_node)] = 0
                            self.partners[i + 1][first_node] = [sib, last_node]
                        node_set.discard(sib)
                    node_set.discard(first_node)
                    while len(node_set) > 0:
                        cur_node = node_set.pop()
                        sib = self.get_sibling(cur_node)
                        if not sib:
                            self.partners[i + 1][cur_node] = 0
                            continue
                        if sib == first_node:
                            if cur_node == backup_node:
                                another_node = last_node
                            else:
                                another_node = backup_node
                        elif sib == last_node:
                            if cur_node == first_node:
                                another_node = backup_node
                            else:
                                another_node = first_node
                        else:
                            if cur_node == first_node:
                                another_node = last_node
                            else:
                                another_node = first_node
                        self.needed_pairs[i + 1][(cur_node, sib)] = 0
                        self.needed_pairs[i + 1][(cur_node, another_node)] = 0
                        self.needed_pairs[i + 1][(sib, another_node)] = 0
                        self.partners[i + 1][cur_node] = (sib, another_node)
                        node_set.discard(sib)
                    # first child pairs
                    for node in self.nodes_by_depth[i]:
                        child = self.get_child(node)
                        first_children.add(child)
                        self.first_child[node] = child
                    for (a, b) in combinations(first_children, 2):
                        self.needed_pairs[i + 1][(a, b)] = self.needed_pairs[i + 1][(b, a)] = 0

        def fill_leaf_pairs_distances(self, pw_dist, labels):
            # Can only be run after get_needed_pairs function is run
            try:
                _ = pw_dist[0][0]
            except KeyError:
                pw_dist = pw_dist['arr_0'] #weird numpy issue
            if len(self.needed_pairs) == 0:
                print("Please run get_needed_pairs first")
                return
            label_pos = {k: v for v, k in enumerate(labels)}
            for (a, b) in self.needed_pairs[len(self.nodes_by_depth) - 1]:
                p_a = a
                p_b = b
                if a.startswith('dummy'):
                    p_a = self.get_parent(a)
                    while p_a.startswith('dummy'):
                        p_a = self.get_parent(p_a)
                if b.startswith('dummy'):
                    p_b = self.get_parent(b)
                    while p_b.startswith('dummy'):
                        p_b = self.get_parent(p_b)
                a_index = label_pos[p_a]
                b_index = label_pos[p_b]
                self.needed_pairs[len(self.nodes_by_depth) - 1][(a, b)] = pw_dist[a_index][b_index]

        def update_needed_pairs(self, edge_lengths_solution, level):
            if level >= len(self.nodes_by_depth):
                print(f"level {level} is too big. Max level allowed is {len(self.nodes_by_depth) - 1}.")
                return
            if level < 1:
                return
            for (a, b) in self.needed_pairs[level]:
                a_child = self.first_child[a]
                b_child = self.first_child[b]
                a_child_b_child_dist = self.needed_pairs[level + 1][(a_child, b_child)]
                self.needed_pairs[level][(a, b)] = a_child_b_child_dist - edge_lengths_solution[(a, a_child)] - \
                                                   edge_lengths_solution[(b, b_child)]

        def solve_branch_lengths(self, edge_lengths_solution, level, enforce_positive=True):
            '''
            Solves the branch lengths of the given level
            :param edge_lengths_solution:
            :param level:
            :return:
            '''
            if level < 1:
                return
            elif level == 1 and len(self.needed_pairs[1]) == 1:
                (node1, node2) = list(self.needed_pairs[1])[0]
                parent = self.get_parent(node1)
                edge_lengths_solution[(parent, node1)] = \
                    edge_lengths_solution[(parent, node2)] = self.needed_pairs[1][(node1, node2)] / 2
            else:
                for node in self.partners[level]:
                    parent = self.get_parent(node)
                    if (parent, node) in edge_lengths_solution:
                        continue
                    if self.partners[level][node] == 0:
                        edge_lengths_solution[(parent, node)] = 0
                    else:
                        sib = self.partners[level][node][0]
                        another = self.partners[level][node][1]
                        d1 = self.needed_pairs[level][(node, sib)]
                        d2 = self.needed_pairs[level][(node, another)]
                        d3 = self.needed_pairs[level][(sib, another)]
                        e1 = (d1 + d2 - d3) / 2
                        if enforce_positive:
                            if e1 < 0:
                                e1 = sys.float_info.epsilon
                        edge_lengths_solution[(parent, node)] = e1
                        if (parent, sib) not in edge_lengths_solution:
                            e2 = d1 - e1
                            if enforce_positive:
                                if e2 < 0:
                                    e2 = sys.float_info.epsilon
                            edge_lengths_solution[(parent, sib)] = e2
            self.update_needed_pairs(edge_lengths_solution, level - 1)
            self.solve_branch_lengths(edge_lengths_solution, level - 1)

        def post_process(self, edge_lengths_solution):
            '''
            Even out edges with branch length 0 by sharing half of the ancestor
            :param edge_length_solution:
            :param kegg_tree:
            :return:
            '''
            for i in range(len(self.nodes_by_depth)):
                for node in self.nodes_by_depth[i]:
                    if sum(1 for _ in self.tree.successors(node)) == 1:  # has single child
                        parent = self.get_parent(node)
                        cur_node = node
                        child = self.get_child(cur_node)
                        if child.startswith('dummy') or edge_lengths_solution[(cur_node, child)] != 0:
                            continue
                        nodes_on_the_way = [cur_node]
                        while sum(1 for _ in self.tree.successors(cur_node)) == 1:
                            cur_node = self.get_child(cur_node)
                            if cur_node.startswith('dummy'):
                                break
                            nodes_on_the_way.append(cur_node)
                        ave_edge_length = edge_lengths_solution[(parent, node)] / len(nodes_on_the_way)
                        for node in nodes_on_the_way:
                            edge_lengths_solution[(parent, node)] = ave_edge_length
                            parent = node

        def write_edge_list_preserve_order(self, edge_lengths_solution, out_file):
            with open(self.file, 'r') as f:
                f.readline()
                pairs = f.readlines()
            with open(out_file, 'w') as f:
                f.write("#parent\tchild\tedge_length\n")
                for pair in pairs:
                    pair = pair.strip()
                    (p, c) = pair.split('\t')
                    if (p, c) in edge_lengths_solution:
                        f.write(f"{p}\t{c}\t{edge_lengths_solution[(p, c)]}\n")
                    else:
                        f.write(f"{p}\t{c}\'NA'\n")

