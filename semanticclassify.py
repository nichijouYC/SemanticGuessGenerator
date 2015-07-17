# -*- coding:utf-8 -*-
# author:nichijouYC

from nltk.corpus import names
from nltk.corpus import wordnet as wn
import nltk

class SemanticClassification:

    def __init__(self):
        pass

    def semanticClassify(self, s):
        """
        对分段进行语义分类，仅动词和名词具有语义标签，需要先进行POS标记
        Input: [('i', 'PRON'), ('love', 'VERB'), ('you', 'PRON')]
        Output: [('i', 'PRON', ' '), ('love', 'VERB', 'love.n.01'), ('you', 'PRON', ' ')]
        """
        classified_seg = []
        for seg in s:

            male_name = [w.lower() for w in names.words('male.txt')]
            female_name = [w.lower() for w in names.words('female.txt')]

            month = ['january', 'february', 'march', 'april', 'may', 'june',
                     'july', 'august', 'september', 'october', 'november', 'december']

            if seg[1] == 'NP':
                if seg[0] in male_name:
                    classified_seg.append((seg[0], seg[1], 'male_name'))
                elif seg[0] in female_name:
                    classified_seg.append((seg[0], seg[1], 'female_name'))
                elif seg[0] in month:
                    classified_seg.append((seg[0], seg[1], 'month'))
                else:
                    classified_seg.append((seg[0], seg[1], ' '))
            elif (seg[1] == 'VERB' or seg[1] == 'NOUN'):
                classified = wn.synsets(seg[0])
                if len(classified) > 0:
                    classified_seg.append(
                        (seg[0], seg[1], classified[0].name()))
                else:
                    classified_seg.append((seg[0], seg[1], ' '))
            else:
                classified_seg.append((seg[0], seg[1], ' '))
        return self.encodeutf8(classified_seg)

    def encodeutf8(self,s):
        result = []
        for w in s:
            if isinstance(w[2], unicode):
                encoded_result = (w[0],w[1],w[2].encode('utf8'))
                result.append(encoded_result)
            else:
                result.append(w)
        return result

if __name__ == '__main__':
    semantic = SemanticClassification()
    seg = [('i', 'PRON'), ('love', 'VERB'), ('you', 'PRON')]
    print semantic.semanticClassify(seg)
