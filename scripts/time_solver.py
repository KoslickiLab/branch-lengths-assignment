import sys
import argparse
sys.path.append('..')
sys.path.append('../src')
import utils
import time


def main():
    parser = argparse.ArgumentParser(description="Given a directory, solve branch lengths using 2 methods and time."
                                                 "Returns a dataframe file for the times for 2 methods for each size.")
    parser.add_argument('-r', '--ref_dir', help='Path to original tree files.')
    parser.add_argument('-i', '--inf_dir', help='Path to inferred tree files.')
    parser.add_argument('-fp', '--file_pattern', help='File pattern to match.', default='*.txt')
    parser.add_argument('-o', '--output_dir', help='Path to output directory.', default='../data/plots')

    args = parser.parse_args()
    df = utils.make_df_time(args.inf_dir, args.ref_dir, args.file_pattern)
    df.to_csv(f"{args.output_dir}/time_results_{str(time.time()).split('.')[0]}.csv")
    utils.plot_line(df, x='Tree size', y='Time', hue='Method', out=f"{args.output_dir}/time_vs_size.png")
    utils.plot_line(df, x='Tree size', y='L1 error', hue='Method', out=f"{args.output_dir}/L1_error_vs_size.png")


main()
