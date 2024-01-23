import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def combine_df(ref, inf, orient='horizontal'):
    df_ref = pd.read_table(ref)
    df_inf = pd.read_table(inf)
    if orient == 'vertical':
        df_ref['type'] = ['original'] * len(df_ref['child'])
        df_inf['type'] = ['inferred'] * len(df_inf['child'])
        merged_df = pd.concat([df_ref, df_inf])
    else:
        df_ref.rename(columns={'edge_length': 'original_edge_length'}, inplace=True)
        df_inf.rename(columns={'edge_length': 'inferred_edge_length'}, inplace=True)
        merged_df = pd.merge(df_ref, df_inf, how='inner', on=['#parent', 'child'])
    return merged_df


def scatter_plot_single(df, x, y, **kwargs):
    sns.scatterplot(data=df, x=x, y=y, color=kwargs['color'])
    plt.title(kwargs['title'])
    plt.savefig(kwargs['outfile'])


def L1_error():
    pass


def get_corr_coeff():
    pass
