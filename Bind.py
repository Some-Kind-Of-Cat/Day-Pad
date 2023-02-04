




import os
import re
import Visual
import tkinter
import datetime
from tkinter import ttk
from Behind import NoteDay
from inspect import getsourcefile





class Binder:
    noteDay = None
    visual = None
    configurationFile = os.path.dirname(getsourcefile(lambda:0)) + "/Configuration"


    def setUp(day, visual):
        Binder.noteDay = day
        Binder.visual = visual


    def addNote(newNote):
        Binder.noteDay.notes.append(newNote)

        NoteDay.saveDay(Binder.noteDay)

        Binder.visual.update(Binder.noteDay.date, Binder.noteDay.notes)


    def deleteNote(notePosition):
        del Binder.noteDay.notes[notePosition]

        NoteDay.saveDay(Binder.noteDay)

        Binder.visual.update(Binder.noteDay.date, Binder.noteDay.notes)


    def addNoteAndStart(newNote):
        Binder.addNote(newNote)

        Binder.visual.theWholeThing.noteArea.noteFrame.add.clicked.emit()


    def moveNoteUp(notePosition):
        if notePosition != 0:
            Binder.noteDay.notes[notePosition - 1], Binder.noteDay.notes[notePosition] = \
                Binder.noteDay.notes[notePosition], Binder.noteDay.notes[notePosition - 1]

            NoteDay.saveDay(Binder.noteDay)

            Binder.visual.update(Binder.noteDay.date, Binder.noteDay.notes)


    def moveNoteDown(notePosition):
        if notePosition < len(Binder.noteDay.notes) - 1:
            Binder.noteDay.notes[notePosition + 1], Binder.noteDay.notes[notePosition] = \
                Binder.noteDay.notes[notePosition], Binder.noteDay.notes[notePosition + 1]

            NoteDay.saveDay(Binder.noteDay)

            Binder.visual.update(Binder.noteDay.date, Binder.noteDay.notes)


    def editNote(notePosition, newNote):
        Binder.noteDay.notes[notePosition] = newNote

        NoteDay.saveDay(Binder.noteDay)

        Binder.visual.update(Binder.noteDay.date, Binder.noteDay.notes)


    def loadFile():
        item, okay = Binder.visual.savesDialog(os.listdir(NoteDay.saveFolder))

        if okay:
            NoteDay.saveFile = NoteDay.saveFolder + item
            Binder.loadDate(datetime.date.today())


    def createNewFile():
        name, okay = Binder.visual.newDialog()

        if okay:
            NoteDay.saveFile = NoteDay.saveFolder + name
            Binder.loadDate(datetime.date.today())


    def deleteFile():
        item, okay = Binder.visual.deletionDialog(os.listdir(NoteDay.saveFolder))

        if okay:
            NoteDay.deleteFile(item)

            Binder.loadDate(datetime.date.today())


    def defaultFile():
        item, okay = Binder.visual.defaultSettingDialog(NoteDay.getDefaultFile(),
            os.listdir(NoteDay.saveFolder))

        if okay:
            NoteDay.setDefaultFile(item)


    def loadDate(date):
        Binder.noteDay = NoteDay(date)

        Binder.visual.update(Binder.noteDay.date, Binder.noteDay.notes)


    def previousDay():
        Binder.loadDate(Binder.noteDay.date - datetime.timedelta(days = 1))


    def nextDay():
        Binder.loadDate(Binder.noteDay.date + datetime.timedelta(days = 1))


    def refreshGI():
        Binder.visual.update(Binder.noteDay.date, Binder.noteDay.notes)


    def getAConfiguration(configuration):
        rasp = open(Binder.configurationFile)
        lines = rasp.read()
        rasp.close()

        match = re.search(configuration + ': (.*?)[\n]', lines, re.DOTALL)
        return match.groups()[0]


    def setAConfiguration(configuration, value):
        rasp = open(Binder.configurationFile)
        lines = rasp.read()
        rasp.close()

        match = re.search(configuration + ': (.*?)[\n]', lines, re.DOTALL)
        lines = lines[0:match.start()] + configuration + ': ' + value + '\n' + lines[match.end():]

        rasp = open(NoteDay.configurationFile, "w")
        rasp.write(lines)
        rasp.close()




