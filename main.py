from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
import random

# user & chicken icon by Icon8(icons8.com)

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
        self.addMessageUser(self.chatbox.text())
        self.predict(self.chatbox.text())

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

    def makeButtonBot(self):
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
        for i in range(1, random.randint(2,5)):
            tempChoiceButton = QPushButton("선택지"+ str(i))
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

    def predict(self, text):
        pr = random.randint(1,17)

        if pr == 1:
            self.addMessageBot("안녕?")
        elif pr == 2:
            self.addMessageBot("이렇게 해줄까?")
        elif pr == 3:
            self.addMessageBot("이건 어때?")
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


if __name__ == "__main__" :
    app = QApplication(sys.argv)
    ex = Messenger()
    sys.exit(app.exec_())