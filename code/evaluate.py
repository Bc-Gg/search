from bool_query import *


def main():
    def getone(tu):
        return tu[0]
    md = {'word':{(1,2),(3,4)}}
    ls = md['word']
    ll = set(map(getone, ls))
    print(ll)

if __name__ == '__main__':
    main()