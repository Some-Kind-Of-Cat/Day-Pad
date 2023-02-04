




import os
import datetime
from Bind import Binder
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from inspect import getsourcefile





class Visual(QMainWindow):
    styleSheetPath =  os.path.dirname(getsourcefile(lambda:0)) + "/Style Sheets/"
    iconPath = os.path.dirname(getsourcefile(lambda:0)) + "/Other/Dates.png"
    visualMode = ''



    def __init__(ins, day, notes):
        super().__init__()

        ins.orientWindow()

        ins.theWholeThing = CentralWidget(ins, day, notes)

        ins.setUpMenuBar()

        ins.setFocus()


    def orientWindow(ins):
        Visual.visualMode = Binder.getAConfiguration('Visual Mode')
        ins.setStyleSheet(ins.getStyleSheet())
        ins.setWindowTitle("Day Pad ^_^")
        ins.setWindowIcon(QIcon(Visual.iconPath))

        screen = QApplication.desktop().screen().rect()
        ins.setGeometry(0, 0, int(screen.width() * 0.8), int(screen.height() * 0.8))
        centerOffset = screen.center() - ins.rect().center()
        ins.move(centerOffset)

        ins.show()


    def setUpMenuBar(ins):
        ins.qMenuBar = ins.menuBar()
        ins.fileMenu = ins.qMenuBar.addMenu('File')
        ins.fileMenu.addAction('New Pad', Binder.createNewFile)
        ins.fileMenu.addAction('Load Pad', Binder.loadFile)
        ins.fileMenu.addAction('Delete Pad', Binder.deleteFile)
        ins.fileMenu.addAction('Set the Default Pad', Binder.defaultFile)

        ins.lookMenu = ins.qMenuBar.addMenu('Change Look')
        ins.lookMenu.addAction('Normal', lambda: ins.changeStyleSheet('Normal Sheet'))
        ins.lookMenu.addAction('Dark Mode', lambda: ins.changeStyleSheet('Dark Sheet'))


    def update(ins, day, notes):
        ins.theWholeThing.update(day, notes)


    def getStyleSheet(ins):
        path = Visual.styleSheetPath + Binder.getAConfiguration('Visual Mode')
        label = open(path)
        rasp = label.read()
        label.close()
        return rasp


    def changeStyleSheet(ins, newOne):
        Binder.setAConfiguration('Visual Mode', newOne)
        Visual.visualMode = Binder.getAConfiguration('Visual Mode')
        ins.setStyleSheet(ins.getStyleSheet())


    def savesDialog(ins, list):
        return QInputDialog.getItem(ins, 'Pads', 'Which pad would you like to load?',
            list, editable = False)


    def newDialog(ins):
        return QInputDialog.getText(ins, 'New Pad',
            'What would you like the name of your new day pad to be?')


    def deletionDialog(ins, list):
        return QInputDialog.getItem(ins, 'Pads', 'Which pad do you need to delete?',
            list, editable = False)


    def defaultSettingDialog(ins, current, list):
        return QInputDialog.getItem(ins, 'Default Pad',
            'Which pad would you like to be the defaut (the current default is '+ current + ')?',
            list, editable = False)


    def keyPressEvent(ins, qEvent):
        keyEventDictionary = {Qt.Key_Right: Binder.nextDay,
            Qt.Key_Left: Binder.previousDay}

        if qEvent.key() in keyEventDictionary:
            keyEventDictionary[qEvent.key()]()





class CentralWidget(QWidget):
    def __init__(ins, container, day, notes):
        super().__init__()

        ins.orientWindow(container)

        ins.update(day, notes)

        ins.setFocus()


    def keyPressEvent(ins, qEvent):
        qEvent.ignore()


    def orientWindow(ins, container):
        container.setCentralWidget(ins)
        ins.layout = QGridLayout(); ins.setLayout(ins.layout)


    def update(ins, day, notes):
        ins.removeWidgets()

        ins.date = DateLabel(day, ins)

        ins.changeDate = DateChangeButton(ins)

        ins.noteArea = ScrollContainer(ins, notes)


    def removeWidgets(ins):
        for al in ['date', 'changeDate', 'noteArea', 'dateEntry']:
            if hasattr(ins, al):
                ins.layout.removeWidget(getattr(ins, al))
                getattr(ins, al).hide()
                delattr(ins, al)
        NoteWidget.noteWidgets = []





