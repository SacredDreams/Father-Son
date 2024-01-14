from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import *
import json

class Main(object):
    """窗口交互"""
    def __init__(self):
        # 加载ui文件
        self.main_ui = QUiLoader().load("ui/main.ui")
        self.discouses_ui = QUiLoader().load("ui/discouses.ui")
        self.moves_ui = QUiLoader().load("ui/moves.ui")
        self.settings_ui = QUiLoader().load("ui/settings.ui")

        self.message = None
        self.f_s_number = None
        self.vertical_scrollbar = 1000
        self.A_layout = QVBoxLayout()
        self.chat_history = []
        self.fun_list = [
            self.sendMessages, self.selectCommonDiscouses, self.sendMoves, self.selectChatObject, self.avatarsVideo
        ]
        self.main_ui_chat_pB = [
            self.main_ui.SendMessages, self.main_ui.CommonDiscouses, self.main_ui.SendMoves,
            self.main_ui.SelectChatObject, self.main_ui.AvatarsVideo
        ]
        self.main_ui_control_pB = [
            self.main_ui.ChangeSettings
        ]

        self.init_main_ui()

    def init_main_ui(self):
        """初始化窗口"""
        # 读取聊天历史记录文件，并添加到self.chat_history
        with open("History\\object_1.json", "r", encoding="utf-8") as file:
            history = json.load(file)
            self.chat_history.append(history)
        print("<self.chat_history>", self.chat_history)

        # 创建聊天记录滚动区域
        for key, value in self.chat_history[0].items():
            temp_dict = {
                "widget_0": self.set_QLabel_styles(text=self.deal_keys(key)),
                "widget_1": self.set_QLabel_styles(text=value, set_word_wrap=True, set_maximum_width=500),
                "item_0": QSpacerItem(0, 40, QSizePolicy.Expanding, QSizePolicy.Expanding)
            }
            self.A_layout.addLayout(  # 添加每一行的布局
                self.set_Layout(h_or_v="h", addition=temp_dict)
            )
        self.main_ui.scrollAreaWidget_ChatHistory.setLayout(self.A_layout)  # 将总布局应用到控件
        self.main_ui.ChatHistory.setWidget(self.main_ui.scrollAreaWidget_ChatHistory)
        spacer = QSpacerItem(QSizePolicy.Expanding, QSizePolicy.Minimum)
        # spacer.setOrientation(Qt.Vertical)
        self.A_layout.addItem(spacer)

        # 所有pushButton建立连接
        each_fun = 0
        for each_pB in range(0, len(self.main_ui_chat_pB)):
            self.main_ui_chat_pB[each_pB].clicked.connect(self.fun_list[each_fun])
            each_fun += 1

        # 设置编号问题
        self.f_s_number = int(len(self.chat_history[0]) / 2)

    def sendMessages(self):
        """发送消息给AI - 接收AI返回的消息"""
        # 获取文本框输入的文本
        self.message = self.main_ui.Messages.toPlainText()
        print("<sendMessages>", self.message)

        # 将“父亲”文本添加到聊天区
        temp_dict1 = {
            "widget_0": self.set_QLabel_styles(text="父亲"),
            "widget_1": self.set_QLabel_styles(text=self.message),
            "item_0": QSpacerItem(0, 40, QSizePolicy.Expanding, QSizePolicy.Expanding)
        }
        self.A_layout.addLayout(
            self.set_Layout(h_or_v="h", addition=temp_dict1)
        )

        # 发送消息后，清空文本框, 并将“父亲”文本添加到self.chat_history
        self.main_ui.Messages.clear()
        self.chat_history[0]["父亲$%s" % self.f_s_number] = self.message

        # 调用AI
        son_msg = "滚！！！！！！！！！！！！！！！"
        
        # 将“儿子”文本添加到聊天区
        temp_dict2 = {
            "widget_0": self.set_QLabel_styles(text="儿子"),
            "widget_1": self.set_QLabel_styles(text=son_msg),
            "item_0": QSpacerItem(0, 40, QSizePolicy.Expanding, QSizePolicy.Expanding)
        }
        self.A_layout.addLayout(
            self.set_Layout(h_or_v="h", addition=temp_dict2)
        )
        
        # 将“儿子”文本添加到self.chat_history
        self.chat_history[0]["儿子$%s" % self.f_s_number] = son_msg
        print("<self.chat_history>", self.chat_history)

        # 编号增加1
        self.f_s_number += 1

        # 写入文件，储存聊天信息
        with open("History\\object_1.json", "w", encoding="utf-8") as file:
            json.dump(self.chat_history[0], file, ensure_ascii=False)

    def selectCommonDiscouses(self):
        """选择常用语录并添加到聊天框内"""
        def insertText():
            cursor = QTextCursor(self.main_ui.Messages.document())
            cursor.insertText(self.discouses_ui.listWidget.currentItem().text())
            cursor = None
        self.discouses_ui.pushButton.clicked.connect(insertText)
        self.discouses_ui.show()

    def sendMoves(self):
        """选择动作并直接发送"""
        self.moves_ui.show()

    def selectChatObject(self):
        """选择聊天对象并切换"""
        pass

    def avatarsVideo(self):
        """启动/关闭虚拟形象"""
        pass

    @staticmethod
    def deal_keys(key):
        """
        用于处理父亲与儿子的编号问题
        :return “父亲”or“儿子”
        """
        temp_key = key.split("$")
        del temp_key[-1]
        return temp_key[0]

    @staticmethod
    def set_QLabel_styles(
            text="None", set_alignment=Qt.AlignTop, set_word_wrap=False, set_maximum_width=0
    ):
        """
        设置QLabel的样式
        :return 一个定义好样式的label
        """
        label = QLabel(text)
        if set_alignment: label.setAlignment(set_alignment)
        if set_word_wrap: label.setWordWrap(set_word_wrap)
        if set_maximum_width: label.setMaximumWidth(set_maximum_width)
        return label

    @staticmethod
    def set_Layout(
            h_or_v=None, addition=None
    ):
        """
        制作一个布局
        :return 一个添加了控件的布局
        """
        if h_or_v == "h": layout = QHBoxLayout()
        else: layout = QVBoxLayout()
        for key, value in addition.items():
            if "widget" in key: layout.addWidget(value)
            if "item" in key: layout.addItem(value)
        return layout

class Chatbots:
    """聊天机器人"""
    def __init__(self):
        pass

class Avatars:
    """虚拟形象"""
    def __init__(self):
        pass

if __name__ == '__main__':
    app = QApplication()
    run = Main()
    run.main_ui.show()
    app.exec_()
