#-*- coding:utf8 -*-
# author: nichijouYC

from segment import Segmentation
from postag import PosTagging
from semanticclassify import SemanticClassification
from string_classify_extracctor import StringClassifyExtractor

segmentation = Segmentation()
postag = PosTagging()
semanticclassify = SemanticClassification()
string_ectractor = StringClassifyExtractor()


def process(word):
    result = []
    substring = string_ectractor.getSubstringAllType(word)
    for s in substring:
        if s[1] == 'num':
            result.append((s[0], ' ', 'number'))
        if s[1] == 'char':
            seg = segmentation.getBestSegment(s[0])[0]
            tagged_seg = postag.posTagging(seg)
            semantic_seg = semanticclassify.semanticClassify(tagged_seg)
            result = result + semantic_seg
        if s[1] == 'spe':
            result.append((s[0], ' ', 'special'))
    return result
if __name__ == '__main__':
    print process('@iloveyou123')
