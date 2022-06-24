import json
import os


def AND_func():
    pass

def OR_func():
    pass

def NOT_func():
    pass

def get_bool_filter() -> dict:
    query_filter_file_path = os.path.join(os.getcwd(), 'query.json')
    with open(query_filter_file_path, 'r', encoding='utf8') as fp:
        bool_filter = str(fp.read())
    bool_filter = json.loads(bool_filter)
    return bool_filter

def read_invert_index():
    with open(r'/Users/liubenchen/Desktop/文献检索/search/invert_index.json','r',encoding='utf8') as fp:
        pass

def main():
    ans = []
    invert_index = read_invert_index()
    bool_filter = get_bool_filter()
    print(bool_filter)
    for operator, key_words in bool_filter.items():
        func = eval(operator+'_func')
        for key_word in key_words:
            func(key_word,ans)
    print(ans)

if __name__ == '__main__':
    main()