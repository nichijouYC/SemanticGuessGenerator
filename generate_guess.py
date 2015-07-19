# -*- coding:utf-8 -*-
# author: nichijiuYC

from __future__ import division
import random
from pprint import pprint
from segment_pos_semanticclassify import process

def generateStructure(wordlist):
    """
    生成基础结构和句法结构
    Input: 经过segment_pos_semanticclassify.process处理后的单词列表
    Output: base_structure and syntactic_structure
    """
    """
    param
    [[('i', 'PRON', ' '),('love', 'VERB', 'love.n.01'),('you', 'PRON', ' '),('2', ' ', 'number')],
     [('i', 'PRON', ' '),('hated', 'NN', ' '),('them', 'PRON', ' '),('3', ' ', 'number')],
     [('football', 'NOUN', 'football.n.01'), ('3', ' ', 'number')]]
    base_structure
    [('i', 'PRON'), ('love', 'love.n.01.VERB'), ('you', u'PRON'), ('2', 'number'), ('i', 'PRON'),
     ('hated', 'NN'), ('them', 'PRON'), ('3', 'number'), ('football', 'football.n.01.NOUN'),
     ('3', 'number')]
    syntactic_structure
    [[PRON][love.n.01.VERB][PRON][number], [PRON][NN][PRON][number], [football.n.01.NOUN][number]]
    """
    base_structure = []
    syntactic_structure = []
    for word in wordlist:

        word_base_structure = []
        word_syntactic_structure = ''

        for seg in word:
            if seg[2] == ' ':
                word_base_structure = word_base_structure + [(seg[0], seg[1])]
                word_syntactic_structure = word_syntactic_structure + \
                    '[' + seg[1] + ']'
            elif (seg[1] == ' ') | (seg[1] == 'NP'):
                word_base_structure = word_base_structure + [(seg[0], seg[2])]
                word_syntactic_structure = word_syntactic_structure + \
                    '[' + seg[2] + ']'
            else:
                word_base_structure = word_base_structure + \
                    [(seg[0], seg[2] + '.' + seg[1])]
                word_syntactic_structure = word_syntactic_structure + \
                    '[' + seg[2] + '.' + seg[1] + ']'

        base_structure = base_structure + word_base_structure
        syntactic_structure = syntactic_structure + [word_syntactic_structure]

    return base_structure, syntactic_structure

def generateWordRules(syntactic_structure):
    """
    生成词规则
    """
    word_rules = []
    syntactic_structure_set = list(set(syntactic_structure))
    for i in xrange(0, len(syntactic_structure_set)):
        probability = syntactic_structure.count(
            syntactic_structure_set[i]) / len(syntactic_structure)
        rules = [
            ('N1', '->', syntactic_structure_set[i], "%.4f" % (probability))]
        word_rules = word_rules + rules
    return word_rules


def generateSegRules(base_structure):
    """
    生成片段规则
    """
    seg_rules = []
    semantic_structure = [w[1] for w in base_structure]
    semantic_structure_set = list(set(semantic_structure))
    for i in xrange(0, len(semantic_structure_set)):
        semantic = semantic_structure_set[i]
        seg = [w[0] for w in base_structure if w[1] == semantic]
        seg_set = list(set(seg))
        for segment in seg_set:
            probability = seg.count(segment) / len(seg)
            seg_rules = seg_rules + \
                [('[' + semantic + ']', '->', segment, '%.4f' % (probability))]
    return seg_rules


def generateRules(wordlist):
    """
    生成单词列表的所有规则（词规则+片段规则）
    Input：经过segment_pos_semanticclassify.process处理后的单词列表
    Outout：word_rules + seg_rules
    """
    """
    param
    [[('i', 'PRON', ' '),('love', 'VERB', 'love.n.01'),('you', 'PRON', ' '),('2', ' ', 'number')],
     [('i', 'PRON', ' '),('hated', 'NN', ' '),('them', 'PRON', ' '),('3', ' ', 'number')],
     [('football', 'NOUN', 'football.n.01'), ('3', ' ', 'number')]]
    rules
    [('N1', '->', '[football.n.01.NOUN][number]', '0.33'),
     ('N1', '->', '[PRON][love.n.01.VERB][PRON][number]', '0.33'),
     ('N1', '->', '[PRON][hate.v.01.VERB][PRON][number]', '0.33'),
     ('[NN]', '->', 'hated', '1.00'),
     ('[PRON]', '->', 'i', '0.50'), ('[PRON]', '->', 'you', '0.25'),
     ('[PRON]', '->', 'them', '0.25'), ('[football.n.01.NOUN]', '->', 'football', '1.00'),
     ('[number]', '->', '3', '0.67'), ('[number]', '->', '2', '0.33'),
     ('[love.n.01.VERB]', '->', 'love', '1.00')]
    """
    rules = []
    base_structure, syntactic_structure = generateStructure(wordlist)
    word_rules = generateWordRules(syntactic_structure)
    seg_rules = generateSegRules(base_structure)
    rules = word_rules + seg_rules
    return rules

