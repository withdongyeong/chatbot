from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
import random

# user & chicken icon by Icon8(icons8.com)
from SpecChecker import getCondition
from toWeb import goDestination
from train import predict


class Messenger(QWidget):
    def __init__(self):
        super(Messenger, self).__init__()
        self.setParameter()
        self.setGUI()
        self.show()
        # when initialize, focus on chatbox
        self.chatbox.setFocus()

    def setParameter(self):
        self.roundProfileSize = 30
        self.chickenImage = QPixmap('img/icons8-chicken-30.png')
        self.userImage = QPixmap('img/icons8-user-30.png')

        self.customEncoding = {
            0 : '롤',
            1 : '오버워치',
            2 : '배틀그라운드',
            3 : '로스트아크'
        }
        self.requirements = {
            '롤':{
                '권장사양':{
                    'CPU':"intel i5-3300",
                    'GPU':"Geforce 560",
                    'RAM':"4GB"
                },
                '구매추천':{
                    'CPU': "intel i5-3300",
                    'GPU': "Geforce 560",
                    'RAM': "4GB"
                }
            },
            '오버워치':{
                '권장사양':{
                    'CPU': "intel i5",
                    'GPU': "Geforce 660",
                    'RAM': "6GB"
                },
                '구매추천': {
                    'CPU': "intel i5-3300",
                    'GPU': "Geforce 560",
                    'RAM': "4GB"
                }
            },
            '배틀그라운드':{
                '권장사양':{
                    'CPU': "intel i5-6600k",
                    'GPU': "Geforce GTX 1060 3GB",
                    'RAM': "16GB"
                },
                '구매추천': {
                    'CPU': "intel i5-3300",
                    'GPU': "Geforce 560",
                    'RAM': "4GB"
                }
            },
            '로스트아크':{
                '권장사양':{
                    'CPU': "intel i5",
                    'GPU': "Geforce RTX 2080",
                    'RAM': "16GB"
                },
                '구매추천': {
                    'CPU': "intel i5-3300",
                    'GPU': "Geforce 560",
                    'RAM': "4GB"
                }
            }
        }

    def setGUI(self):
        # set title
        self.setWindowTitle("다알아")

        # set basic size
        self.resize(400, 800)

        # set scroll box
        mainLayout = QVBoxLayout()
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        mainLayout.addWidget(self.scrollArea)

        # initialize scroll layout
        self.scrollLayout = QVBoxLayout()
        self.scrollLayout.setAlignment(Qt.AlignTop)

        # set chat layout
        self.chatLayout = QVBoxLayout()
        self.chatbox = QLineEdit()

        # event for enter
        self.chatbox.returnPressed.connect(self.enter)
        self.chatLayout.addWidget(self.chatbox)
        self.chatButtonLayout = QHBoxLayout()

        # mic button
        self.chatMicButton = QPushButton("Mic")
        self.chatMicButton.clicked.connect(self.mic)
        self.chatButtonLayout.addWidget(self.chatMicButton)

        # enter button
        self.chatEnterButton = QPushButton("Enter")
        self.chatEnterButton.clicked.connect(self.enter)
        self.chatButtonLayout.addWidget(self.chatEnterButton)

        self.chatLayout.addLayout(self.chatButtonLayout)
        mainLayout.addLayout(self.chatLayout)

        self.setLayout(mainLayout)

    def enter(self):
        text = self.chatbox.text()
        self.addMessageUser(text)
        self.callPredict(text)

    def mic(self):
        print("mic")

    def addMessageBot(self, text):
        self.makeMessageBox(text, "bot")

    def addMessageUser(self, text):
        self.makeMessageBox(text, "user")

    def makeMessageBox(self, text, type):
        # 1. make temp widget
        tempWidget = QWidget()

        # 2. get scroll layout
        scrollLayout = self.scrollLayout

        # 3. add text box to bottom of scroll layout
        textBoxLayout = QHBoxLayout()

        if type == "user":
            # user
            # set left spacer
            Spacer = QLabel()
            TextLabel = QLabel(text)
            TextLabel.setStyleSheet(
                "color: green;"  # text color
                "border-style: solid;"  # border line style
                "border-width: 2px;"  # border line width
                "border-color: green"  # border line color
            )
            roundLabel = QLabel()
            roundLabel.setPixmap(self.userImage)
            roundLabel.setMaximumHeight(self.roundProfileSize)
            roundLabel.setMaximumWidth(self.roundProfileSize)
            roundLabel.setStyleSheet(
                "border: 1px solid green;"
                "border-radius:  " + str(self.roundProfileSize / 2) + "px;"
            )
            textBoxLayout.addWidget(Spacer)
            textBoxLayout.addWidget(TextLabel)
            textBoxLayout.addWidget(roundLabel)
        else:
            # bot
            # set right spacer
            Spacer = QLabel()
            TextLabel = QLabel(text)
            TextLabel.setStyleSheet(
                "color: red;"  # text color
                "border-style: solid;"  # border line style
                "border-width: 2px;"  # border line width
                "border-color: red"  # border line color
            )
            roundLabel = QLabel()
            roundLabel.setPixmap(self.chickenImage)
            roundLabel.setMaximumHeight(self.roundProfileSize)
            roundLabel.setMaximumWidth(self.roundProfileSize)
            roundLabel.setStyleSheet(
                "border: 1px solid red;"
                "border-radius:  " + str(self.roundProfileSize / 2) + "px;"
            )
            textBoxLayout.addWidget(roundLabel)
            textBoxLayout.addWidget(TextLabel)
            textBoxLayout.addWidget(Spacer)


        TextLabel.setMinimumHeight(100)
        TextLabel.setMaximumHeight(100)
        scrollLayout.addLayout(textBoxLayout)

        # 4. update tempWidget
        tempWidget.setLayout(scrollLayout)

        # 5. set tempWidget to scrollArea
        self.scrollArea.setWidget(tempWidget)

        # 6. set scroll bar to bottom
        self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().maximum())

        # 7. clear chat box
        self.chatbox.setText("")

    def makeButtonBot(self, buttonList):
        # 1. make temp widget
        tempWidget = QWidget()

        # 2. get scroll layout
        scrollLayout = self.scrollLayout

        # 3. add push bottons to bottom of scroll layout
        buttonBoxLayout = QHBoxLayout()

        # set right spacer
        Spacer = QLabel()
        choiceBox = QWidget()
        choiceBoxLayout = QVBoxLayout()
        choiceBox.setStyleSheet(
            "color: red;"  # text color
            "border-style: solid;"  # border line style
            "border-width: 2px;"  # border line width
            "border-color: red"  # border line color
        )

        # make choice buttons
        choiceLayout = QVBoxLayout()
        for func, buttonName, label in buttonList:
            tempChoiceButton = QPushButton(buttonName)
            tempChoiceButton.clicked.connect(lambda: func(label))
            choiceLayout.addWidget(tempChoiceButton)
            tempChoiceButton.setMinimumHeight(30)
            tempChoiceButton.setStyleSheet(
                # base
                "QPushButton { color:red; border-radius: 5px; background-color: white}"
                # when pressed
                "QPushButton:pressed { background-color: #E7E7E7 }"
            )

        choiceBoxLayout.addLayout(choiceLayout)
        choiceBox.setLayout(choiceBoxLayout)
        roundLabel = QLabel()
        roundLabel.setPixmap(self.chickenImage)
        roundLabel.setMaximumHeight(self.roundProfileSize)
        roundLabel.setMaximumWidth(self.roundProfileSize)
        roundLabel.setStyleSheet(
            "border: 1px solid red;"
            "border-radius:  " + str(self.roundProfileSize / 2) + "px;"
        )
        buttonBoxLayout.addWidget(roundLabel)
        buttonBoxLayout.addWidget(choiceBox)
        buttonBoxLayout.addWidget(Spacer)

        scrollLayout.addLayout(buttonBoxLayout)

        # 4. update tempWidget
        tempWidget.setLayout(scrollLayout)

        # 5. set tempWidget to scrollArea
        self.scrollArea.setWidget(tempWidget)

        # 6. set scroll bar to bottom
        self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().maximum())

    def showRequirement(self, label):
        self.addMessageBot("권장사양은\n"
                           + "CPU : " + self.requirements[self.customEncoding[label]]['권장사양']['CPU'] + "\n"
                           + "GPU : " + self.requirements[self.customEncoding[label]]['권장사양']['GPU'] + "\n"
                           + "RAM : " + self.requirements[self.customEncoding[label]]['권장사양']['RAM'] + "이야")

    def callPredict(self, text):
        pr = predict(text, 0)
        if pr == 0:
            self.addMessageBot(self.customEncoding[pr] + " 컴퓨터 알려줄까?")
            self.addMessageBot("지금 사용중인 스펙은\n"
                               + getCondition() + "이네")
            self.showRequirement(pr)
            self.addMessageBot("다나와 권장 사양 링크 볼래?")
            buttonList = [
                (self.cpuLink, "CPU 추천", pr),
                (self.gpuLink, "GPU 추천", pr),
                (self.ramLink, "RAM 추천", pr)
            ]
            self.makeButtonBot(buttonList)
        elif pr == 1:
            self.addMessageBot(self.customEncoding[pr] + " 컴퓨터 알려줄까?")
            self.addMessageBot("지금 사용중인 스펙은\n"
                               + getCondition() + "이네")
            self.showRequirement(pr)
            self.addMessageBot("다나와 권장 사양 링크 볼래?")
            buttonList = [
                (self.cpuLink, "CPU 추천", pr),
                (self.gpuLink, "GPU 추천", pr),
                (self.ramLink, "RAM 추천", pr)
            ]
            self.makeButtonBot(buttonList)
        elif pr == 2:
            self.addMessageBot(self.customEncoding[pr] + " 컴퓨터 알려줄까?")
            self.addMessageBot("지금 사용중인 스펙은\n"
                               + getCondition() + "이네")
            self.showRequirement(pr)
            self.addMessageBot("다나와 권장 사양 링크 볼래?")
            buttonList = [
                (self.cpuLink, "CPU 추천", pr),
                (self.gpuLink, "GPU 추천", pr),
                (self.ramLink, "RAM 추천", pr)
            ]
            self.makeButtonBot(buttonList)
        elif pr == 3:
            self.addMessageBot(self.customEncoding[pr] + " 컴퓨터 알려줄까?")
            self.addMessageBot("지금 사용중인 스펙은\n"
                               + getCondition() + "이네")
            self.showRequirement(pr)
            self.addMessageBot("다나와 권장 사양 링크 볼래?")
            buttonList = [
                (self.cpuLink, "CPU 추천", pr),
                (self.gpuLink, "GPU 추천", pr),
                (self.ramLink, "RAM 추천", pr)
            ]
            self.makeButtonBot(buttonList)
        elif pr == 4:
            self.addMessageBot("고마워")
        elif pr == 5:
            self.addMessageBot("별 말씀을")
        elif pr == 6:
            self.addMessageBot("꺄하하")
        elif pr == 7:
            self.addMessageBot("재밌겠다")
        elif pr == 8:
            self.addMessageBot("너 이렇게 해야될 것 같은데")
        elif pr == 9:
            self.addMessageBot("알았어")
        elif pr == 10:
            self.addMessageBot("사실이야?")
        elif pr == 11:
            self.addMessageBot("다시 말해봐")
        elif pr == 12:
            self.addMessageBot("뭐라고 했어?")
        elif pr == 13:
            self.addMessageBot("뭐라고?")
        elif pr == 14:
            self.addMessageBot("오냐~")
        elif pr == 15:
            self.addMessageBot("알았다~")
        elif pr == 16:
            self.addMessageBot("안 들려~")
        else:
            self.addMessageBot("잘 가~")

    def cpuLink(self, pr):
        target = (self.requirements[self.customEncoding[pr]]['구매추천']['CPU'])
        print(self.requirements[self.customEncoding[pr]]['구매추천']['CPU'])
        goDestination(target)

    def gpuLink(self, pr):
        target = (self.requirements[self.customEncoding[pr]]['구매추천']['GPU'])
        print(self.requirements[self.customEncoding[pr]]['구매추천']['GPU'])
        goDestination(target)

    def ramLink(self, pr):
        target = (self.requirements[self.customEncoding[pr]]['구매추천']['RAM'])
        print(self.requirements[self.customEncoding[pr]]['구매추천']['RAM'])
        goDestination(target)

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    ex = Messenger()
    sys.exit(app.exec_())