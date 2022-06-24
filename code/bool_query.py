import json
import os

extra_and_dict:dict = {}

def AND_func(key_word:str ,ans:set ,invert_index:dict):
    temp_set = set([docID for docID, _ in invert_index[key_word]])
    temp_set = ans & temp_set
    for docID, num in invert_index[key_word]:
        if docID in temp_set:
            if docID in extra_and_dict.keys():
                extra_and_dict[docID] += num
            else:
                extra_and_dict[docID] = num
        else:
            extra_and_dict.pop(docID,None)
    return temp_set

def OR_func(key_word:str ,ans:set ,invert_index:dict):
    temp_set = set([x for x, _ in invert_index[key_word]])
    return ans | temp_set

def NOT_func(key_word:str ,ans:set ,invert_index:dict):
    temp_set = set([x for x, _ in invert_index[key_word]])
    return ans - temp_set

def get_bool_filter() -> dict:
    query_filter_file_path = os.path.join(os.getcwd(), 'query.json')
    with open(query_filter_file_path, 'r', encoding='utf8') as fp:
        bool_filter = str(fp.read())
    bool_filter = json.loads(bool_filter)

    return bool_filter

def read_invert_index():
    path = os.path.join(os.getcwd(),'../invert_index.txt')
    with open(path,'r',encoding='utf8') as fp:
        invert_index_dict = eval(fp.read())
    return invert_index_dict

def main():
    global extra_and_dict
    ans = set()
    invert_index = read_invert_index()
    bool_filter = get_bool_filter()
    for operator, key_words in bool_filter.items():
        func= eval(operator+'_func')
        for key_word in key_words:
            ans = func(key_word,ans,invert_index)
    print(ans)
    print("优化AND排序之后，文章索引值为：")
    extra_and_dict = sorted(extra_and_dict.items(), key=lambda x: x[1], reverse=True)
    print(extra_and_dict)

if __name__ == '__main__':
    main()