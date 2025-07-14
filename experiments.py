## This file contains the main script to run the experiment for estimating the fraction of AI-generated text in articles.

from src.estimation import estimate_text_distribution
from src.MLE import MLE
import os
import pandas as pd
import json
from util import *
import numpy as np

from log import setup_logger


if __name__ == "__main__":
    logger = setup_logger("my_logger", "experiment.log")
    name = "ojs_ed"
    ai_data_21 = pd.read_parquet(f"data/training_data/{name}/ai_data_21.parquet")
    #logger.info(f"ai_data_21: {ai_data_21.shape[0]} sentences")
    human_data_21 = pd.read_parquet(f"data/training_data/{name}/human_data_21.parquet")
    #logger.info(f"human_data_21: {human_data_21.shape[0]} sentences")
    estimate_text_distribution(f"data/training_data/{name}/human_data_21.parquet",
                               f"data/training_data/{name}/ai_data_21.parquet",
                               f"distribution/{name}.parquet")

    model= MLE(f"distribution/{name}.parquet")
    for alpha in [0,0.025,0.05,0.075,0.1,0.125,0.15,0.175,0.2,0.225,0.25]:
        estimated,ci=model.inference(f"data/validation_data/{name}/ground_truth_alpha_{alpha}.parquet",
                                     ground_truth=alpha, save=True)
        error=abs(estimated-alpha)
        logger.info(f"{'Ground Truth':>10},{'Prediction':>10},{'CI':>10},{'Error':>10}")
        logger.info(f"{alpha:10.3f},{estimated:10.3f},{ci:10.3f},{error:10.3f}")
