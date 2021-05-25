# NLP-negation-handling-and-data-augmentation-techniques

For specific NLP tasks, like emotion mining, the semantic context of sentences plays a vital role. Removing negation words like no, not, never etc. can totally change the meaning of a sentence, thus such words have to be excluded from the stopwords list. Our goal is to find a way to capture the context of a negation, into a single term.

A script is provided to, firstly, perform POS tag in order to identify the adjectives and verbs. Afterwards, the bigrams of each sentence are checked and whenever a negating word is identified, if the following word is an adjective or a verb, it is substituted by its antonym and the negation word is removed. The reason why the focus is only on adjectives and verbs is that the negation of these terms can affect the context of a sentence.  

An example of this approach is the following; given the sentence "The weather today is not bad", the script locates the word "not", then checks the next word's POS tag, which is adjective, and substitutes it by its antonym. This results in the following sentence; "The weather today is good".

The second script, data agumentation is performed by substituting the synonyms of words. This technique can be used to populate datasets, or balance the classes of an imbalanced dataset.
