# This file runs the inference model for given subject and years

from argparse import ArgumentParser
import os
from util import get_year_month
from analysis import estimate_alpha
import time
import pandas as pd
from tqdm import tqdm

def parse_args():

    parser = ArgumentParser()
    parser.add_argument("--data_loc", required=True,
                        help="path to the folder containing tokenized data")
    parser.add_argument("--dist_path", required=True,
                        help="path to the parquet file containing word distributions")
    parser.add_argument("--subject", required=True,
                        help="subject of interest")
    parser.add_argument("--year", required=True, type=int,
                        help="the year in which the article was published")
    parser.add_argument("--month", default=None, type=int, nargs='+',
                        help="the month in which the article was published")
    parser.add_argument("--output_loc", required=True,
                        help="the path to the folder where the output is saved")

    return parser.parse_args()


if __name__ == "__main__":

    args = parse_args()
    results = {"month":[], "year":[], "alpha":[], "ci":[]}
    os.makedirs(args.output_loc, exist_ok=True)
    log = open("{}/log.txt".format(args.output_loc), "w")
    str_log = ""
    months = args.month
    if months is None:
        if args.year == 2024:
            months = [1, 2, 3, 4, 5]
        else:
            months = list(range(1, 13))

    for file in os.listdir(args.data_loc):
        full_path = os.path.join(args.data_loc, file)
        if ".parquet" in file:
            print(file)
            year, month = get_year_month(file)
            if month in months:
                print("Running MLE for {}, {}, {}".format(args.subject, year, month))
                try:
                    alpha, ci = estimate_alpha(full_path, args.dist_path)
                    results["alpha"].append(alpha)
                    results["ci"].append(ci)
                    results["month"].append(month)
                    results["year"].append(year)
                except (ValueError, IndexError) as e:
                    print("Error {} in file: {}".format(e, full_path))
                    str_log = str_log + str(time.time())
                    str_log = str_log + full_path + "\n"

    df_output = pd.DataFrame.from_dict(results)
    print(results)
    df_output.to_csv("{}/{}_{}.csv".format(args.output_loc, args.subject, args.year))
    log.write(str_log)

