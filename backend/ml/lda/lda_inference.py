import os

import nltk
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from string import punctuation
from gensim import corpora, models
from ml.lda.config import MODEL_PATH, DICTIONARY_PATH, id2topic
from typing import List, Tuple
import re

english_stopwords = stopwords.words("english")
lemmatizer = WordNetLemmatizer()


def pos_tagger(nltk_tag):
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


def remove_punct(text):
    table = {
        33: ' ', 34: ' ', 35: ' ', 36: ' ', 37: ' ', 38: ' ', 39: ' ', 40: ' ',
        41: ' ', 42: ' ', 43: ' ', 44: ' ', 45: ' ', 46: ' ', 47: ' ', 58: ' ', 59: ' ',
        60: ' ', 61: ' ', 62: ' ', 63: ' ', 64: ' ', 91: ' ', 92: ' ', 93: ' ', 94: ' ',
        95: ' ', 96: ' ', 123: ' ', 124: ' ', 125: ' ', 126: ' '
    }
    return text.translate(table)


def preprocess(data):
    data = map(lambda x: x.lower(), data)
    data = map(lambda x: remove_punct(x), data)
    data = map(lambda x: re.sub(r'\d+', ' ', x), data)

    data = map(lambda x: x.split(' '), data)
    data = map(lambda x: [token for token in x if token not in english_stopwords], data)
    data = map(lambda x: [token for token in x if token != " " and token.strip() not in punctuation], data)

    data = map(lambda x: ' '.join(x), data)

    data = list(data)

    result = []
    for every in data:
        pos_tagged = nltk.pos_tag(nltk.word_tokenize(every))
        wordnet_tagged = list(map(lambda x: (x[0], pos_tagger(x[1])), pos_tagged))

        lemmatized_sentence = []
        for word, tag in wordnet_tagged:
            if tag is None:
                lemmatized_sentence.append(word)
            else:
                lemmatized_sentence.append(lemmatizer.lemmatize(word, tag))
        lemmatized_sentence = " ".join(lemmatized_sentence)

        result.append(lemmatized_sentence)

    return result


print(MODEL_PATH)
print(os.system(f'ls -al {MODEL_PATH}'))
print(os.system(f'md5sum {MODEL_PATH}'))
model = models.LdaModel.load(MODEL_PATH)
dictionary = corpora.Dictionary.load(DICTIONARY_PATH)


def inference(abstracts: List[str], return_probs=False) -> List[Tuple[int, float]]:
    papers = preprocess(abstracts)

    list_of_list_of_tokens = list(map(lambda x: x.split(' '), papers))

    for i in range(len(list_of_list_of_tokens)):
        list_of_list_of_tokens[i] = list(filter(lambda x: len(x) > 3, list_of_list_of_tokens[i]))

    corpus = [dictionary.doc2bow(list_of_tokens) for list_of_tokens in list_of_list_of_tokens]

    inference_result = model[corpus]

    if return_probs:
        result = [(id2topic[topic[0][0]], float(topic[0][1])) for topic in inference_result]
    else:
        result = [id2topic[topic[0][0]] for topic in inference_result]

    return result
