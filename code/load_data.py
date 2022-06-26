import functools
import os
import numpy as np
# ==================global================
Term_list = []
Term_set = set([])
Term_dict = {}
Term_ind = 0
# ==================class================

# 主链节点的对象
class Term:
    def __init__(self, next, term="", df=0) -> None:
        self.term = term
        self.df = df
        self.next = next

    def set_element(self, term, docID) -> None:
        self.term = term
        self.docID = docID

    def add_df(self) -> None:
        self.df += 1

    def get_next(self):
        return self.next

    def get_term(self) -> str:
        return self.term

    def get_df(self) -> int:
        return self.df


# 主链中分支节点的对象
class Node:
    def __init__(self, docID=0, tf=0) -> None:
        self.docID = docID
        self.tf = tf

    def get_docID(self) -> int:
        return self.docID

    def get_tf(self) -> int:
        return self.tf

# 检查当前词项是否为中文词项
def check(term):
    if len(term) > 1:
        for i in term:
            if i < '\u4e00' or i > '\u9fa5': return False
        return True
    return False


def insert_docID(in_term, docID, term_fre):
    in_term.add_df()
    docID_list = in_term.get_next()
    new_node = Node(docID, term_fre)
    docID_list.append(new_node)


# 还需要书写一个插入函数负责进行词项插入主链中
def insert_Term(term, docID, term_fre) -> None:
    global Term_list, Term_set, Term_dict, Term_ind
    if term in Term_set:
        in_term = Term_list[Term_dict[term]]
        insert_docID(in_term, docID, term_fre)
    else:
        Term_dict[term] = Term_ind
        Term_ind += 1
        Term_set.add(term)
        new_Term = Term([], term)
        # print(term)
        insert_docID(new_Term, docID, term_fre)
        Term_list.append(new_Term)


def my_compare(x, y):
    if x.get_term() > y.get_term():
        return 1
    elif x.get_term() < y.get_term():
        return -1
    return 0


def main():
    # 创建停用词表 用于过滤掉停用词
    with open('code/stop_word.txt', 'r', encoding='utf-8') as f:
        stopwords = list(f.read().split())

    base_path = os.path.abspath((os.path.join(os.getcwd(), '..')))
    filePath = os.path.join(base_path,'rawdata')

    files = os.listdir(filePath)
    for file_index,file in enumerate(sorted(files[:10])):
        try:
            print('processing:' ,file)
            file = os.path.join(filePath, file)
            with open(file, 'r', errors='ignore', encoding='gbk') as fp:
                terms= fp.read().split()
            terms = dict(zip(*np.unique(terms, return_counts=True)))
            for term in terms.keys():
                if check(term) and (term not in stopwords):
                    # 将来还会添加的要求就是尽可能的也可以得出在文章中的位置
                    insert_Term(term, file_index,terms[term])
        except Exception as e:
            print("Error : %s" % e)

    Term_list.sort(key=functools.cmp_to_key(my_compare))
    # 保存为json文件
    with open('invert_index.txt', 'w') as fp:
        fp.write('{')
        for term in Term_list:
            # 这个最后要打开json把第一个逗号删掉
            # fp.write(f'\t"{term.get_term()}_{term.get_df()}":')
            fp.write(f'\n,"{term.get_term()}":')
            term_list = term.get_next()
            fp.write('[')
            fp.write(f'({term_list[0].get_docID()},{term_list[0].get_tf()})')
            for doc in term_list[1:]:
                fp.write(f',({doc.get_docID()},{doc.get_tf()})')
            fp.write("]")
        fp.write('}')

if __name__=="__main__":
    main()