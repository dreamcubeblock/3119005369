import numpy as np
import sys 
import re

import jieba
import jieba.analyse
class simhash:
    def __init__(self,content):
        self.simhash=self.simhash(content)

    def __str__(self):
        return str(self.simhash)

    def simhash(self,content):
        #seg = jieba.cut(content)
        #jieba.analyse.set_stop_words('stopword.txt')
        keyWord = jieba.analyse.extract_tags(
            '|'.join(content), topK=10, withWeight=True, allowPOS=())#在这里对jieba的tfidf.py进行了修改
        #将tags = sorted(freq.items(), key=itemgetter(1), reverse=True)修改成tags = sorted(freq.items(), key=itemgetter(1,0), reverse=True)
        #即先按照权重排序，再按照词排序
        keyList = []
        for feature, weight in keyWord:
            weight = int(weight * 10)
            feature = self.string_hash(feature)
            temp = []
            for i in feature:
                if(i == '1'):
                    temp.append(weight)
                else:
                    temp.append(-weight)
            # print(temp)
            keyList.append(temp)
        list1 = np.sum(np.array(keyList), axis=0)
        #print(list1)
        if(keyList==[]): #编码读不出来
            return '00'
        simhash = ''
        for i in list1:
            if(i > 0):
                simhash = simhash + '1'
            else:
                simhash = simhash + '0'
        return simhash

    def similarity(self, other):
        a = float(self.simhash)
        b = float(other.simhash)
        if a > b : return b / a
        else: return a / b

    def string_hash(self,source):
        if source == "":
            return 0
        else:
            x = ord(source[0]) << 7
            m = 1000003
            mask = 2 ** 128 - 1
            for c in source:
                x = ((x * m) ^ ord(c)) & mask
            x ^= len(source)
            if x == -1:
                x = -2
            x = bin(x).replace('0b', '').zfill(64)[-64:]
            #print(source,x)

            return str(x)

    def hammingDis(self, com):
        t1 = '0b' + self.simhash
        t2 = '0b' + com.simhash
        n = int(t1, 2) ^ int(t2, 2)
        i = 0
        while n:
            n &= (n - 1)
            i += 1
        return i

if __name__ == '__main__':
    punc = './ <>_ - - = ", 。，？！“”：‘’@#￥% … &×（）——+【】{};；● &～| \s:'
    real_txt=open(sys.argv[1],encoding='utf8')
    string1=''
    string2=''
    copy_txt=open(sys.argv[2],encoding='utf8')
    real_txt=real_txt.read()
    copy_txt=copy_txt.read()
    real_txt = re.sub(r'[^\w]+', '',real_txt)
    seg=jieba.cut(real_txt)
    string1=string1.join(seg)
    line1 = re.sub(r"[{}]+".format(punc), "", string1)
    copy_txt = re.sub(r'[^\w]+', '',copy_txt)
    seg=jieba.cut(copy_txt)
    string2=string2.join(seg)
    line2 = re.sub(r"[{}]+".format(punc), "", string2)
    print(line2)
    print(line1)
    hash1=simhash(line1.split())
    hash2=simhash(line2.split())
    print(hash2.hammingDis(hash1))
   
    #with open(sys.argv[3],"a") as f:
    #        f.write(str(result)+"\n")
    #        f.write(str(result)+"\n")