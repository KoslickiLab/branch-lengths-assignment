import argparse
import sys
sys.path.append('../src')
from utils import combine_df, scatter_plot_single
import os


def main():
    parser = argparse.ArgumentParser(description="Given 2 files of edge lists, this script compares them and "
                                                 "outputs a dot plot.")
    parser.add_argument('-r', '--reference', type=str, help='Reference file. Has to be edge list.')
    parser.add_argument('-i', '--inferred', type=str, help='Inferred file(s). Has to be edge list.')
    parser.add_argument('-x', '--x', type=str, default='original_edge_length')
    parser.add_argument('-y', '--y', type=str, default='inferred_edge_length')
    parser.add_argument('-c', '--color', type=str, help='Color of plot', default='blue')
    parser.add_argument('-o', '--outfile', type=str, help='Path to save output to.', default='./out.png')


    args = parser.parse_args()
    merged_df = combine_df(args.reference, args.inferred)
    additional_args = {'color': args.color,
                       'file_name': args.inferred,
                       'outfile': args.outfile}
    scatter_plot_single(merged_df, x=args.x, y=args.y, **additional_args)


main()
