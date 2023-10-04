import jieba
import random
import math
import re
import wordcloud
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
 
 
def read_stop_words():
    ''' 读取停用词函数'''
    with open("stopwords_list.txt",'r',encoding='utf-8') as f:
        stopwords = f.read().splitlines()  #用splitlines()函数 将读取的每一行作为一个元素存入列表stopwords中
        
        return stopwords  #返回停用词列表
    
def load_special_words():
    jieba.load_userdict("special_words.txt")

    
def read_job_desc(file_name:str):
    '''读取数据集的函数'''
    with open(file_name,"r",encoding='utf-8') as f:
        text = f.read()  #使用reader()函数，将整个数据集每行作为一个元素，存入reader列表
        text = re.sub('\s+', '', text) 
        return text   #返回已每条弹幕作为元素的列表
    
    
def count_word_frequ(texts, stopwords):
    load_special_words()
    '''这是一个统计词频的函数'''
    words_list = jieba.lcut(texts) 
    words_list = [word for word in words_list if word not in stopwords]
    words_counts = dict(Counter(words_list))
        # 生成词频统计表
    table = pd.DataFrame(columns=['词语', '词频']) # 生成空表
    table['词语'] = list(words_counts.keys())   # 词语字段保存词语
    table['词频'] = list(words_counts.values()) # 词频字段保存词语对应的词频
    table = table.sort_values(by=['词频'], ascending=False) # 按照词频降序排序
    
    return table       
        
 
def filter_low_freq_words(counts):
    '''这是一个筛选词频的函数'''
    items = list(counts.items()) #将之前的词频字典转化为元组为元素的列表
    items1 = items[:]
    for i in items1:
        #如果词频小于5就将其删除
        if i[1] <= 5:  
            items.remove(i)
    counts1 = dict(items)
    
    return counts1
 
 
def matrix(counts1,rows):
    '''这是一个根据弹幕生成向量矩阵的函数'''
    matrics = []
    n = len(counts1)
    items = list(counts1.keys())
    for row in rows:  #对每条弹幕进行遍历  
        words = jieba.lcut(row) #对一条弹幕进行分词
        if len(words) <=7:  #如果一条弹幕总词组数量小于7，则不计入矩阵
            pass
        else:
            #找到对于单词对应的位置，在该位置设置标记
            lis = [0]*n
            for word in words:
                if word in items:
                    lis[items.index(word)] = 1 
            matrics.append(lis)
            
    return matrics,n
 
 
def distance(n,matrics):
    '''这是一个计算不同弹幕距离的函数'''
    sums = 0
    mole = 0
    #随机找出矩阵中的两个向量
    for i in range(n):
        x = random.randint(0,10)
        y = random.randint(0,10)
        sums = (matrics[x][i] - matrics[y][i])**2 + sums
        mole = mole + matrics[x][i]*matrics[y][i]
    # 计算欧式距离
    distance_euc = math.sqrt(sums)
    sum1 = sum(matrics[x]);sum2 = sum(matrics[y])
    deno = math.sqrt(sum1*sum2)
    #计算余弦距离
    if deno == 0:
        distance_cos = 0
    else:
        distance_cos = mole/deno    
        
    return distance_euc, distance_cos    
 
 
def plot_Wc(counts1):
    '''这是将词频字典生成词云的函数'''
    #主结构很像前端里面CSS的写法
    wc = wordcloud.WordCloud(             #根据词频字典生成词云图
            max_words=100,  # 最多显示词数
            max_font_size=300,  # 字体最大值
            background_color="white",  # 设置背景为白色，默认为黑色
            width = 1500,  # 设置图片的宽度
            height= 960,  # 设置图片的高度
            margin= 10,  # 设置图片的边缘
        )
    wc.generate_from_frequencies(counts1)  # 从字典生成词云
    plt.imshow(wc)  # 显示词云
    plt.axis('off')  # 关闭坐标轴
    plt.show()  # 显示图像
 
 
def TF_IDF(counts1,rows):
    '''对TF_IDF进行构建'''
    n = len(counts1)
    m = len(rows)
    counts_IF = counts1
    for i in counts1:
        #计算tf
        tf = counts1.get(i)/n
        count = 0
        for row in rows:
            words = jieba.lcut(row)
            if i in words:
                count = count + 1
        #计算idf
        idf = math.log(m/count)
        #两者求积得tf_idf
        tf_idf = tf*idf
        counts_IF[i] = tf_idf
        
    return counts_IF
        
 
def count_file_words(file_name:str):
    '''这是主函数对之前定义的函数进行调用'''
    stopwords = read_stop_words() #停用词列表
    texts = read_job_desc(f'{file_name}.txt')  #弹幕列表
    words_count_table = count_word_frequ(texts, stopwords)  #词频列表
    print(words_count_table)
    words_count_table.to_excel(f'{file_name}.xlsx', index=False) # 将结果保存为 excel 表
 
if __name__ == '__main__':
    count_file_words("blockchain_engineer")