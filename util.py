## This file contain useful utility functions

import pickle
import spacy
import re
from pathlib import Path
import re


def year_checker(collection, year):
    """
    check the correctness of get_article_date() method

    Args:
        collection: (ArticleCollection)
        year: (int)
    """

    months = [12]
    total = 0
    for m in months:
        coll = collection.get_articles_date(year, m)
        total += coll.get_size()

    print(total, collection.get_size())


def tokenize(text, nlp, min_words=1):
    """
    code from: https://github.com/Weixin-Liang/Mapping-the-Increasing-Use-of-LLMs-in-Scientific-Papers

    Processes the input text, splits it into sentences, and further processes each sentence
    to extract non-numeric words. It constructs a list of these words for each sentence.

    Args:
        text: (str) A string containing multiple sentences.
        nlp: (spacy.lang.en.English)
        min_words: (int) minimum number of words needed in a sentence

    Returns:
    list: A list of lists, where each inner list contains the words from one sentence,
          excluding any numeric strings.
    """
    # remove newline characters, this line is not necessary for all cases
    # the reason it is included here is because the abstracts in the dataset contain abnormal newline characters
    # e.g. Recent works on diffusion models have demonstrated a strong capability for\nconditioning image generation,
    text = text.replace('\n',' ')
    # Initialize an empty list to store the list of words for each sentence
    sentence_list=[]
    # Process the sentence using the spacy model to extract linguistic features and split into components
    doc=nlp(text)
    # Iterate over each sentence in the processed text
    for sent in doc.sents:
        # Extract the words from the sentence
        if len(sent) > min_words:
            words = re.findall(r'\b\w+\b', sent.text.lower())
            # Remove any words that are numeric
            words_without_digits=[word for word in words if not word.isdigit()]
            # If the list is not empty, append the list of words to the sentence_list
            if len(words_without_digits)!=0:
                sentence_list.append(words_without_digits)
    return sentence_list


def get_year_month(input_str):
    """
    returns the year and month
    Args:
        input_str: (str) the input string

    Returns: (int, int) year, month
    """
    parts = input_str.split('_')
    year = int(parts[0])
    month = int(parts[1].split('.')[0])

    return year, month

def save_pkl(obj, folder, name):
    """
    save the object as a pkl file
    Args:
        obj: (object)
        folder: (str) path to the folder
        name: (str) name of the fole
    """

    path = Path(folder)
    path.mkdir(parents=True, exist_ok=True)
    if ".pkl" not in name:
        name = "{}.pkl".format(name)
    full = path / name
    with open(full, "wb") as handle:
        pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)

def FleschReadabilityEase(text):
    """
    Calculate the Flesch Reading Ease score
    Args:
        text (str): input text 
    
    Returns:
        (float): the Flesch Reading Ease score
    """

    if len(text) > 0:
        return 206.835 - (1.015 * len(text.split()) / len(text.split('.'))) - 84.6 * (sum(list(
            map(lambda x: 1 if x in ["a", "i", "e", "o", "u", "y", "A", "E", "I", "O", "U", "y"] else 0, text))) / len(
            text.split()))
    return 0.0


def ARI(text):
    """
    Calculate the Automated Readability Index (ARI) score
    Args:
        text (str): the input text 
    Returns:
        (float): the ARI score
    """

    score = 0.0
    if len(text) > 0:
        score = 4.71 * (len(text) / len(text.split())) + 0.5 * (len(text.split()) / len(text.split('.'))) - 21.43
        return score if score > 0 else 0.0
    
    return 0.0



def FleschKincaidTest(text):
    """
    Calculate the Flesch-Kincaid Grade Level score

    Args:
        text (str): the input text
    Returns:
        (float): the Flesch-Kincaid Grade Level score
    """

    score = 0.0
    if len(text) > 0:
        score = (0.39 * len(text.split()) / len(text.split('.'))) + 11.8 * (sum(list(
            map(lambda x: 1 if x in ["a", "i", "e", "o", "u", "y", "A", "E", "I", "O", "U", "y"] else 0, text))) / len(
            text.split())) - 15.59
        return score if score > 0 else 0
    
    return 0.0


def coleman_liau_index(text):
    """
    Calculate the Coleman-Liau index
    Args:
        text (str): the input text
    Returns:
        (float): the Coleman-Liau index score
    """


    # Count letters (ignoring non-letter characters)
    letters = sum(c.isalpha() for c in text)

    # Count words by splitting text on whitespace
    words = len(text.split())

    # Count sentences using regex to consider '.', '!', '?' as end of sentences
    sentences = len(re.split(r'[.!?]+', text)) - 1  # subtract one for the last split

    # Calculate the average number of letters and sentences per 100 words
    if words == 0:
        average_letters_per_100_words = 0
        average_sentences_per_100_words = 0
    else:
        average_letters_per_100_words = (letters / words) * 100
        average_sentences_per_100_words = (sentences / words) * 100

    # Coleman-Liau index calculation
    cli = (0.0588 * average_letters_per_100_words) - (0.296 * average_sentences_per_100_words) - 15.8

    return cli