class DateChangeButton(QFrame):
    def __init__(ins, container):
        super().__init__()


        ins.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))


        ins.layout = QGridLayout(); ins.setLayout(ins.layout)


        ins.leftArrow = QPushButton("<")
        ins.leftArrow.setMaximumWidth(20)
        ins.leftArrow.clicked.connect(Binder.previousDay)
        ins.layout.addWidget(ins.leftArrow, 0, 0)
        ins.leftArrow.setObjectName('dateButton')


        ins.rightArrow = QPushButton(">")
        ins.rightArrow.setMaximumWidth(20)
        ins.rightArrow.clicked.connect(Binder.nextDay)
        ins.layout.addWidget(ins.rightArrow, 0, 2)
        ins.rightArrow.setObjectName('dateButton')


        ins.button = QPushButton("Choose A Date ^_^")
        ins.button.clicked.connect(lambda:
            setattr(container, 'dateEntry', DateEntry(container)))
        ins.layout.addWidget(ins.button, 0, 1)
        ins.button.setObjectName('dateButton')


        container.layout.addWidget(ins, 0, 0, 1, 3, Qt.AlignCenter)

    def keyPressEvent(ins, event):
        event.ignore()





class DateEntry(QFrame):
    def __init__(ins, container):
        super().__init__()

        ins.setMaximumWidth(500)
        ins.setMaximumHeight(250)

        container.layout.removeWidget(container.changeDate); container.changeDate.hide()
        del container.changeDate

        ins.setUpWidgets()

        container.layout.addWidget(ins, 0, 0, 1, 3, Qt.AlignCenter)


    def keyPressEvent(ins, event):
        event.ignore()



    def setUpWidgets(ins):
        ins.layout = QGridLayout(); ins.setLayout(ins.layout)

        ins.calendar = QCalendarWidget()

        ins.layout.addWidget(ins.calendar, 0, 0, 1, 2)

        ins.cancel = QPushButton("Cancel")
        ins.cancel.clicked.connect(Binder.refreshGI)
        ins.layout.addWidget(ins.cancel, 1, 0)

        ins.confirmation = QPushButton("Okay")
        ins.confirmation.clicked.connect(lambda: Binder.loadDate(
            ins.calendar.selectedDate().toPyDate()))
        ins.layout.addWidget(ins.confirmation, 1, 1)





class DateLabel(QLabel):
    suffixes = {1: "st", 2: "nd", 3: 'rd', 21: 'st', 22: 'nd', 23: 'rd', 31: 'st'}


    def __init__(ins, theDate, container):
        super().__init__(theDate.strftime("%B " + DateLabel.stringDay(theDate) + ", %Y"))

        ins.setAlignment(Qt.AlignCenter)

        container.layout.addWidget(ins, 1, 0, 1, 3)


    def keyPressEvent(ins, event):
        event.ignore()


    def stringDay(aDate):
        day = aDate.day

        if day in DateLabel.suffixes:
            return str(day) + DateLabel.suffixes[day]
        else:
            return str(day) + 'th'





class ScrollContainer(QScrollArea):
    def __init__(ins, container, notes):
        super().__init__()

        ins.arraySheet(notes)

        ins.setUpScrollBar()

        for al in [0, 2]: container.layout.setColumnStretch(al, 1)

        container.layout.setColumnStretch(1, 3)
        container.layout.addWidget(ins, 2, 1)


    def keyPressEvent(ins, event):
        event.ignore()


    def arraySheet(ins, notes):
        ins.layout = QVBoxLayout(); ins.setLayout(ins.layout)
        ins.noteFrame = NoteFrame(ins, notes)


    def setUpScrollBar(ins):
        ins.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        ins.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        ins.setWidgetResizable(True)
        ins.setWidget(ins.noteFrame)





class NoteFrame(QFrame):
    def __init__(ins, container, notes):
        super().__init__()

        ins.layout = QGridLayout(); ins.setLayout(ins.layout)


        for ee in notes:
            NoteWidget(ins, ee)
        ins.add = AddButton(ins)

        container.layout.addWidget(ins)


    def keyPressEvent(ins, event):
        event.ignore()





