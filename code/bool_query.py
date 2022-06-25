import json
import os

extra_and_dict:dict = {}

def fn_timer(fn):
    def function_timer(*args, **kwargs):
        """装饰器"""
        from time import time
        t = time()
        result = fn(*args, **kwargs)
        print('%s函数运行%.3f秒' % (fn.__name__, time() - t))
        return result
    return function_timer

def AND_func(key_word:str ,ans:set ,invert_index:dict):
    temp_set = set([docID for docID, _ in invert_index[key_word]])
    ans = ans & temp_set if len(ans) else temp_set
    for docID, num in invert_index[key_word]:
        if docID in temp_set:
            if docID in extra_and_dict.keys():
                extra_and_dict[docID] += num
            else:
                extra_and_dict[docID] = num
        else:
            extra_and_dict.pop(docID,None)
    return ans

def OR_func(key_word:str ,ans:set ,invert_index:dict):
    temp_set = set([x for x, _ in invert_index[key_word]])
    return ans | temp_set

def NOT_func(key_word:str ,ans:set ,invert_index:dict):
    temp_set = set([x for x, _ in invert_index[key_word]])
    return ans - temp_set

def get_bool_filter() -> dict:
    query_filter_file_path = os.path.join(os.getcwd(), 'query.json')
    with open(query_filter_file_path, 'r', encoding='utf8') as fp:
        return json.loads(fp.read())

def read_invert_index():
    path = os.path.join(os.getcwd(),'../invert_index.txt')
    with open(path,'r',encoding='utf8') as fp:
        return eval(fp.read())

# @fn_timer
def db_query(bool_filter, invert_index):
    global extra_and_dict
    ans = set()
    for operator, key_words in bool_filter.items():
        func= eval(operator+'_func')
        for key_word in key_words:
            ans = func(key_word,ans,invert_index)
    return ans , sorted(extra_and_dict.items(), key=lambda x: x[1], reverse=True)

def main():
    invert_index = read_invert_index()
    bool_filter = get_bool_filter()
    # print(bool_filter)
    ans ,sorted_ans = db_query(bool_filter, invert_index)
    print(ans, sorted_ans)


if __name__ == '__main__':
    main()