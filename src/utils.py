import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import glob
import re
import plotly.express as px
import seaborn as sns
import time



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
    df_dict = {'method': [], 'perturbation': [], 'threshold': [], 'L1 error': [], 'Corr coeff': []}
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
            corr_coeff = get_corr_coeff(df['original_edge_length'], df['inferred_edge_length'])
            df_dict['method'].append(method)
            df_dict['threshold'].append(float(threshold))
            df_dict['perturbation'].append(float(perturb))
            df_dict['L1 error'].append(float(l1_error))
            df_dict['Corr coeff'].append(float(corr_coeff))
    final_df = pd.DataFrame.from_dict(df_dict)
    print(final_df)
    return final_df


def make_df_lambda(inf_dir, ref_dir, file_pattern):
    ref_files = glob.glob(f"{ref_dir}/{file_pattern}*")
    file_prefixes = [os.path.basename(f).split('.')[0] for f in ref_files]
    df_dict = {'Regularization factor': [], 'L1 error': [], 'Corr coeff': []}
    for i, p in enumerate(file_prefixes):
        inf_files = glob.glob(f"{inf_dir}/{p}*")
        if len(inf_files) == 0:
            continue
        for f in inf_files:
            lamb = re.search("lambda-([^_\.]*)", f).group(1)
            df = combine_df(ref=ref_files[i], inf=f)
            l1_error = L1_error(df['original_edge_length'], df['inferred_edge_length'])
            corr_coeff = get_corr_coeff(df['original_edge_length'], df['inferred_edge_length'])
            df_dict['L1 error'].append(float(l1_error))
            df_dict['Corr coeff'].append(float(corr_coeff))
            df_dict['Regularization factor'].append(float(lamb))
    final_df = pd.DataFrame.from_dict(df_dict)
    print(final_df)
    return final_df


def make_df_factor(inf_dir, ref_dir, file_pattern):
    ref_files = glob.glob(f"{ref_dir}/{file_pattern}*")
    file_prefixes = [os.path.basename(f).split('.')[0] for f in ref_files]
    df_dict = {'Multiples of rank': [], 'L1 error': [], 'Corr coeff': [], 'r-ary': []}
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
            df_dict['L1 error'].append(float(l1_error))
            df_dict['Corr coeff'].append(float(corr_coeff))
            df_dict['Multiples of rank'].append(float(factor))
            df_dict['r-ary'].append(r)
    final_df = pd.DataFrame.from_dict(df_dict)
    print(final_df)
    return final_df

def make_df_time(inf_dir, ref_dir, file_pattern):
    df_dict = {'Tree size': [], 'Method': [], 'Time': [], 'L1 error': []}
    ref_files = glob.glob(f"{ref_dir}/{file_pattern}")
    for t in ref_files:
        base_name = os.path.basename(t).split('.')[0]
        A_file = glob.glob(f"{ref_dir}/{base_name}*_A.npz")
        if len(A_file) < 1:
            continue
        else:
            A_file = glob.glob(f"{ref_dir}/{base_name}*_A.npz")[0]
            print(base_name)
            print(A_file)
            y_file = glob.glob(f"{ref_dir}/{base_name}*_y.npy")[0]
            edge_file = glob.glob(f"{ref_dir}/{base_name}*_edges.npy")[0]
            pw_dist = glob.glob(f"{ref_dir}/{base_name}*_pw-distance.npz")[0]
            basis_file = glob.glob(f"{ref_dir}/{base_name}*_leaf-nodes.npy")[0]
            naive_nnls_out = f"{inf_dir}/{base_name}_recover_nnls.txt"
            bu_out = f"{inf_dir}/{base_name}_recover_bottom-up.txt"
            tree_size = re.search("n([^_\.]*)", base_name).group(1)
            print(f"NNLS size {tree_size}")
            df_dict['Tree size'] += [tree_size, tree_size]
            df_dict['Method'].append('naive nnls')
            start_time = time.time()
            os.system(f"python solve_branch_lengths.py -m nnls -t {t} -A {A_file} -y {y_file} -l {edge_file} "
                      f"-o {naive_nnls_out} -f 5 -i 100")
            end_time = time.time()
            df_dict['Time'].append(end_time - start_time)
            comparison_df = combine_df(t, naive_nnls_out)
            df_dict['L1 error'].append(L1_error(comparison_df['original_edge_length'],
                                       comparison_df['inferred_edge_length']))
            print(f"bottom up size {tree_size}")
            df_dict['Tree size'].append("bottom-up")
            start_time = time.time()
            os.system(f"python solve_branch_lengths.py -m bottom-up -t {t} -pd {pw_dist} -l {basis_file} "
                      f"-o {bu_out} -i 100")
            end_time = time.time()
            df_dict['Time'].append(end_time - start_time)
            comparison_df = combine_df(t, bu_out)
            df_dict['L1 error'].append(L1_error(comparison_df['original_edge_length'],
                                                comparison_df['inferred_edge_length']))
    final_df = pd.DataFrame.from_dict(df_dict)
    print(final_df)
    return final_df



def scatter_plot_single(df, x, y, **kwargs):
    corr_coeff = round(get_corr_coeff(df[x], df[y])[1, 0], 3)
    l1_err = round(L1_error(df[x], df[y]), 2)
    sns.scatterplot(data=df, x=x, y=y, color=kwargs['color'])
    plt.title(format_title(kwargs['file_name'], corr_coeff, l1_err))
    plt.savefig(kwargs['outfile'])


def format_title(file_name, corr_coeff, l1_err):
    base_name = os.path.basename(file_name)
    root = os.path.splitext(base_name)[0]
    components = root.split('_')
    component_dict = dict()
    print(file_name)
    for component in components:
        if component.startswith('repeat') or component.startswith('recover'):
            pass
        elif component.startswith('naive') or component.startswith('regularized') or component.startswith('bottom'):
            component_dict['method'] = component
        elif component.startswith('r') and len(component) < 5:
            component_dict['r'] = component[1:]
        elif component.startswith('perturb'):
            component_dict['perturb'] = float(component.split('-')[1])
    print(component_dict)
    if component_dict['perturb'] > 0:
        return f"{component_dict['r']}-ary tree {component_dict['perturb']*100}% perturbation recovered using {component_dict['method']}\n" \
               f"Correlation Coefficient: {corr_coeff} \n" \
               f"L1 error: {l1_err}"
    else:
        return f"{component_dict['r']}-ary tree no perturbation recovered using {component_dict['method']}\n" \
               f"Correlation Coefficient: {corr_coeff} \n" \
               f"L1 error: {l1_err}"



def scatter_plot_multiple(df, x, y, **kwargs):
    sns.set_palette('colorblind')
    sns.scatterplot(data=df, x=x, y=y, hue=kwargs['hue'])
    plt.title(kwargs['title'])
    plt.savefig(kwargs['outfile'])


def plot_line(df, x, y, out, hue=None, style=None, marker='o'):
    sns.lineplot(data=df, x=x, y=y, hue=hue, style=style, marker=marker)
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



def L1_error(arr1, arr2):
    l1_error = np.mean(np.abs(arr1 - arr2))
    return l1_error

def get_corr_coeff(arr1, arr2):
    return np.corrcoef(arr1, arr2)[1, 0]
