import json
import os


def get_bool_filter():
    query_filter_file_path = os.path.join(os.getcwd(), 'query.json')
    with open(query_filter_file_path, 'r', encoding='utf8') as fp:
        bool_filter = str(fp.read())
    bool_filter = json.loads(bool_filter)
    return bool_filter



def main():
    bool_filter = get_bool_filter()
    print(bool_filter)
if __name__ == '__main__':
    main()