import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import glob
import re
import plotly.express as px
import seaborn as sns
import time
import networkx as nx
import itertools as it


def combine_df(ref, inf, orient='horizontal'):
    df_ref = pd.read_table(ref)
    df_inf = pd.read_table(inf)
    if orient == 'vertical':
        df_ref['method'] = ['original'] * len(df_ref['child'])
        df_inf['method'] = ['inferred'] * len(df_inf['child'])
        merged_df = pd.concat([df_ref, df_inf])
    else:
        df_ref.rename(columns={'edge_length': 'original_edge_length'}, inplace=True)
        df_inf.rename(columns={'edge_length': 'inferred_edge_length'}, inplace=True)
        merged_df = pd.merge(df_ref, df_inf, how='inner', on=['#parent', 'child'])
    return merged_df


def make_df_perturbation_threshold(inf_dir, ref_dir, ref_file_pattern, inf_file_suffix=''):
    ref_files = glob.glob(f"{ref_dir}/{ref_file_pattern}*")
    file_prefixes = [os.path.basename(f).split('.')[0] for f in ref_files]
    df_dict = {'Method': [], 'Perturbation proportion': [], 'Perturbation likelihood': [], 'Mean L1 error': []}
    for i, p in enumerate(file_prefixes):
        inf_files = glob.glob(f"{inf_dir}/{p}*{inf_file_suffix}*")
        if len(inf_files) == 0:
            continue
        for f in inf_files:
            method = re.search("recover_([^_\.]*)", f).group(1)
            threshold = re.search("threshold-(.*)_recover", f).group(1)
            perturb = re.search("perturb-(.*)_threshold", f).group(1)
            df = combine_df(ref=ref_files[i], inf=f)
            l1_error = L1_error(df['original_edge_length'], df['inferred_edge_length'])
            df_dict['Method'].append(method)
            df_dict['Perturbation likelihood'].append(float(threshold))
            df_dict['Perturbation proportion'].append(float(perturb))
            df_dict['Mean L1 error'].append(float(l1_error))
    final_df = pd.DataFrame.from_dict(df_dict)
    print(final_df)
    return final_df


def make_df_lambda(inf_dir, ref_dir, file_pattern):
    ref_files = glob.glob(f"{ref_dir}/{file_pattern}*")
    file_prefixes = [os.path.basename(f).split('.')[0] for f in ref_files]
    df_dict = {'Regularization factor': [], 'Mean L1 error': [], 'Corr coeff': []}
    for i, p in enumerate(file_prefixes):
        inf_files = glob.glob(f"{inf_dir}/{p}*")
        if len(inf_files) == 0:
            continue
        for f in inf_files:
            lamb = re.search("lambda-([^_\.]*)", f).group(1)
            df = combine_df(ref=ref_files[i], inf=f)
            l1_error = L1_error(df['original_edge_length'], df['inferred_edge_length'])
            corr_coeff = get_corr_coeff(df['original_edge_length'], df['inferred_edge_length'])
            df_dict['Mean L1 error'].append(float(l1_error))
            df_dict['Corr coeff'].append(float(corr_coeff))
            df_dict['Regularization factor'].append(float(lamb))
    final_df = pd.DataFrame.from_dict(df_dict)
    print(final_df)
    return final_df


def make_df_factor(inf_dir, ref_dir, file_pattern):
    ref_files = glob.glob(f"{ref_dir}/{file_pattern}*")
    file_prefixes = [os.path.basename(f).split('.')[0] for f in ref_files]
    df_dict = {'Selection factor': [], 'Mean L1 error': [], 'Corr coeff': [], 'r-ary': []}
    for i, p in enumerate(file_prefixes):
        inf_files = glob.glob(f"{inf_dir}/{p}*factor*")
        if len(inf_files) == 0:
            continue
        for f in inf_files:
            factor = re.search("factor-([^_\.]*)", f).group(1)
            r = re.search("n1000_r([^_\.]*)", f).group(1)
            df = combine_df(ref=ref_files[i], inf=f)
            l1_error = L1_error(df['original_edge_length'], df['inferred_edge_length'])
            corr_coeff = get_corr_coeff(df['original_edge_length'], df['inferred_edge_length'])
            df_dict['Mean L1 error'].append(float(l1_error))
            df_dict['Corr coeff'].append(float(corr_coeff))
            df_dict['Selection factor'].append(float(factor))
            df_dict['r-ary'].append(r)
    final_df = pd.DataFrame.from_dict(df_dict)
    print(final_df)
    return final_df

