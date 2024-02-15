import argparse
import sys
sys.path.append('../src')
import utils
import os


def main():
    parser = argparse.ArgumentParser(description="Compare recovered edge lists by directories.")
    parser.add_argument('-i', "--inferred_dir", help="directory that contains inferred edge lists.")
    parser.add_argument("-r", "--reference_dir", help="directory that contains reference edge lists.")
    parser.add_argument("-x", "--x", help="x axis")
    parser.add_argument("-y", "--y", help="y axis")
    parser.add_argument("-z", "--z", help="z axis. Optional.")
    parser.add_argument("-hue", "--hue", help="Color by")
    parser.add_argument("-o", "--out_file", help="Path to save the plot to.")
    parser.add_argument("-style", "--style", help="Group by which line pattern differ.")
    parser.add_argument("-ip", "--inferred_file_pattern", help="File pattern for inferred files. e.g. *naive*", default="")



    args = parser.parse_args()
    if args.z: #plot 3D
        df = utils.make_df_perturbation_threshold(args.inferred_dir, args.reference_dir, "*.txt")
        utils.plot_3D(df, x=args.x, y=args.y, z=args.z, hue=args.hue)
    else: #plot boxplot
        if args.x == 'Multiples of rank':
            df = utils.make_df_factor(args.inferred_dir, args.reference_dir, '*.txt')
        elif args.x == 'Regularization factor':
            df = utils.make_df_lambda(args.inferred_dir, args.reference_dir, "*.txt")
        elif args.x == 'perturbation' or args.x == 'threshold':
            df = utils.make_df_perturbation_threshold(args.inferred_dir, args.reference_dir, "*.txt", args.inferred_file_pattern)
        else:
            print("Please check argument x.")
        utils.plot_line(df, x=args.x, y=args.y, hue=args.hue, style=args.style, out=args.out_file)



main()