def calculateProbability(rules, word):
    """
    计算某个口令的概率
    @param: rules:规则集 word:口令字符串
    @return：该口令在该规则集中出现的概率
    """
    word_rules = [w for w in rules if w[0] == 'N1']
    seg_rules = [w for w in rules if w[0] != 'N1']
    after_seg_word = process(word)
    wordlist = [after_seg_word]
    rules = generateRules(wordlist)
    new_rules = []
    for rule in rules:
        if rule[0] == 'N1':
            if len([w for w in word_rules if w[2] == rule[2]]) != 0:
                probability = float(
                    [w[3] for w in word_rules if w[2] == rule[2]][0])
            else:
                probability = 0
            new_rules.append((rule[0], rule[1], rule[2], '%.4f' % probability))
        else:
            if len([w for w in seg_rules if w[0] == rule[0] and w[2] == rule[2]]) != 0:
                probability = float(
                    [w[3] for w in seg_rules if w[0] == rule[0] and w[2] == rule[2]][0])
            else:
                probability = 0
            new_rules.append((rule[0], rule[1], rule[2], '%.4f' % probability))
    final_probability = 1
    for rule in new_rules:
        final_probability = final_probability * float(rule[3])
    return final_probability


def chooseBestRules(rules):
    probability = ['0.0'] + [w[3] for w in rules]
    probability_sum = []
    for i in xrange(0, len(rules) + 1):
        temp_pro = 0.0
        for j in xrange(0, i + 1):
            temp_pro = temp_pro + float(probability[j])
        probability_sum = probability_sum + [str(temp_pro)]
    probability_sum[-1] = 1.0
    choose_rule = []
    random_num = "{:.3f}".format(random.random())
    for i in xrange(0, len(probability_sum)):
        if float(random_num) < (float(probability_sum[i])):
            choose_rule = rules[i - 1]
            break
    if len(choose_rule) == 0:
        choose_rule = rules[-1]
    return choose_rule


def getProbabilitiestPassword(rules, num):
    """
    生成最高概率的N个词
    @param: rules:规则集 num:生成最有可能口令个数
    @return：在规则集中最有可能口令
    """
    word_rules = [w for w in rules if w[0] == 'N1']
    seg_rules = [w for w in rules if w[0] != 'N1']
    probabilitiest_password_set = []
    for i in xrange(0, num):
        choose_word_rule = chooseBestRules(word_rules)
        syntactic_structure = choose_word_rule[2]
        temp_syntactic_structure = syntactic_structure.replace(']', ']|')
        base_structure = temp_syntactic_structure.split("|")[:-1]
        probabilitiest_password = []
        for w in base_structure:
            seg_set = [i for i in seg_rules if i[0] == w]
            choose_seg_rule = chooseBestRules(seg_set)
            probabilitiest_password.append(choose_seg_rule[2])
        probabilitiest_password_set.append(''.join(probabilitiest_password))
    return probabilitiest_password_set

if __name__ == '__main__':
    word = ['iloveyou2', 'ihatedthem3', 'football3']
    print '口令列表：'
    print word
    wordlist = [process(w) for w in word]
    rules = generateRules(wordlist)
    print '口令规则集：'
    pprint(rules)
    print '在规则集中最有可能的3个新口令：'
    print getProbabilitiestPassword(rules,3)
    probability = calculateProbability(rules,'youlovethem2')
    print ('%s 在规则集中的概率是：%f') %('youlovethem2',probability)


