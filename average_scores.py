import pandas as pd
import os
import argparse

parser = argparse.ArgumentParser(description='SETI Classifier - Average Scores of Several Models')

parser.add_argument('input', metavar='PATH',
                    help="Input folder of CSVs of individual models' results")
parser.add_argument('output', metavar='PATH',
                    help='Output CSV file path')

args = parser.parse_args()


def average_scores(input_folder, output_path):
    """
    Averages scores of several CSV files generated by test.py

    Args:
        input_folder (path): folder with models' scores' CSVs in it.
        output_path (path): path of output CSV file with averaged scores, ready for submission to SETI scoreboards
    """
    csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]
    model_scores = []
    for i, csv in enumerate(csv_files):
        df = pd.read_csv(os.path.join(input_folder, csv), index_col=0, header=None)
        if i == 0:
            index = df.index
        else:
            assert index.equals(df.index), "Indices of one or more files do not match!"
        model_scores.append(df)
    print "Read %d files. Averaging..." % len(model_scores)

    concat_scores = pd.concat(model_scores)
    averaged_scores = concat_scores.groupby(level=0).mean()
    assert averaged_scores.shape[0] == len(list(index)), "Something went wrong when concatenating/averaging!"
    averaged_scores = averaged_scores.reindex(index)

    averaged_scores.to_csv(output_path, header=False, index=True)
    print "Averaged scores saved to %s" % output_path


if __name__ == '__main__':
    average_scores(args.input, args.output)
