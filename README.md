# SemanticGuessGenerator
A guess generator which could generate some guess passwords through semantic method

##segment.py
- Segmentation.getAllSegment(s)
    - 给出s所有可能分段情况
    - Input：'anyone'
    - Output：[['any','one'],['anyone']]
- Segmentation.getBestSegment(s)
    - 给出s最佳分段
    - Input：'anyone'
    - Output：[['anyone']]

##postag.py
- PosTagging.posTagging(s)
    - 对一个分段进行POS标记
    - Input：['i','love','you']
    - Output：[('i', 'PRON'), ('love', 'VERB'), ('you', 'PRON')]

##semanticclassify.py
- SemanticClassification.semanticClassify(s)
    - 对分段进行语义分类，仅动词和名词具有语义标签，需要先进行POS标记
    - Input：[('i', 'PRON'), ('love', 'VERB'), ('you', 'PRON')]
    - Output：[('i', 'PRON', ' '), ('love', 'VERB', 'love.n.01'), ('you', 'PRON', ' ')]

##segment_pos_semanticclassify.py
- 对口令进行分段、POS标记和语义分类操作
- 需要segment.py，postag.py，semanticclassify.py和string_classify_extracctor.py

##generate_guess.py
- generateStructure(wordlist)
    - 生成口令列表的基础结构和句法结构
    - Input：经过segment_pos_semanticclassify.process处理后的单词列表
    - Output：base_structure and syntactic_structure
- generateRules(wordlist)
    - 生成单词列表的所有规则（词规则+片段规则）
    - Input：经过segment_pos_semanticclassify.process处理后的单词列表
    - Outout：word_rules + seg_rules
- calculateProbability(rules, word)
    - 计算某个口令在规则集中的概率
    - Input：rules:规则集 word:口令字符串
    - Output：该口令在该规则集中出现的概率
- getProbabilitiestPassword(rules, num)
    - 生成规则集中最高概率的N个词
    - Input：rules:规则集 num:生成最有可能口令个数
    - Output：在规则集中最有可能的N个口令

Hello GitHub!
