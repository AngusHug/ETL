# 自动机节点
class Node(object):
    """AC自动机的树节点
    Attrobites"
        next:指向子节点
        fail:Node类型,自动机fail指针
        length:exists 判断节点是否为单词
    """
    
    __slots__ = ['next', 'fail', 'length']
    
    def __init__(self):
        self.next = {}
        self.fail = None
        self.length = -1
    
# 自动机实现
class Ahocorasick(object):
    def __init__(self):
        """初始化根节点"""
        self.__root = Node()
    
    def add_word(self, word):
        """添加单词到trie树"""
        current = self.__root
        for char in word:
            current = current.next.setdefault(char, Node())
        current.length = len(word)
        
    def make(self):
        """fail指针"""
        queue = list()
        for key in self.__root.next:
            self.__root.next[key].fail = self.__root
            queue.append(self.__root.next[key])
            
        # 广度优先算法遍历设置fai指针
        while len(queue) > 0 :
            
            # 基于当前结点的fail指针设置其子节点的fail指针
            current = queue.pop(0)
            
            for k in current.next:
                current_fail = current.fail
                
                # 若当前结点有fail指针，尝试设置其子节点的fail指针
                while current_fail is not None:
                    if k in current_fail.next:
                        current.next[k].fail = current_fail.next[k]
                        break
                    current_fail = current_fail.fail
                
                # 若当前结点fail指针不存在该子节点，令子节点fail指向根节点
                if current_fail is None:
                    current.next[k].fail = self.__root
                    
                queue.append(current.next[k])
                
    def search(self, content):
        """后向最大匹配
        对content文本进行多模匹配，返回后向最大匹配结果
        Args:
            content:string类型,用于多模式匹配字符串
        Retruns:
            list类型,最大匹配单词列表,每个元素为匹配的模式串的起止位置
            
        """
        result = []
        p = self.__root
        for current_position in range(len(content)):
            word = content[current_position]
            
            while word not in p.next:
                if p == self.__root:
                    break
                p = p.fail
            else:
                p = p.next[word]
                if p.length > 0 :
                    result.append((current_position-p.length+1, current_position))
        return result
    
    def seach_all(self, content):
        """
        对content的文本进行多模式匹配,返回所有匹配结果
        Args:
            content:string类型,用于多模匹配的字符串
        Returns:
            list类型,所有匹配单词列表，每个元素为匹配的模式串在居中的起始位置
        """
        result = []
        p = self.__root
        for current_position in range(len(content)):
            word = content[current_position]
            while word not in p.next:
                if p == self.__root:
                    break
                p = p.fail
            else:
                p = p.next[word]
                
                # 回溯查看是否存在以当前字符结尾的单词
                tmp = p
                while tmp != self.__root:
                    if tmp.length > 0:
                        result.append(
                            (current_position - tmp.length + 1,current_position)
                        )
        return  result
    