def make_df_time(inf_dir, ref_dir, file_pattern):
    df_dict = {'Tree size': [], 'Method': [], 'Time': [], 'Mean L1 error': []}
    ref_files = glob.glob(f"{ref_dir}/{file_pattern}")
    for t in ref_files:
        base_name = os.path.basename(t).split('.')[0]
        A_file = glob.glob(f"{ref_dir}/{base_name}*_A.npz")
        if len(A_file) < 1:
            continue
        else:
            A_file = glob.glob(f"{ref_dir}/{base_name}*_A.npz")[0]
            y_file = glob.glob(f"{ref_dir}/{base_name}*_y.npy")[0]
            edge_file = glob.glob(f"{ref_dir}/{base_name}*_edges.npy")[0]
            pw_dist = glob.glob(f"{ref_dir}/{base_name}*_pw-distance.npz")[0]
            basis_file = glob.glob(f"{ref_dir}/{base_name}*_leaf-nodes.npy")[0]
            naive_nnls_out = f"{inf_dir}/{base_name}_recover_nnls.txt"
            bu_out = f"{inf_dir}/{base_name}_recover_bottom-up.txt"
            tree_size = re.search("n([^_\.]*)", base_name).group(1)
            print(f"NNLS size {tree_size}")
            df_dict['Tree size'] += [int(tree_size), int(tree_size)]
            print(f"tree size: {tree_size}")
            df_dict['Method'].append('naive nnls')
            start_time = time.time()
            os.system(f"python solve_branch_lengths.py -m nnls -t {t} -A {A_file} -y {y_file} -l {edge_file} "
                      f"-o {naive_nnls_out} -pd {pw_dist} -f 5 -i 1 -b -1 0")
            end_time = time.time()
            df_dict['Time'].append(end_time - start_time)
            comparison_df = combine_df(t, naive_nnls_out)
            df_dict['Mean L1 error'].append(L1_error(comparison_df['original_edge_length'],
                                       comparison_df['inferred_edge_length']))
            print(f"bottom up size {tree_size}")
            df_dict['Method'].append("bottom-up")
            start_time = time.time()
            os.system(f"python solve_branch_lengths.py -m bottom-up -t {t} -pd {pw_dist} -l {basis_file} "
                      f"-o {bu_out} -i 1")
            end_time = time.time()
            df_dict['Time'].append(end_time - start_time)
            comparison_df = combine_df(t, bu_out)
            df_dict['Mean L1 error'].append(L1_error(comparison_df['original_edge_length'],
                                                comparison_df['inferred_edge_length']))
    print(df_dict)
    final_df = pd.DataFrame.from_dict(df_dict)
    print(final_df)
    return final_df


def scatter_plot_single(x, y, df=None, detail_title=False, **kwargs):
    if df is not None:
        corr_coeff = get_corr_coeff(df[x], df[y])
        corr_coeff = round(corr_coeff, 3)
        l1_err = round(L1_error(df[x], df[y]), 2)
        sns.scatterplot(data=df, x=x, y=y, color=kwargs.get('color'), s=kwargs.get('s'), maker='.', alpha=0.5)
    else:
        corr_coeff = get_corr_coeff(x, y)
        corr_coeff = round(corr_coeff, 3)
        l1_err = round(L1_error(np.array(x), np.array(y)), 2)
        sns.scatterplot(x=x, y=y, color=kwargs.get('color'), s=kwargs.get('s'), marker='.', alpha=0.5)
    if detail_title:
        plt.title(format_title(kwargs['file_name'], corr_coeff, l1_err, detail_title=True))
    elif kwargs.get('title'):
        plt.title(f"{kwargs['title']}\nCorrelation Coefficient: {corr_coeff}\nMean L1 error: {l1_err}")
    else:
        #plt.title(format_title(kwargs['file_name'], corr_coeff=corr_coeff, l1_err=l1_err))
        plt.title(f"Correlation Coefficient: {corr_coeff}\nMean L1 error: {l1_err}")
    if kwargs.get('xlabel'):
        plt.xlabel(kwargs['xlabel'])
    if kwargs.get('ylabel'):
        plt.ylabel(kwargs['ylabel'])
    if 'yticks' in kwargs:
        plt.yticks(kwargs['yticks'])
    if 'ylim' in kwargs:
        plt.ylim(kwargs['ylim'])
    plt.axline((0, 0), (1, 1))
    plt.savefig(kwargs['outfile'])
    print(kwargs['outfile'])
    #plt.show()


