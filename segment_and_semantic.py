# -*- coding:utf-8 -*-

from __future__ import division
from nltk.corpus import brown
from nltk.corpus import names
from nltk.corpus import wordnet as wn


import nltk
import re
import pickle


class Segmentation:

    """
    dict源语料库用于生成候选分段(修剪)
    """
    source_corpus_all_words = brown.words()
    source_corpus_unique_words = set(source_corpus_all_words)

    onechar_word = [u'a', u'I', u'i']
    twochar_word_freq = nltk.FreqDist(
        [word for word in source_corpus_all_words if len(word) == 2])
    twochar_word_list = list(twochar_word_freq.items())
    twochar_word_list.sort(key=lambda x: x[1], reverse=True)
    twochar_word = [word[0]
                    for word in twochar_word_list[:int(
                        len(twochar_word_list) * 0.37)]]
    threechar_word_freq = nltk.FreqDist(
        [word for word in source_corpus_all_words if len(word) == 3])
    threechar_word_list = list(threechar_word_freq.items())
    threechar_word = [word[0]
                      for word in threechar_word_list if word[1] > 100]

    male_name = names.words('male.txt')
    male_name = [w.lower() for w in male_name]
    female_name = names.words('female.txt')
    female_name = [w.lower() for w in female_name]

    f_read_city = open('C:\\nltk_data\\my_corpora\\city.txt', 'r')
    city = f_read_city.read().split(' ')
    f_read_city.close()

    month = [u'january', u'february', u'march', u'april', u'may', u'june', u'july', u'august', u'september',
             u'october', u'november', u'december']

    source_corpus_trim = onechar_word + twochar_word + threechar_word + [
        word for word in source_corpus_unique_words if len(word) > 3] + male_name + female_name + month + city

    dict = source_corpus_trim

    """
    reference_corpus参考语料库用于选出最佳分段
    """
    # reference_corpus = source_corpus_all_words
    reference_corpus = source_corpus_trim
    reference_corpus_unigram = reference_corpus
    reference_corpus_unigram_num = len(reference_corpus_unigram)
    reference_corpus_bigram = list(nltk.ngrams(reference_corpus, 2))
    reference_corpus_bigram_num = len(reference_corpus_bigram)
    reference_corpus_trigram = list(nltk.ngrams(reference_corpus, 3))
    reference_corpus_trigram_num = len(reference_corpus_trigram)

    def segment(self, s):
        candidates = self.wordBreak(s)
        if len(candidates) > 1:
            return self.chooseBest(candidates)
        else:
            return candidates

    def wordBreak(self, s):
        """
        选出所有可能分段情况
        """
        n = len(s)
        dp = [[False for j in xrange(n)] for i in xrange(n)]
        for i in xrange(n):
            for j in xrange(n - i):
                if s[i:i + j + 1] in self.dict:
                    dp[i][i + j] = True

        for i in xrange(n):
            if dp[i][n - 1]:
                ans = []
                self.dfs(0, n, [], s, dp, ans)
                if ans == []:
                    return [s]
                else:
                    return ans

        return [s]

    def dfs(self, cur, n, path, s, dp, ans):
        if cur == n:
            ans.append(''.join(path))
            return

        for i in xrange(n):
            if dp[cur][i]:
                if path:
                    self.dfs(
                        i + 1, n, path + [' '] + [s[cur:i + 1]], s, dp, ans)
                else:
                    self.dfs(i + 1, n, path + [s[cur:i + 1]], s, dp, ans)

    def chooseBest(self, candidates):
        """
        选出一个最佳分段（分数最高）
        """
        score_seg = [(self.ngramScore(nltk.word_tokenize(seg)), seg)
                     for seg in candidates]

        print score_seg
        score_seg.sort(key=lambda x: x[0], reverse=True)
        return [score_seg[0][1]]

    def ngramScore(self, seg):
        """
        为一个分段计算ngram分数
        """
        score = 0
        l = len(seg)
        if l == 1:
            score = self.reference_corpus_unigram.count(
                seg[0]) / self.reference_corpus_unigram_num
        elif l == 2:
            score = self.reference_corpus_bigram.count(
                tuple(seg)) / self.reference_corpus_bigram_num
        elif l == 3:
            score = self.reference_corpus_trigram.count(
                tuple(seg)) / self.reference_corpus_trigram_num

        if score == 0:
            for i in (1, 3):
                if i < l:
                    a = self.ngramScore(seg[:i])
                    b = self.ngramScore(seg[i:])
                    tempScore = a * b
                    if tempScore > score:
                        score = tempScore
        return score


class PosTagging:


    def posTagging(self, s):
        """
        对一个分段进行POS标记
        """
        brown_tagged_sents = brown.tagged_sents(tagset='universal')

        default_tagger = nltk.DefaultTagger('NN')

        f_read_city = open('C:\\nltk_data\\my_corpora\\city.txt', 'r')
        city = f_read_city.read().split(' ')
        f_read_city.close()

        month = [u'january', u'february', u'march', u'april', u'may', u'june',
             u'july', u'august', u'september', u'october', u'november', u'december']

        np_words = [w.lower() for w in names.words()] + month + city
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

        return regexp_tagger.tag(nltk.word_tokenize(s))


