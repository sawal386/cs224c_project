## This file is used generating the data


from helper import convert_raw_json
import json
from argparse import ArgumentParser
from util import *
from log import setup_logger

def parse_args():

    parser = ArgumentParser()
    parser.add_argument("--input_loc", required=True,
                        help="path to the folder containing the raw json files")
    parser.add_argument("--subject", required=True,
                        help="subject of interest")
    parser.add_argument("--year", required=True, type=int,
                        help="the year in which the article was published")
    parser.add_argument("--month", default=None, type=int,
                        help="the month in which the article was published")
    parser.add_argument("--output_loc", required=True,
                        help="the path to the folder where the output is saved")

    return parser.parse_args()


if __name__ == "__main__":

    args = parse_args()
    #base_json = "/Users/sawal/Documents/stanford_ms_icme/courses/spring_24/cs224c/project/data"
    #subject = "medicine"
    #year = 2024
    #month = 1
    json_path = "{}/{}.json".format(args.input_loc, args.year)
    output_folder = "{}/{}/{}".format(args.output_loc, args.subject, args.year)
    logger = setup_logger("my_logger", "run.log")
    with open(json_path, "r") as f:
        raw_json = json.load(f)

    all_collection = convert_raw_json(raw_json)
    subj_collection = all_collection.get_articles_subject(args.subject)
    # save the entire collection
    save_pkl(subj_collection, output_folder, "{}_{}_whole".format(args.subject, args.year))

    logger.info("Subject size:{}".format(subj_collection.get_size()))
    total_data = 0
    if args.month is None:
        for m in range(1, 13):
            logger.debug("Generating data for subject: {}, year: {}, month:{}".format(args.subject,
                                                                               args.year, m))
            name = "{}_{}_{}".format(args.subject, args.year, m)
            subj_time_collection = subj_collection.get_articles_time(args.year, m)
            subj_time_collection.assign_subject(args.subject)
            logger.info("Time-year Size: {}".format( subj_time_collection.get_size()))
            total_data += subj_time_collection.get_size()
            save_pkl(subj_time_collection, output_folder, name)
            #subj_time_collection.export_parquet(output_folder, name)

    else:
        ## Todo this later
        name = "{}_{}".format(args.year, args.month)

    logger.info("Total size of data: {}".format(total_data))