class AddButton(QPushButton):
    def __init__(ins, container):
        super().__init__("+")

        ins.setUpButton()

        ins.clicked.connect(lambda: NoteEntry(container, len(NoteWidget.noteWidgets),
            lambda: Binder.addNote(container.entry.text.document().toPlainText())))


        innerLayout = QVBoxLayout()

        container.layout.addLayout(innerLayout, len(NoteWidget.noteWidgets), 0, 1, 0,
            Qt.AlignTop | Qt.AlignHCenter)
        innerLayout.addItem(QSpacerItem(0, 13))
        innerLayout.addWidget(ins)



    def keyPressEvent(ins, event):
        event.ignore()


    def setUpButton(ins):
        ins.setMinimumWidth(30)
        ins.setMaximumWidth(30)
        ins.setMinimumHeight(30)
        ins.setMaximumHeight(30)





class NoteWidget(QTextBrowser):
    noteWidgets = [] # To keep track of the current "NoteWidget" objects.
    clicked = pyqtSignal(Qt.MouseButton)
    minimumHeight = 60
    width = 250


    def __init__(ins, container, note):
        super().__init__()

        ins.setMaximumWidth(NoteWidget.width)
        ins.setMinimumWidth(NoteWidget.width)

        ins.sizePolicy().setVerticalPolicy(QSizePolicy.Maximum)

        ins.insertPlainText(note)

        height = ins.calculateHeight(note)
        ins.setMinimumHeight(height)
        ins.setMaximumHeight(height)

        ins.setReadOnly(True)

        ins.position = len(NoteWidget.noteWidgets); NoteWidget.noteWidgets.append(ins)

        ins.clicked.connect(lambda: NoteEditWidget(container, ins, note, ins.position))


        ins.outerFrame = QFrame()
        ins.outerFrame.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        ins.outerFrame.layout = QGridLayout()
        ins.outerFrame.setLayout(ins.outerFrame.layout)
        ins.outerFrame.layout.addWidget(ins, 0, 0, 1, 1, Qt.AlignHCenter)

        container.layout.addWidget(
            ins.outerFrame, ins.position, 0, 1, 1, Qt.AlignHCenter)

        ins.setCursor(Qt.ArrowCursor)


    def keyPressEvent(ins, event):
        event.ignore()


    def mousePressEvent(ins, event):
        if Visual.visualMode == 'Dark Mode':
            ins.setStyleSheet("NoteWidget { background-color: #202055 }")
        else:
            ins.setStyleSheet("NoteWidget { background-color: #C0C0FF }")


    def mouseReleaseEvent(ins, event):
        ins.clicked.emit(event.button())


    def calculateHeight(ins, note):
        qRect = ins.fontMetrics().boundingRect(
            0, 0, NoteWidget.width, 10000000, Qt.TextWrapAnywhere, note)

        return max(NoteWidget.minimumHeight, qRect.height() + 10)





class NoteEditWidget(QFrame):
    def __init__(ins, container, noteWidget, note, position):
        super().__init__()

        container.noteEdit = ins

        ins.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        container.layout.itemAtPosition(position, 0).widget().hide()
        container.add.setEnabled(False)

        ins.layout = QGridLayout(); ins.setLayout(ins.layout)

        ins.setUpWidgets(container, noteWidget, note, position)

        container.layout.addWidget(ins, position, 0, 1, 1, Qt.AlignHCenter)

        ins.text.setFocus()


    def keyPressEvent(ins, event):
        event.ignore()


    def setUpMoveUp(ins, position):
        ins.moveUp = RoundButton("↑", lambda: Binder.moveNoteUp(position))
        ins.layout.addWidget(ins.moveUp, 0, 0, 1, 1, Qt.AlignHCenter)


    def setUpMoveDown(ins, position):
        ins.moveDown = RoundButton("↓", lambda: Binder.moveNoteDown(position))
        ins.layout.addWidget(ins.moveDown, 0, 1, 1, 1, Qt.AlignHCenter)


    def setUpDelete(ins, position):
        ins.delete = RoundButton("x", lambda: Binder.deleteNote(position))
        ins.layout.addWidget(ins.delete, 0, 4, 1, 1, Qt.AlignHCenter)



    def setUpConfirmation(ins, layout, note, position):
        ins.confirmation = QPushButton("✓")
        ins.confirmation.clicked.connect(lambda: Binder.editNote(position,
            ins.text.document().toPlainText()))
        layout.addWidget(ins.confirmation)


    def setUpCancellation(ins, layout):
        ins.cancel = QPushButton("x")
        ins.cancel.clicked.connect(Binder.refreshGI)
        layout.addWidget(ins.cancel)


    def setUpWidgets(ins, container, noteWidget, note, position):
        ins.text = NoteEditText(ins, noteWidget, note)
        ins.setUpMoveUp(position)
        ins.setUpMoveDown(position)
        ins.setUpDelete(position)
        ins.layout.addItem(QSpacerItem(36, 0), 0, 3)


        ins.innerLayout = QHBoxLayout();
        ins.layout.addLayout(ins.innerLayout, 1, 2)


        ins.setUpCancellation(ins.innerLayout)
        ins.setUpConfirmation(ins.innerLayout, note, position)





