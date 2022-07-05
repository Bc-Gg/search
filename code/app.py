import sys
from PySide6.QtWidgets import (QLineEdit, QPushButton, QApplication,QVBoxLayout, QDialog,
                               QTextBrowser, QButtonGroup, QRadioButton)
from time import time
from bool_query import *

def init_path():
    base_path = os.path.abspath((os.path.join(os.getcwd(), '..')))
    output_path = os.path.join(base_path, 'query')
    if not os.path.exists(output_path):
        os.mkdir(output_path)

def reload_query_filter(and_word: str, or_word: str, not_word: str):
    ans = dict()
    ans['AND'] = and_word.split()
    ans['OR'] = or_word.split()
    ans['NOT'] = not_word.split()
    return ans

def load_file_name():
    base_path = os.path.abspath((os.path.join(os.getcwd(), '../..')))
    filePath = os.path.join(base_path, 'rawdata')
    return sorted(os.listdir(filePath))

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        # 创建组件
        self.resize(1000, 1000)
        self.select_num = -1
        self.AND_edit = QLineEdit("")
        self.OR_edit = QLineEdit("")
        self.NOT_edit = QLineEdit("")
        self.button = QPushButton("Show Me the ans")
        self.result = QTextBrowser()
        self.result.size()
        self.button1 = QRadioButton()
        self.button1.setText('10')
        self.button2 = QRadioButton()
        self.button2.setText('20')
        self.button3 = QRadioButton()
        self.button3.setText('50')
        self.button4 = QRadioButton()
        self.button4.setText('-1')
        self.buttongroup = QButtonGroup()
        self.buttongroup.addButton(self.button1, 1)
        self.buttongroup.addButton(self.button2, 2)
        self.buttongroup.addButton(self.button3, 3)
        self.buttongroup.addButton(self.button4, -1)
        # 创建布局并添加组件
        layout = QVBoxLayout()
        layout.addWidget(self.AND_edit)
        layout.addWidget(self.OR_edit)
        layout.addWidget(self.NOT_edit)
        layout.addWidget(self.button)
        layout.addWidget(self.result)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.addWidget(self.button4)
        # 应用布局
        self.setLayout(layout)
        # 连接query槽和按钮单击信号
        self.button.clicked.connect(self.query)
        # 连接buttongroup的单击信号
        self.buttongroup.buttonClicked.connect(self.change_select_num)
        # 读取数据成员
        self.invert_index = read_invert_index()
        self.filenames = load_file_name()

    def change_select_num(self, item):
        self.select_num = int(item.text())

    def get_length(self, a):
        if self.select_num == -1:
            return a
        return self.select_num
    def save_as_txt(self, words, ans):
        base_path = os.path.abspath((os.path.join(os.getcwd(), '..')))
        output_path = os.path.join(base_path, 'query')
        filename = ' '.join(words) + '.txt'
        filepath = os.path.join(output_path, filename)
        with open(filepath , 'w') as fp:
            for index,_ in ans:
                fp.write(self.filenames[index] + '\n')
    # 数据库查询
    def query(self):
        self.result.clear()
        extra_and_dict.clear()
        bool_filter = reload_query_filter(self.AND_edit.text(), self.OR_edit.text(), self.NOT_edit.text(), )
        t = time()
        ans, message = db_query(bool_filter, self.invert_index)
        self.result.append('query操作总共花费：' + str(round((time() - t), 5)*1000) + 'ms\n')
        if not message:
            self.result.append('查询失败，查无此词\n')
        else :
            self.result.append('查询成功！\n')
        generate_extra_dict(ans, bool_filter['AND'], self.invert_index)
        ans = list(ans)
        sorted_ans = list(sorted(extra_and_dict.items(), key=lambda x: x[1], reverse=True))
        ans_len = self.get_length(len(ans))
        ans, sorted_ans = ans[:ans_len], sorted_ans[:ans_len]
        self.result.append(str(ans_len)+'\n查询列表为：'+str(ans) + '\n排序后列表为：' + str(sorted_ans))
        self.save_as_txt(bool_filter['AND'], sorted_ans)



def main():
    init_path()
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
