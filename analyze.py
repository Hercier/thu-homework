# coding=utf-8
from wordcloud import WordCloud
import numpy as np
from PIL import Image
import math
content = ""
poems = []
words = []
word_total_counts, poems_total_counts = 0, 0
dic = {}
dicidf = {}
def getPoems(fileName):
    global poems, poems_total_counts, poems, content
    with open(fileName, 'r', encoding='utf-8',errors = 'ignore') as f:
        poem ='|'+ f.readline()
        i=0;
        while poem:
#            if i>1000 :
#                break
            if len(poem)>2 :
                poems_total_counts += 1
                poems.append(poem)
                content += poem
                #print(poem)
            poem = f.readline()
            i=i+1;
    print("total {} poems!".format(poems_total_counts))

def countWords(fileName):
    global word_total_counts, word
    with open(fileName, 'r', encoding='utf-8', errors = 'ignore') as f:
        line = f.readline()
        line = f.readline()
        while line:
            word = line.split('\t')[-2];
            freq = content.count('|'+word+'|')
            if len(word) > 0 and freq != 0:
                words.append([word, freq,0.0])
                word_total_counts += freq
            line = f.readline()
    print("total {} words, appear {} times!".format(len(words), word_total_counts))


def solve(fileName1, fileName2):
    global dic,dicidf
    print("Start Calculate idf")
    with open(fileName1, 'w', encoding='utf-8') as f:
        j=0;
        for word in words:
            pos, cnt = 0,0
            for poem in poems:
                pos=poem.count('|'+word[0]+'|')
                if pos!=0:
                    cnt=cnt+1
            idf = math.log(poems_total_counts/cnt)
            word[2]=words[j][2]=idf
            j=j+1
            if len(word[0])!=1 :
                dic[word[0]]=word[1]
            dicidf[word[0]]=word[2]
            f.write("{} ATF={} IDF={}\n".format(word[0], word[1], word[2]))
    print("IDF finish")
    with open(fileName2, 'w', encoding='utf-8') as f:
        for poem in poems:
            docword=poem.split('|')
            #print(docword)
            docsiz=len(docword)
            j=0;
            doclis=[]
            for word in docword:
                if word!='' and word!='\n' and word!='，' and word!='。':
                    tf=docword.count(word)/docsiz
                    if word in dicidf:
                        v=tf*dicidf[word]
                        doclis.append([word,tf*dicidf[word]])
                j=j+1;
            doclis.sort(key=lambda s:(-s[1]));
            np.unique(doclis)
            f.write(poem+" keywords:")
            for i in range(0, 3):
                f.write(" {}".format(doclis[i][0]))
            f.write("\n")

def draw(fileName):
    print("Start Drawing")
    mask_image = np.array(Image.open("alice_mask.png"))
    wordcloud = WordCloud(
                        font_path='simhei.ttf',
                        background_color='white',
                        width=1000,
                        height=1400,
                        mask=mask_image
                ).generate_from_frequencies(dic)
    wordcloud.to_file(fileName)

if __name__ == '__main__':
    getPoems('TopWORDS_SegmentedText.txt')
    countWords('TopWORDS_CompleteDict.txt')
    solve('output_data.txt', 'output_poem.txt')
    draw('wordcloud.png')