import sys
from PySide6.QtWidgets import (QLineEdit, QPushButton, QApplication,
    QVBoxLayout, QDialog)

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        # 创建组件
        self.edit = QLineEdit("Write my name here")
        self.button = QPushButton("Show Greetings")
        # 创建布局并添加组件
        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.button)
        # 应用布局
        self.setLayout(layout)
        # 连接greetings槽和按钮单击信号
        self.button.clicked.connect(self.greetings)

    # 向用户打招呼
    def greetings(self):
        print(f"Hello {self.edit.text()}")

if __name__ == '__main__':
    # 创建Qt应用程序
    app = QApplication(sys.argv)
    # 创建并显示Form
    form = Form()
    form.show()
    # 运行Qt主循环
    sys.exit(app.exec())