class SemanticClassification:


    def semanticClassify(self, s):
        """
        对一个分段进行语义分类
        """
        classified_seg = []
        for seg in s:

            male_name = [w.lower() for w in names.words('male.txt')]
            female_name = [w.lower() for w in names.words('female.txt')]

            f_read_city = open('C:\\nltk_data\\my_corpora\\city.txt', 'r')
            city = f_read_city.read().split(' ')
            f_read_city.close()

            month = [u'january', u'february', u'march', u'april', u'may', u'june',
                 u'july', u'august', u'september', u'october', u'november', u'december']

            if seg[1] == 'NP':
                if seg[0] in male_name:
                    classified_seg.append((seg[0], seg[1], 'male_name'))
                elif seg[0] in female_name:
                    classified_seg.append((seg[0], seg[1], 'female_name'))
                elif seg[0] in month:
                    classified_seg.append((seg[0], seg[1], 'month'))
                elif seg[0] in city:
                    classified_seg.append((seg[0], seg[1], 'city'))
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
        return classified_seg


class SegandSemanticClassify:

    def segandSemanticClassify(self, password):

        result = []

        segmentation = Segmentation()
        seg = segmentation.segment(password)
        print seg

        postagging = PosTagging()
        pos = postagging.posTagging(seg[0])
        print pos

        semanticclassification = SemanticClassification()
        semantic_classify = semanticclassification.semanticClassify(pos)
        print semantic_classify

        return semantic_classify

    def classify(self, password):

        charre = re.search('[a-zA-Z]', password)
        numre = re.search('[0-9]', password)
        specialre = re.search('[^\w]', password)

        if charre:
            if numre:
                if specialre:
                    # mix
                    print 'mix'
                    newresult = []
                    spe = re.split('[\w]', password)
                    char = re.split('[0-9]|[^\w]', password)
                    num = re.split('[a-zA-Z]|[^\w]', password)
                    while '' in spe:
                        spe.remove('')
                    while '' in char:
                        char.remove('')
                    while '' in num:
                        num.remove('')
                    print spe
                    print char
                    print num
                    temp = [(w, password.index(w)) for w in num + char + spe]
                    temp.sort(key=lambda x: x[1])
                    temp = [w[0] for w in temp]
                    print temp
                    for w in temp:
                        if w.isdigit():
                            newresult.append((w, ' ', 'number'))
                        elif w.isalpha():
                            newresult = newresult + \
                                self.segandSemanticClassify(w)
                        else:
                            newresult.append((w, ' ', 'special'))
                    return newresult
                else:
                    # num+char
                    print 'num+char'
                    newresult = []
                    num = re.split('[a-zA-Z]', password)
                    char = re.split('[0-9]', password)
                    while '' in num:
                        num.remove('')
                    while '' in char:
                        char.remove('')
                    temp = [(w, password.index(w)) for w in num + char]
                    temp.sort(key=lambda x: x[1])
                    temp = [w[0] for w in temp]
                    for w in temp:
                        if w.isdigit():
                            newresult.append((w, ' ', 'number'))
                        if w.isalpha():
                            newresult = newresult + \
                                self.segandSemanticClassify(w)

                    return newresult
            else:
                if specialre:
                    # char+spe
                    print 'char+spe'
                    newresult = []
                    spe = re.split('[a-zA-Z]', password)
                    char = re.split('[^\w]', password)
                    while '' in spe:
                        spe.remove('')
                    while '' in char:
                        char.remove('')
                    print spe
                    print char
                    print spe + char
                    temp = [(w, password.index(w)) for w in spe + char]
                    temp.sort(key=lambda x: x[1])
                    temp = [w[0] for w in temp]
                    print temp
                    for w in temp:
                        if w.isalpha():
                            newresult = newresult + \
                                self.segandSemanticClassify(w)
                        else:
                            newresult.append((w, ' ', 'specail'))
                    return newresult
                else:
                    # char
                    return self.segandSemanticClassify(password)
        else:
            if specialre:
                if numre:
                    #'num+spe'
                    return [(password, ' ', 'num+specail')]
                else:
                    # spe
                    return [(password, ' ', 'special')]
            else:
                # num
                return [(password, ' ', 'number')]

process = SegandSemanticClassify()

print process.classify('anyone')

# f_read = open('C:\\nltk_data\\my_corpora\\rockyou_without_num_1000.txt')
# content = f_read.read()
# f_read.close()
# content = content.split('\n')

# word = content[0:1000]
# word = [w.lower() for w in word]
# wordlist = [process.classify(w) for w in word]

# with open('E:\\bishe\\FYC_bishe\\result\\seg_result_0_1000_reference_corpus.txt', 'wb') as f_write:
#     pickle.dump(wordlist, f_write)
