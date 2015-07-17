# -*- coding:utf-8 -*-
# author:nichijouYC

from nltk.corpus import brown
from nltk.corpus import names

import nltk

class PosTagging:

    def __init__(self):
        pass

    def posTagging(self, s):
        """
        对一个分段进行POS标记
        input: ['i','love','you']
        output: [('i', 'PRON'), ('love', 'VERB'), ('you', 'PRON')]
        """
        brown_tagged_sents = brown.tagged_sents(
            tagset='universal', categories='news')

        default_tagger = nltk.DefaultTagger('NN')

        month = [u'january', u'february', u'march', u'april', u'may', u'june',
                 u'july', u'august', u'september', u'october', u'november', u'december']

        np_words = [w.lower() for w in names.words()] + month
        np_tags = dict((word, 'NP') for word in np_words)
        np_tagger = nltk.UnigramTagger(
            model=np_tags, backoff=default_tagger)

        brown_unigram_tagger = nltk.UnigramTagger(
            brown_tagged_sents, backoff=np_tagger)
        brown_bigram_tagger = nltk.BigramTagger(
            brown_tagged_sents, backoff=brown_unigram_tagger)
        brown_trigram_tagger = nltk.TrigramTagger(
            brown_tagged_sents, backoff=brown_bigram_tagger)

        patterns = [(r'\bi\b', 'PRON')]
        regexp_tagger = nltk.RegexpTagger(
            patterns, backoff=brown_trigram_tagger)

        result = regexp_tagger.tag(s)
        return self.encodeutf8(result)

    def encodeutf8(self,s):
        result = []
        for w in s:
            if isinstance(w[1], unicode):
                encoded_result = (w[0],w[1].encode('utf8'))
                result.append(encoded_result)
            else:
                result.append(w)
        return result

if __name__ == '__main__':
    postag = PosTagging()
    print postag.posTagging(['i','love','you'])
    print postag.posTagging(['go'])
