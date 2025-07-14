## This file contains functions that is used to estimate alpha, the fraction of article written using ChatGPT.
## It uses the MLE class to perform the estimation based on the provided inference data and distribution path.

from src.estimation import estimate_text_distribution
from src.MLE import MLE

def estimate_alpha(inference_data_path, dist_path):
    """
    estimates alpha: the fraction of article written using ChatGPT
    Args:
        inference_data_path: (str) the location of the parquet file containing the tokenized
                             sentences of inference data
        dist_path: (str) location of the parquet file containing the distribution of words

    Returns:
        (float) alpha, (ci) the assoicated confidence interval

    """

    model = MLE(dist_path)
    estimated, ci = model.inference(inference_data_path)

    return estimated, ci





