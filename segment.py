# -*- coding:utf-8 -*-
# author:nichijouYC

from __future__ import division
from nltk.corpus import brown
from nltk.corpus import names

import nltk

class Segmentation:

    def __init__(self):
        pass

    source_corpus_all_words = brown.words()
    source_corpus_unique_words = set(source_corpus_all_words)

    onechar_word = ['a', 'I', 'i']
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

    month = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september',
             'october', 'november', 'december']

    """
    dict源语料库用于生成候选分段(修剪)
    """
    source_corpus_trim = onechar_word + twochar_word + threechar_word + [
        word for word in source_corpus_unique_words if len(word) > 3] + male_name + female_name + month

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

    def getAllSegment(self,s):
        """
        给出s所有可能分段情况
        Input: 'anyone'
        Output: [['any','one'],['anyone']]
        """
        candidates = self.wordBreak(s)
        result = [nltk.word_tokenize(w) for w in candidates]
        return result

    def getBestSegment(self,s):
        """
        给出s最佳分段
        Input: 'anyone'
        Output: [['anyone']]
        """
        candidates = self.wordBreak(s)
        result = []
        if len(candidates) > 1:
            result = [nltk.word_tokenize((self.chooseBest(candidates))[0])]
        else:
            result = [nltk.word_tokenize(candidates[0])]
        return result

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

if __name__ == '__main__':
    segmentation = Segmentation()
    print segmentation.getAllSegment('helloworld')
    print segmentation.getAllSegment('anyone')
    print segmentation.getBestSegment('helloworld')
    print segmentation.getBestSegment('anyone')
