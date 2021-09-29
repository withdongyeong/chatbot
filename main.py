import os

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
                    'CPU': "intel i5-9400f",
                    'GPU': "Geforce gtx 1660 ti",
                    'RAM': "DDR4-3200 8GB"
                }
            },
            '오버워치':{
                '권장사양':{
                    'CPU': "intel i5",
                    'GPU': "Geforce 660",
                    'RAM': "6GB"
                },
                '구매추천': {
                    'CPU': "intel i5-9400f",
                    'GPU': "Geforce gtx 1660 ti",
                    'RAM': "DDR4-3200 8GB"
                }
            },
            '배틀그라운드':{
                '권장사양':{
                    'CPU': "intel i5-6600k",
                    'GPU': "Geforce GTX 1060 3GB",
                    'RAM': "16GB"
                },
                '구매추천': {
                    'CPU': "intel i7-8700k",
                    'GPU': "Geforce RTX 2060",
                    'RAM': "DDR4-3200 8GB"
                }
            },
            '로스트아크':{
                '권장사양':{
                    'CPU': "intel i5",
                    'GPU': "Geforce RTX 2080",
                    'RAM': "16GB"
                },
                '구매추천': {
                    'CPU': "intel i7-8700k",
                    'GPU': "Geforce RTX 2080",
                    'RAM': "DDR4-3200 8GB"
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

        # enter button
        self.chatEnterButton = QPushButton("Enter")
        self.chatEnterButton.clicked.connect(self.enter)
        self.chatButtonLayout.addWidget(self.chatEnterButton)

        self.chatLayout.addLayout(self.chatButtonLayout)
        mainLayout.addLayout(self.chatLayout)

        self.setLayout(mainLayout)

        # hi
        self.hi()

    def hi(self):
        case = random.randint(0, 2)
        if case == 0:
            self.addMessageBot("안녕, 게임 컴퓨터 견적 알려주는 다알아라고해\n어떤 걸 알려줄까?")
        elif case == 1:
            self.addMessageBot("반가워, 게임 컴퓨터 견적 알려주는 다알아야\n뭐가 궁금해?")
        elif case == 2:
            self.addMessageBot("환영해, 게임 컴퓨터 견적 알려주는 다알아야\n무엇을 알려줄까?")

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
            tempChoiceButton.clicked.connect(func(label))
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

    def writeMisunderstandings(self, target):
        dir = "./unk"
        if not os.path.isdir(dir):
            os.mkdir(dir)
        # 파일 읽기
        fname = dir + os.sep + "misunderstandings.txt"
        f = open(fname, 'a+', encoding='UTF-8')
        text = ""
        while True:
            line = f.readline()
            if not line:
                break
            text += line

        # 맨 마지막 줄에 추가하기
        text += target + "\n"
        f.writelines(text)
        f.close()

    def callPredict(self, text):
        pr, score = predict(text, 0)
        if score < 0.95:
            case = random.randint(1, 3)
            if case == 1:
                self.addMessageBot("미안해 잘 모르겠어")
            elif case == 2:
                self.addMessageBot("다시 말해줄래?")
            else:
                self.addMessageBot("이해 못 했어")
            # 기록하기
            self.writeMisunderstandings(text)
            return
        
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
        else:
            self.addMessageBot("고려하지 않은 분석이야, 확인해봐")

    def cpuLink(self, pr):
        # 이렇게 만든 이유는, 버튼마다 다른 argument를 전달하고 싶은데
        # 버튼을 생성할 때, 함수를 connect하는 순간 작업(링크 띄우는일)을 하지 않도록 하기 위함
        def workCPU():
            target = (self.requirements[self.customEncoding[pr]]['구매추천']['CPU'])
            print(self.requirements[self.customEncoding[pr]]['구매추천']['CPU'])
            goDestination(target)
        return workCPU

    def gpuLink(self, pr):
        def workGPU():
            target = (self.requirements[self.customEncoding[pr]]['구매추천']['GPU'])
            print(self.requirements[self.customEncoding[pr]]['구매추천']['GPU'])
            goDestination(target)
        return workGPU

    def ramLink(self, pr):
        def workRAM():
            target = (self.requirements[self.customEncoding[pr]]['구매추천']['RAM'])
            print(self.requirements[self.customEncoding[pr]]['구매추천']['RAM'])
            goDestination(target)
        return workRAM

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    ex = Messenger()
    sys.exit(app.exec_())