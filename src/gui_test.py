'''
Created on 2016/02/14

@author: master
'''
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout

class TestWidget(QWidget):

    def __init__(self, parent=None):
        # コンストラクタ
        QWidget.__init__(self, parent=parent)
        # 実際の生成コード
        self.setup_ui()

    def setup_ui(self):
        # QPushButtonのインスタンスを作る
        #self.start_button = QtGui.QPushButton("START", parent=self)
        #self.stop_button = QtGui.QPushButton("STOP", parent=self)
        self.reset_button = QPushButton("RESET", parent=self)
        self.quit_button = QPushButton("QUIT", parent=self)

        # Buttonをレイアウトマネージャに入れる
        layout = QGridLayout()
        #layout.addWidget(self.start_button, 0, 0)
        #layout.addWidget(self.stop_button, 0, 1)
        layout.addWidget(self.reset_button, 1, 0)
        layout.addWidget(self.quit_button, 1, 1)
        
        # レイアウトマネージャをWidgetに入れる
        self.setLayout(layout)


if __name__ == '__main__':
    
    w = TestWidget()
    w.show()
    
    pass

