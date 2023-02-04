




import re
import os
import datetime
from inspect import getsourcefile





""" The "day" parameter will be a type "date" object. """

class NoteDay():
    saveFolder = os.path.dirname(getsourcefile(lambda:0)) + '/Save Files/'
    configurationFile = os.path.dirname(getsourcefile(lambda:0)) + '/Configuration'
    saveFile = ''


    def __init__(ins, date):
        ins.date = date
        ins.notes = NoteDay.loadNotes(date)


    """ The "date" parameter will be a "datetime.date" object. """

    def loadNotes(date):
        try:
            rasp = open(NoteDay.saveFile, "r")
            ee = rasp.read()
            rasp.close()
        except:
            open(NoteDay.saveFile, 'x')
            ee = ''

        stick = re.search("<" + str(date) + ">(.*?)<" + str(date) + ">", ee, re.DOTALL)

        if stick == None:
            return []
        else:
            return re.findall('<Note/>(.*?)</Note>', stick.groups()[0], re.DOTALL)


    """ The "day" parameter is a "Day" object. """

    def saveDay(noteDay):
        rasp = open(NoteDay.saveFile, "r")
        ee = rasp.read()
        rasp.close()

        label = str(noteDay.date)
        stick = re.search("<" + label + ">(.*?)<" + label + ">", ee, re.DOTALL)

        delimetedNotes = ['<Note/>' + al + '</Note>' for al in noteDay.notes]
        newString = "<" + label + ">\n" + "\n".join(delimetedNotes) + "\n<" + label + ">"

        if stick == None:
            ee += ("\n" + newString)
        else:
            ee = ee[0:stick.start()] + newString + ee[stick.end():]

        rasp = open(NoteDay.saveFile, "w")
        rasp.write(ee)
        rasp.close()


    def deleteFile(fileName):
        os.remove(NoteDay.saveFolder + fileName)

        if fileName == NoteDay.saveFile:
            NoteDay.saveFile = 'Record'


    def getDefaultFile():
        rasp = open(NoteDay.configurationFile)
        lines = rasp.read()
        rasp.close()

        match = re.search('default file: (.*?)[\n]', lines, re.DOTALL)
        return match.groups()[0]


    def setDefaultFile(fileName):
        rasp = open(NoteDay.configurationFile)
        lines = rasp.read()
        rasp.close()

        match = re.search('default file: (.*?)[\n]', lines, re.DOTALL)
        lines = lines[0:match.start()] + 'default file: ' + fileName + \
            '\n' + lines[match.end():]

        rasp = open(NoteDay.configurationFile, "w")
        rasp.write(lines)
        rasp.close()








