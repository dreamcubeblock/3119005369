import sys
import nltk
import jieba
import re
import os

#import time
import gensim
def calc_similarity(text1,text2):
    texts=[text1,text2]
    dictionary = gensim.corpora.Dictionary(texts)
    #print(dictionary)
    corpus = [dictionary.doc2bow(text) for text in texts]
   # print(corpus)
    similarity = gensim.similarities.Similarity('-Similarity-index', corpus, num_features=len(dictionary))
    test_corpus_1 = dictionary.doc2bow(text1)
    cosine_sim = similarity[test_corpus_1][1]
    return cosine_sim
def filter(str):
    str = jieba.lcut(str)
    result = []
    for tags in str:
        if (re.match(u"[a-zA-Z0-9\u4e00-\u9fa5]", tags)):
            result.append(tags)
        else:
            pass
    return result
if __name__ == '__main__':
  #  start = time.clock()
    assert len(sys.argv)==4,"输入不符合规范，缺少文件目录"
    assert os.path.exists(sys.argv[1]),"原文文件不存在，请检查文件目录是否正确"
    assert os.path.exists(sys.argv[2]),"抄袭文件不存在，请检查文件目录是否正确"
   # assert os.path.exists(sys.argv[1]),"文件不存在，请检查文件目录是否正确"
    real_txt=open(sys.argv[1],encoding='utf8')

    copy_txt=open(sys.argv[2],encoding='utf8')
    str1=real_txt.read()
    str2=copy_txt.read()
    #print(str2)
    text1 = filter(str1)
    text2 = filter(str2)
   # print(text2)
    sim=calc_similarity(text1,text2)
    print("重复率："+str(round(sim,2)))
    realrootname=sys.argv[1].split("/")[-1]
    rootname=sys.argv[2].split("/")[-1]
    #print(rootname)
    with open(sys.argv[3],"a") as f:
            f.write(realrootname+" and "+rootname+":"+str(round(sim,2))+"\n")
   # end = time.clock()
   # print("final is in ", end - start)

