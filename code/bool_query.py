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

def AND_func(ans:set ,index_table):
    temp_set = set(map(lambda x: x[0], index_table))
    return temp_set if ans == set() else ans & temp_set

def generate_extra_dict(ans, AND_filter, invert_index):
    for word in AND_filter:
        for docID, num in invert_index[word]:
            if docID in ans:
                if docID in extra_and_dict.keys():
                    extra_and_dict[docID] += num
                else:
                    extra_and_dict[docID] = num
            else:
                extra_and_dict.pop(docID, None)


def OR_func(ans:set ,index_table):
    return ans | set(map(lambda x: x[0], index_table))

def NOT_func(ans:set ,index_table):
    return ans - set(map(lambda x: x[0], index_table))

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
    try :
        ans = set()
        for operator, key_words in bool_filter.items():
            func= eval(operator+'_func')
            for key_word in key_words:
                ans = func(ans,invert_index[key_word])
        return ans, True
    except Exception:
        set(), False

def main():
    invert_index = read_invert_index()
    bool_filter = get_bool_filter()
    # print(bool_filter)
    ans = db_query(bool_filter, invert_index)
    generate_extra_dict(ans,bool_filter['AND'],invert_index)
    sorted_ans = list(sorted(extra_and_dict.items(), key=lambda x: x[1], reverse=True))
    print(ans, sorted_ans)


if __name__ == '__main__':
    main()