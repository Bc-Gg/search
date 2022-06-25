import json
import sys
from PySide6.QtWidgets import (QLineEdit, QPushButton, QApplication,
    QVBoxLayout, QDialog, QTextBrowser)
extra_and_dict:dict = {}
from bool_query import *
class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        # 创建组件
        self.AND_edit = QLineEdit("")
        self.OR_edit = QLineEdit("")
        self.NOT_edit = QLineEdit("")
        self.button = QPushButton("Show Me the ans")
        self.result = QTextBrowser()
        # 创建布局并添加组件
        layout = QVBoxLayout()
        layout.addWidget(self.AND_edit)
        layout.addWidget(self.OR_edit)
        layout.addWidget(self.NOT_edit)
        layout.addWidget(self.button)
        layout.addWidget(self.result)
        # 应用布局
        self.setLayout(layout)
        # 连接greetings槽和按钮单击信号
        self.button.clicked.connect(self.query)
        # 数据成员
        self.invert_index = read_invert_index()
        print(self.invert_index)

    def reload_query_filter(self,and_word:str, or_word:str, not_word:str):
        ans = dict()
        ans['AND'] = and_word.split()
        ans['OR'] = or_word.split()
        ans['NOT'] = not_word.split()
        return ans

    # 向用户打招呼
    def query(self):
        self.result.clear()
        extra_and_dict.clear()
        bool_filter = self.reload_query_filter(self.AND_edit.text(),self.OR_edit.text(),self.NOT_edit.text(),)
        from time import time
        t = time()
        ans ,sorted_ans = db_query(bool_filter,self.invert_index)
        self.result.append('query操作总共花费：'+str(round((time() - t),5))+'s\n')
        self.result.append(str(ans)+'\n'+str(sorted_ans))


def main():
    global extra_and_dict

    app = QApplication(sys.argv)
    form = Form()
    form.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()
