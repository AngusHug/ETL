# coding:utf-8
import os
import json
import pickle
import hashlib
from collections.abc import Iterable


def _hashfunc(x):
    return int(hashlib.md5(x).hexdigest(), 16)


class Trie(object):
    """定义基本的Trie树结构，便于存储词典（词+词频）。
    主要的代码量是基于Python类的特殊方法来定义一些函数，
    达到表面上看起来和dict的使用方法基本一致的效果。
    """
    
    def __init__(self, insert_path=None, pos=False):
        self.dic = {}  # 叶子节点值为{father_char:son_char},尾节点值为{True:word}
        self.end = True
        self.pos = pos
        # 从文件中加载，文件的每一行是 词
        if isinstance(insert_path, str) and os.path.exists(insert_path):
            if insert_path.endswith(".pkl"):
                with open(insert_path, 'rb') as f:
                    self.dic = pickle.load(f)
            else:
                with open(insert_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if self.pos:
                            line = line.rstrip('\n').split('\t')
                            self.additem(line[0], float(line[1]))
                        else:
                            self.additem(line.rstrip('\n'))
    
    def additem(self, word, pos=None):
        self.root = self.dic
        for char in word:
            if char not in self.root:
                self.root[char] = {}
            self.root = self.root[char]
        
        if pos:
            self.root[self.end] = (word, pos)
        else:
            self.root[self.end] = word
    
    def delitem(self, item):  # 删除某个词
        self.root = self.dic
        for char in item:
            if char not in self.root:
                return None
            self.root = self.root[char]
        
        if self.end in self.root:
            del self.root[self.end]
    
    def search(self, sent):  # 返回字符串中所有能找到的词语
        result = {}  # 结果是{(start, end): (词)}的字典
        for i, _ in enumerate(sent):
            self.root = self.dic
            for j, char in enumerate(sent[i:]):
                if char in self.root:
                    self.root = self.root[char]
                    if self.end in self.root:
                        result[i, i + j + 1] = self.root[self.end]
                else:
                    break
        return result
    
    def save(self, save_path):
        with open(save_path, 'wb') as f:
            pickle.dump(self.dic, f)


class TrieNode(object):
    def __init__(self, value=None, pos=None):
        self.value = value  # 值
        self.pos = pos  # 实体名称
        self.fail = None  # 失败指针
        self.tail = None  # 尾标志，储存单词
        self.word_length = -1
        self.children = {}  # 子节点，{value:TrieNode}


class TrieAC(object):
    
    def __init__(self, insert_path=None, pos=False):
        self.root = TrieNode()  # 根节点
        self.pos = pos
        
        if isinstance(insert_path, str) and os.path.exists(insert_path):
            if insert_path.endswith(".pkl"):
                with open(insert_path, 'rb') as f:
                    self.dic = pickle.load(f)
            else:
                with open(insert_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if self.pos:
                            line = line.rstrip('\n').split('\t')
                            self.additem(line[0], float(line[1]))
                        else:
                            self.additem(line.rstrip('\n'))
        
        self.ac_automation()
    
    def additem(self, word, pos=None):
        """
        插入一个字符串
        :param word: 字符串
        """
        cur_node = self.root
        for item in word:
            if item not in cur_node.children:
                # 插入结点
                child = TrieNode(value=item)
                cur_node.children[item] = child
                cur_node = child
            else:
                cur_node = cur_node.children[item]
        cur_node.tail = word
        cur_node.word_length = len(word)
        if pos:
            cur_node.pos = pos
    
    def ac_automation(self):
        """
        构建失败路径
        """
        queue = [self.root]
        # BFS遍历字典树
        while len(queue):
            temp_node = queue[0]
            # 取出队首元素
            queue = queue[1:]
            for value in temp_node.children.values():
                # 根的子结点fail指向根自己
                if temp_node == self.root:
                    value.fail = self.root
                else:
                    # 转到fail指针
                    p = temp_node.fail
                    while p:
                        # 若结点值在该结点的子结点中，则将fail指向该结点的对应子结点
                        if value.value in p.children:
                            value.fail = p.children[value.value]
                            break
                        # 转到fail指针继续回溯
                        p = p.fail
                    # 若为None，表示当前结点值在之前都没出现过，则其fail指向根结点
                    if not p:
                        value.fail = self.root
                # 将当前结点的所有子结点加到队列中
                queue.append(value)
    
    def search(self, text):
        p = self.root
        result = {}  # 结果是{(start, end): (词)}的字典
        for i in range(len(text)):
            single_char = text[i]
            while single_char not in p.children and p is not self.root:
                p = p.fail
            # 有一点瑕疵，原因在于匹配子串的时候，若字符串中部分字符由两个匹配词组成，此时后一个词的前缀下标不会更新
            # 这是由于KMP算法本身导致的，目前与下文循环寻找所有匹配词存在冲突
            # 但是问题不大，因为其标记的位置均为匹配成功的字符
            # 若找到匹配成功的字符结点，则指向那个结点，否则指向根结点
            if single_char in p.children:
                p = p.children[single_char]
            else:
                p = self.root
            
            temp = p
            while temp is not self.root:
                # 尾标志为0不处理，但是tail需要-1从而与敏感词字典下标一致
                # 循环原因在于，有些词本身只是另一个词的后缀，也需要辨识出来
                if temp.tail:
                    if self.pos:
                        result[i - temp.word_length + 1, i + 1] = (temp.tail, temp.pos)
                    else:
                        result[i - temp.word_length + 1, i + 1] = temp.tail
                temp = temp.fail
        return result


class DAG(object):
    """定义一般的有向无环图（Directed Acyclic Graph）对象，
    便于在各种场景下使用。其中optimal_path方法使用viterbi
    算法来给出最优路径。
    """
    
    def __init__(self, nb_node, null_score=-1000):
        self.edges = {}
        self.nb_node = nb_node
        self.null_score = null_score
    
    def __setitem__(self, start_end, score):  # 构建图上的加权边
        start, end = start_end  # key是(start, end)下标对
        if start not in self.edges:
            self.edges[start] = {}
        self.edges[start][end] = score
    
    def optimal_path(self):
        """动态规划求最优路径
        result的key是当前字的下标，代表截止到前一字的规划结果，
        result的第一个值是list，表示匹配片段的(start, end)下标对；
        result的第二个值是路径的分数
        """
        result = {0: ([], 1)}
        start = 0  # 当前字的下标
        length = self.nb_node
        while start < length:
            if start in self.edges:  # 如果匹配得上
                for i, j in self.edges[start].items():  # 这里i是终止下标
                    score = result[start][1] + j  # 当前路径分数
                    # 如果当前路径不在result中，或者它的分数超过已有路径，则更新
                    if i not in result or (score >= result[i][1]):
                        result[i] = result[start][0] + [(start, i)], score
            
            # 为了下一步的匹配，如果下一字还不在result中，
            # 就按单字来插入，概率为null_score
            if start + 1 not in result:
                score = result[start][1] + self.null_score
                result[start + 1] = result[start][0] + [(start, start + 1)], score
            
            start += 1
        
        return result[self.nb_node][0]


class Tokenizer(object):
    def __init__(self, trie):
        self.trie = trie
    
    def __call__(self, sent, quer_v=None):
        dag = DAG(len(sent))
        ts = self.trie.search(sent)
        for i in ts.keys():
            dag[i] = -1
        
        dags = dag.optimal_path()
        res = [ts[key] for key in dags if key in ts]
        return res


class SimHash(object):
    def __init__(self, features, bits=64, hashfunc=None):
        self.bits = bits
        if hashfunc:
            self.hashfunc = hashfunc
        else:
            self.hashfunc = _hashfunc
        
        self.value = self.simhash(features)
    
    def __str__(self):
        return str(self.value)
    
    def build_by_features(self, features):
        """
        `features` might be a list of unweighted tokens (a weight of 1
                    will be assumed), a list of (token, weight) tuples or
                    a token -> weight dict.
        """
        v = [0] * self.bits
        masks = [1 << i for i in range(self.bits)]
        if isinstance(features, dict):
            features = features.items()
        for f in features:
            if isinstance(f, str):
                h = self.hashfunc(f.encode('utf-8'))
                w = 1
            else:
                assert isinstance(f, Iterable)
                h = self.hashfunc(f[0].encode('utf-8'))
                w = f[1]
            for i in range(self.bits):
                v[i] += w if h & masks[i] else -w
        ans = 0
        for i in range(self.bits):
            if v[i] > 0:
                ans |= masks[i]
        return ans
    
    def simhash(self, features):
        hashcode = self.build_by_features(features)
        return hashcode
    
    def distance(self, another):
        x = self.value ^ another.value
        ans = 0
        while x:
            ans += 1
            x &= x - 1
        return ans


class DoubleArrayAhoCorasickAutoMation(object):
    def __init__(self, path=None):
        with open(path, 'r', encoding='utf-8') as f:
            dic = json.load(f)
        self.base = dic['base']
        self.check = dic['check']
        self.next = dic['next']
        self.value = dic['value']
        self.base_length = len(self.base)
        # 记录每个词的长度
        self.word_length = [0 for _ in self.base]
        for i, value in enumerate(self.value):
            if value:
                self.word_length[i] = len(value[0])
    
    def search(self, text):
        match_pair = {}
        parent_index = 0
        parent_value = 1
        for i, w in enumerate(text):
            w_index = self.get_index(w)
            while not (
                parent_value + w_index <= self.base_length and self.base[parent_value + w_index] != 0 and self.check[
                parent_value + w_index] == parent_index) and (parent_index > 0):
                parent_index = self.next[parent_index]
                parent_value = abs(self.base[parent_index])
            
            if parent_value + w_index <= self.base_length and self.base[parent_value + w_index] != 0 and self.check[
                parent_value + w_index] == parent_index:
                parent_index = parent_value + w_index
                parent_value = abs(self.base[parent_index])
            else:
                parent_index = 0
                parent_value = 1
            
            tmp_index = parent_index
            while tmp_index > 0:
                if self.base[tmp_index] < 0:
                    match_pair[i - self.word_length[tmp_index] + 1, i + 1] = self.value[tmp_index]
                tmp_index = self.next[tmp_index]
        return match_pair
    
    def get_index(self, w):
        return ord(w) + 1


if __name__ == "__main__":
    ac = DoubleArrayAhoCorasickAutoMation('DoubleArrayAhoCorasickAutoMation.json')
    msgs = ["尊敬的客户王者荣耀王者,您尾号123"]
    for msg in msgs:
        print(ac.search(msg))
