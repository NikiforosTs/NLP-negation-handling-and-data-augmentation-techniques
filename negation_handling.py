import re, string
import spacy
nlp = spacy.load("en_core_web_sm")

import nltk
from nltk.corpus import stopwords, wordnet
nltk.download(["stopwords", "vader_lexicon", "punkt", "wordnet", "averaged_perceptron_tagger"])




# customising stop words list to remove negation tokens

stopwords = nltk.corpus.stopwords.words("english")
non_stopwords = ['not','no','never','none','nor','hadn','mustn',"didn't",'doesn',"hadn't","mustn't",
                 'mightn','haven',"aren't","haven't",'weren','didn',"couldn't","doesn't","hasn't",'isn',
                 'wasn','needn','mustn',"weren't",'don','couldn','wouldn',"mightn't","wouldn't","don't",
                 'ain',"shouldn't",'aren',"isn't","needn't","wasn't",'shouldn','hasn',"won't"]
my_stopwords = set([word for word in stopwords if word not in non_stopwords])

print("Total number of stopwords is:" + " " + str(len(my_stopwords)))


def negation_handling(unigram):
    antonyms = []

    # if word after "not" is adjective or verb
    if nlp(unigram)[0].pos_ in ['ADJ', 'VERB']:

        # find antonyms
        for syn in wordnet.synsets(unigram):
            for l in syn.lemmas():
                if l.antonyms():
                    antonyms.append(l.antonyms()[0].name())

    # keep unique antonyms
    antonyms = set(antonyms)

    # return first adjective antonym
    for antonym in antonyms:
        # Since we want to avoid substituting for example a verb with an
        # adjective, the POS tagging must be the same
        if nlp(antonym)[0].pos_ == nlp(unigram)[0].pos_:
            return antonym

    # if no adj antonym found, return original word
    return unigram


# In this case, negation handling is performed by checking the bi-grams and substituting negative bi-grams with their antonyms

def preprocessing(sentence):
    # convert to lowercase
    sentence = sentence.lower()

    # remove punctuation
    nopunc = [char for char in sentence if char not in string.punctuation]
    sentence = ''.join(nopunc)

    # remove stopwords
    sentence = ' '.join([word for word in sentence.split() if word not in my_stopwords])

    # lemmatization
    doc = nlp(sentence)
    sentence = [token.lemma_ if ('PRON' not in token.lemma_) & (len(token.lemma_) > 2) else '' for token in doc]

    # remove empty tokens
    sentence = list(filter(('').__ne__, sentence))

    # negation handling
    antonyms = {}
    for idx, (first, second) in enumerate(zip(sentence, sentence[1:])):
        if first in non_stopwords:
            antonyms[idx - len(antonyms.keys())] = negation_handling(second)

    for key in antonyms.keys():
        sentence[key] = antonyms[key]
        sentence.pop(key + 1)

    return ' '.join([word for word in sentence])

# An example of how this function operates. Of course, the result is imposed to lemmatization and the other preprocessing steps
# but still, it can be seen that 'not' is removed and 'good' is substituted by 'bad'.
sentence1 = "The weather today is not good"

preprocessing(sentence1)