def format_title(file_name, corr_coeff, l1_err, detail_title=False):
    base_name = os.path.basename(file_name)
    root = os.path.splitext(base_name)[0]
    if detail_title:
        components = root.split('_')
        component_dict = dict()
        print(file_name)
        for component in components:
            if component.startswith('repeat') or component.startswith('recover'):
                pass
            elif component.startswith('naive') or component.startswith('regularized') or component.startswith('bottom') or component.startswith('nnls'):
                component_dict['method'] = component
            elif component.startswith('r') and len(component) < 5:
                component_dict['r'] = component[1:]
            elif component.startswith('perturb'):
                component_dict['perturb'] = float(component.split('-')[1])
        print(component_dict)
        if component_dict['perturb'] > 0:
            return f"{component_dict['r']}-ary tree {component_dict['perturb']*100}% perturbation recovered using {component_dict['method']}\n" \
                   f"Correlation Coefficient: {corr_coeff} \n" \
                   f"Mean L1 error: {l1_err}"
        else:
            return f"{component_dict['r']}-ary tree no perturbation recovered using {component_dict['method']}\n" \
                   f"Correlation Coefficient: {corr_coeff} \n" \
                   f"Mean L1 error: {l1_err}"
    else:
        return f"Correlation Coefficient: {corr_coeff}\nMean L1 error: {l1_err}"


def scatter_plot_multiple(df, x, y, **kwargs):
    sns.set_palette('colorblind')
    sns.scatterplot(data=df, x=x, y=y, hue=kwargs['hue'])
    plt.title(kwargs['title'])
    plt.savefig(kwargs['outfile'])


def plot_line(df, x, y, out, hue_order, hue=None, style=None, marker='o'):
    sns.lineplot(data=df, x=x, y=y, hue=hue, style=style, marker=marker, hue_order=hue_order)
    plt.savefig(out)
    plt.show()


def plot_3D(df, x, y, z, hue):
    #x = df['perturbation']
    #y = df['threshold']
    #z = df[metric]
    methods = df['method']

   # ax = plt.axes(projection='3d')
   # color_map = {'naive-nnls': 'coral', 'regularized-nnls': 'seagreen', 'bottom-up': 'slateblue'}
   # cmap = [color_map[i] for i in methods]

    #ax.scatter3D(x, y, z, color='method')
    fig = px.scatter_3d(df, x=x, z=z, y=y, color=hue)
    fig.show()
    #ax.set_xlabel('Perturbation')
    #ax.set_ylabel('Probability of perturbation')
    #ax.set_zlabel(metric.capitalize())
    #plt.show()

def compute_n_combine_leaf_pw_dist(tree1, tree2):
    #tree1 and tree2 have to have identical structure
    start = time.time()
    leaf_nodes = [node for node in tree1 if tree1.out_degree(node) == 0]
    undir_tree1 = tree1.to_undirected()
    pw_dist1 = dict(nx.shortest_path_length(undir_tree1, weight='edge_length'))
    undir_tree2 = tree2.to_undirected()
    print(undir_tree2.edges(data=True))
    pw_dist2 = dict(nx.shortest_path_length(undir_tree2, weight='edge_length'))
    end = time.time()
    print(f'distance computed in {(end-start)/60} minutes')
    leaf_pw_dist1 = []
    leaf_pw_dist2 = []
    pairs = []
    for i, (a, b) in enumerate(it.combinations(leaf_nodes, 2)):
        if i % 1000000 == 0:
            print(i)
        leaf_pw_dist1.append(pw_dist1[a][b])
        leaf_pw_dist2.append(pw_dist2[a][b])
        pairs.append((a, b))
    #df_dict = {'pair': pairs, 'NNLS': leaf_pw_dist1, 'bottom-up': leaf_pw_dist2}
    #df = pd.DataFrame.from_dict(df_dict)
    #df.to_csv('../data/pw_dist_compare_temp.csv', index=False)
    return leaf_pw_dist1, leaf_pw_dist2

def compute_dist_combine_with_ref(tree, ref_pw_dist, label_file):
    leaf_nodes = [node for node in tree if tree.out_degree(node) == 0]
    undir_tree = tree.to_undirected()
    pw_dist = dict(nx.shortest_path_length(undir_tree, weight='edge_length'))
    leaf_pw_dist = []
    labels = open_list_file(label_file)
    index_dict = {v:i for i, v in enumerate(labels)}
    ref_dist_list = []
    for i, (a, b) in enumerate(it.combinations(leaf_nodes, 2)):
        if i % 1000000 == 0:
            print(i)
        leaf_pw_dist.append(pw_dist[a][b])
        ref_dist_list.append(ref_pw_dist[index_dict[a]][index_dict[b]])
    return leaf_pw_dist, ref_dist_list

def open_list_file(file):
    with open(file, 'r') as f:
        lst = f.readlines()
        lst = [l.strip() for l in lst]
    return lst

def L1_error(arr1, arr2):
    l1_error = np.mean(np.abs(arr1 - arr2))
    return l1_error

def get_corr_coeff(arr1, arr2):
    return np.corrcoef(arr1, arr2)[1, 0]