class RoundButton(QPushButton):
    def __init__(ins, text, function):
        super().__init__(text)

        ins.setMinimumWidth(30)
        ins.setMaximumWidth(30)
        ins.setMinimumHeight(30)
        ins.setMaximumHeight(30)

        ins.clicked.connect(function)


    def keyPressEvent(ins, qEvent):
        qEvent.ignore()





class NoteEditText(QTextEdit):
    def __init__(ins, container, noteWidget, note):
        super().__init__()

        ins.container = container

        ins.setStyleSheet("font-style: italic")
        ins.setMinimumWidth(NoteWidget.width)
        ins.setMaximumWidth(NoteWidget.width)
        ins.setMaximumHeight(noteWidget.height())
        ins.setMinimumHeight(noteWidget.height())

        ins.insertPlainText(note)
        ins.container.layout.addWidget(ins, 0, 2, 1, 1, Qt.AlignHCenter)


    def  keyPressEvent(ins, qEvent):
        if qEvent.key() == Qt.Key_Return and qEvent.modifiers() != Qt.ShiftModifier:
            ins.container.confirmation.clicked.emit()
        else:
            super().keyPressEvent(qEvent)





class NoteEntry(QFrame):
    def __init__(ins, container, position, function):
        super().__init__()

        container.entry = ins

        ins.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

        ins.layout = QGridLayout(); ins.setLayout(ins.layout)

        ins.setUpWidgets(function)

        ins.switchWidgets(container, position)

        ins.text.setFocus()


    def keyPressEvent(ins, event):
        event.ignore()


    def setUpConfirmation(ins, layout, function):
        ins.confirmation = QPushButton("✓")
        ins.confirmation.clicked.connect(function)
        layout.addWidget(ins.confirmation)


    def setUpCancellation(ins, layout):
        ins.cancel = QPushButton("x")
        ins.cancel.clicked.connect(Binder.refreshGI)
        layout.addWidget(ins.cancel)


    def setUpWidgets(ins, function):
        ins.text = NoteEntryText(ins)
        ins.innerLayout = QHBoxLayout()
        ins.layout.addLayout(ins.innerLayout, 1, 0)
        ins.setUpCancellation(ins.innerLayout)
        ins.setUpConfirmation(ins.innerLayout, function)



    def switchWidgets(ins, container, position):
        toRemove = container.layout.itemAtPosition(position, 0).widget()
        container.layout.removeItem(toRemove)
        container.layout.addWidget(ins, position, 0, 1, 1, Qt.AlignHCenter | Qt.AlignTop)





class NoteEntryText(QPlainTextEdit):
    def __init__(ins, container):
        super().__init__()

        ins.setStyleSheet("font-style: italic")

        ins.container = container

        ins.setMaximumWidth(NoteWidget.width)
        ins.setMinimumWidth(NoteWidget.width)
        ins.setMaximumHeight(NoteWidget.minimumHeight)
        ins.setMinimumHeight(NoteWidget.minimumHeight)

        container.layout.addWidget(ins, 0, 0, 1, 1, Qt.AlignCenter)


    def keyPressEvent(ins, qEvent):
        if qEvent.key() == Qt.Key_Return and qEvent.modifiers() != Qt.ShiftModifier:
            Binder.addNoteAndStart(ins.document().toPlainText())
        else:
            super().keyPressEvent(qEvent)




