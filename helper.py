## This file contains the functions to convert information from raw json file to
## an article object. The filters are based on the notebook preprocessing.ipynb

from base import Article, ArticleCollection
from tqdm import tqdm
import datetime
from util import tokenize
import spacy
from log import setup_logger
from spacy.cli import download


def check_date_validity(date):
    """
    Check if the date is valid

    Args:
        date: (str)
    Returns:
        (bool)
    """

    if date is None:
        return False
    else:
        try:
            month = datetime.datetime.strptime(date, "%Y-%m-%d").month
            year = datetime.datetime.strptime(date, "%Y-%m-%d").year
            return True
        except ValueError:
            return False

def check_length_validity(text, nlp, min_val=31, max_val=533):
    """
    Checks if the text length is within the min and max_val

    Args:
        text: (str)
        nlp: () the spacy model
        min_val: (int)
        max_val: (int)

    Returns:
        (bool)
    """

    if text is None:
        return False
    else:
        length = len(tokenize(text, nlp))
        if length <= max_val and length >= min_val:
            return True
        else:
            return False

def check_score(score, cutoff=0.9):
    """
    Check if the score is bigger or smaller than the cutoff

    Args:
        cutoff: (float)
        score: (float)

    Returns:
        (bool)
    """
    if score is None:
        return False
    else:
        if score > cutoff:
            return True
        else:
            return False

def convert_raw_json(json_orig, collect_translated=False):
    """
    Create an Article Collection from the raw json file

    Args:
        json_orig: (dict) the orgininal json file
        collect_translated: (bool)

    Returns:
        (ArticleCollection)
    """
    try:
        nlp = spacy.load("en_core_web_lg")
    except OSError:
        print("Downloading model")
        download("en_core_web_lg")
        nlp = spacy.load("en_core_web_lg")

    collection = ArticleCollection("all")
    total_discarded = 0
    total_valid = 0
    logger = setup_logger("my_logger", "helper.log")
    for key in tqdm(json_orig):
        for i in range(len(json_orig[key])):
            article = Article(json_orig[key][i], key)

            # check the validity of the date
            date_valid = check_date_validity(article.date)

            # check if the article is translated
            is_not_translated = False
            if article.translated is not None:
                if article.translated is not True:
                    is_not_translated= True
                else:
                    continue

            # check if the length is within the desired length
            #is_valid_length = check_length_validity(article.description, nlp)

            # check for classifier score
            is_high_score = check_score(article.subject_score)

            # check for language
            is_eng = True if article.language == "eng" else False

            # check for description:
            include_desc = True if article.description is not None else False
            if is_high_score and is_not_translated and date_valid and include_desc and is_eng:
                collection.add_article(article)
                total_valid += 1
            else:
                total_discarded += 1
    logger.info("Total valid articles: {}, total discarded: {}".format(
        total_valid, total_discarded))

    return collection
