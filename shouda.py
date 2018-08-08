import re, collections
import time

alphabet = 'abcdefghijklmnopqrstuvwxyz'
open_r=open("big.txt",'r')
#print(open_r)
big_info=open_r.read()
#print(len(big_info))
open_r.close()

#提取单词，即把所有的标点符号都去掉，并且转化为小写
def words(info):
	return re.findall("[a-z]+",info.lower())

#统计每个词的词频
def wordIndex(wordtext):
	words={}
	for word in wordtext:
		if word in words:
			words[word]=words[word]+1;
		else:
			words[word]=1
#			print(word)
	return words



wordslist=words(big_info)
#print(wordslist)
words_map=wordIndex(wordslist)

#print(len(words_map))

def known(word):
	word_exist=[]
	for word_one in word:
		if word_one in words_map:
			word_exist.append(word_one)
	return word_exist

#w="apple pie"
#print(known(w))





# 咱这里只能定性的分析，即默认使 love输错一个字母得到错误单词的概率相等，
# 即P(lovl|love)=P(lovel|lovle)=P(lvoe|love)=P(lov|love)(这里的转换要注意)，
# 而假设输错两个字母得到的错误单词的概率相等，但是这个概率值肯定要远远小于输入一个字母的概率，这个不用多做解释了吧。

def knomn_edit1(words):
    edit1_word = []
    n = len(words)#元素个数，实际上就1个
    # print(n)
    for j in range(n):
        # print(i)
        word = words[j]
        m = len(word)
        # print(m)#单词长度
        for i in range(m):
            # print(i)
            if i != m - 1:
                edit1_word.append(word[0:i] + word[i + 1:])  # 删掉索引为i的字符
                if i != m - 2:
                    edit1_word.append(word[0:i] + word[i + 1] + word[i] + word[i + 2:])  # 移动,实际上是把刚才删掉的字符移动到后面的位置
                    # print(edit1_word)
                else:
                    edit1_word.append(word[0:i] + word[i + 1] + word[i])  # 移动,实际上是如果是倒数第二个字符，就和倒数第一个交换位置了
                for ch in alphabet:
                    edit1_word.append(word[0:i] + ch + word[i + 1:])  # 替换，意思是第i个字符可能是输错的，所以替换
                    edit1_word.append(word[0:i] + ch + word[i:])  # 插入，意思是第i个字符后面可能是漏输入了一个，所以插入
            else:
                edit1_word.append(word[0:(m - 1)])  # 删，直接删掉最后一个字符
                for ch in alphabet:
                    edit1_word.append(word[0:(m - 1)] + ch)  # 替换，将最后一个字符用用字母表里所有字符替换
                    edit1_word.append(word[0:m] + ch)  # 插入，最后可能漏删了一个字符，插入所有可能字符
    return edit1_word



def know_edit2(word):
    words1 = knomn_edit1(word)
    words2 = knomn_edit1(words1)

    edit2_word = []
    for word2 in words2:
        if word2 in words_map:
            edit2_word.append(word2)
    return edit2_word


def correct(word):
    canword = known([word]) or known(knomn_edit1([word])) or know_edit2([word])
    if len(canword) == 0:#如果两步纠正还是没得到正确单词，那么就默认返回输入的错误单词
        canword = [word]
        print(canword)
    else:
        max_info = max(canword, key=lambda w: words_map[w])
        print(str(max_info) + "----P---" + str(words_map[max_info]))

w="appla"
# print(known(knomn_edit1([w])))#这么造了一堆词之后，哪些词是真实存在的。
# print(know_edit2([w]))
# print(known([w]))
# print(known(knomn_edit1([w])))
# print(know_edit2([w]))

# print(known([w]) or known(knomn_edit1([w])) or know_edit2([w]))
canword=['apple', 'apply']
max_info=max(canword, key=lambda w: words_map[w])
print(max_info)
# print(words_map[canword])
print(words_map[canword[0]])
print(words_map[canword[1]])
correct(w)
