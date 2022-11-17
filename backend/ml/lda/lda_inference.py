import re
from string import punctuation
from typing import List, Tuple

import nltk
from gensim import corpora, models
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from ml.lda.config import LDA_MODEL_PATH, LDA_DICTIONARY_PATH, NLTK_PATH, id2topic
nltk.data.path = [str(NLTK_PATH)]


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


class LDAModel:
    def __init__(self):
        self.english_stopwords = stopwords.words("english")
        self.lemmatizer = WordNetLemmatizer()
        self.model = models.LdaModel.load(LDA_MODEL_PATH)
        self.dictionary = corpora.Dictionary.load(LDA_DICTIONARY_PATH)

    def preprocess(self, data):
        data = map(lambda x: x.lower(), data)
        data = map(lambda x: remove_punct(x), data)
        data = map(lambda x: re.sub(r'\d+', ' ', x), data)

        data = map(lambda x: x.split(' '), data)
        data = map(lambda x: [token for token in x if token not in self.english_stopwords], data)
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
                    lemmatized_sentence.append(self.lemmatizer.lemmatize(word, tag))
            lemmatized_sentence = " ".join(lemmatized_sentence)

            result.append(lemmatized_sentence)

        return result

    def inference(self, abstracts: List[str], return_probs=False) -> List[Tuple[int, float]]:
        papers = self.preprocess(abstracts)

        list_of_list_of_tokens = list(map(lambda x: x.split(' '), papers))

        for i in range(len(list_of_list_of_tokens)):
            list_of_list_of_tokens[i] = list(filter(lambda x: len(x) > 3, list_of_list_of_tokens[i]))

        corpus = [self.dictionary.doc2bow(list_of_tokens) for list_of_tokens in list_of_list_of_tokens]

        inference_result = self.model[corpus]

        if return_probs:
            result = [(id2topic[topic[0][0]], float(topic[0][1])) for topic in inference_result]
        else:
            result = [id2topic[topic[0][0]] for topic in inference_result]

        return result
