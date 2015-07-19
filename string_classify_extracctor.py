#-*- coding:utf-8 -*-
#author: nichijouYC

import re

class StringClassifyExtractor(object):

    def __init__(self):
        self.string_type = [0,0,0]

    def getStringType(self,s):
        """
        返回字符串的类型
        Input：'@123pr'
        Output: 'num+char+spe'
        """
        numre = re.search('[0-9]', s)
        charre = re.search('[a-zA-Z]', s)
        specialre = re.search('[^\w]', s)
        num_type = 1 if numre else 0
        char_type = 1 if charre else 0
        spe_type = 1 if specialre else 0
        self.string_type = [num_type,char_type,spe_type]
        if self.string_type == [1,0,0]:
            return 'num'
        elif self.string_type == [0,1,0]:
            return 'char'
        elif self.string_type == [0,0,1]:
            return 'special'
        elif self.string_type == [1,1,0]:
            return 'num+char'
        elif self.string_type == [1,0,1]:
            return 'num+spe'
        elif self.string_type == [0,1,1]:
            return 'char+spe'
        elif self.string_type == [1,1,1]:
            return 'num+char+spe'
        else:
            return 'this string is none of num,char,spe'

    def getSubstringAllType(self,s):
        """
        返回字符串所有类型的子串(按原有字符串顺序)
        Input：'@123pr'
        Output: [('@','spe'),('123','num'),('pr','char')]
        """
        self.getStringType(s)
        if self.string_type == [1,0,0]:
            return [("%s"%s,'num')]
        elif self.string_type == [0,1,0]:
            return [("%s"%s,'char')]
        elif self.string_type == [0,0,1]:
            return [("%s"%s,'spe')]
        elif self.string_type == [1,1,0]:
            num = re.split('[a-zA-Z]', s)
            char = re.split('[0-9]', s)
            while '' in num:
                num.remove('')
            while '' in char:
                char.remove('')
            temp = [(w, s.index(w)) for w in num + char]
            temp.sort(key=lambda x: x[1])
            temp = [w[0] for w in temp]
            result = []
            for w in temp:
                if w in num:
                    result.append((w,'num'))
                if w in char:
                    result.append((w,'char'))
            return result
        elif self.string_type == [1,0,1]:
            num = re.split('[^\w]', s)
            spe = re.split('[0-9]', s)
            while '' in spe:
                spe.remove('')
            while '' in num:
                num.remove('')
            temp = [(w, s.index(w)) for w in spe + num]
            temp.sort(key=lambda x: x[1])
            temp = [w[0] for w in temp]
            result = []
            for w in temp:
                if w in spe:
                    result.append((w,'spe'))
                if w in num:
                    result.append((w,'num'))
            return result
        elif self.string_type == [0,1,1]:
            spe = re.split('[a-zA-Z]', s)
            char = re.split('[^\w]', s)
            while '' in spe:
                spe.remove('')
            while '' in char:
                char.remove('')
            temp = [(w, s.index(w)) for w in spe + char]
            temp.sort(key=lambda x: x[1])
            temp = [w[0] for w in temp]
            result = []
            for w in temp:
                if w in spe:
                    result.append((w,'spe'))
                if w in char:
                    result.append((w,'char'))
            return result
        elif self.string_type == [1,1,1]:
            spe = re.split('[\w]', s)
            char = re.split('[0-9]|[^\w]', s)
            num = re.split('[a-zA-Z]|[^\w]', s)
            while '' in spe:
                spe.remove('')
            while '' in char:
                char.remove('')
            while '' in num:
                num.remove('')
            temp = [(w, s.index(w)) for w in num + char + spe]
            temp.sort(key=lambda x: x[1])
            temp = [w[0] for w in temp]
            result = []
            for w in temp:
                if w in spe:
                    result.append((w,'spe'))
                if w in char:
                    result.append((w,'char'))
                if w in num:
                    result.append((w,'num'))
            return result
        else:
            return 'this string is none of num,char,spe'

if __name__ == '__main__':
    extractor = StringClassifyExtractor()
    print extractor.getStringType('123')
    print extractor.getSubstringAllType('123')
    print extractor.getStringType('abc')
    print extractor.getSubstringAllType('abc')
    print extractor.getStringType('@!~')
    print extractor.getSubstringAllType('@!~')
    print extractor.getStringType('123abc4')
    print extractor.getSubstringAllType('123abc4')
    print extractor.getStringType('123@4!')
    print extractor.getSubstringAllType('123@4!')
    print extractor.getStringType('a@!bc')
    print extractor.getSubstringAllType('a@!bc~~')
    print extractor.getStringType('123a@!bc')
    print extractor.getSubstringAllType('123a@!bc')
    print extractor.getStringType('')
    print extractor.getSubstringAllType('')

