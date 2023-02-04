




""" Whenever something is changed in "Day Pad", the save happens immediately. """





import os
import Behind
import Visual
from Bind import Binder
import datetime
from inspect import getsourcefile
from PyQt5.QtWidgets import QApplication





Behind.NoteDay.saveFile = Behind.NoteDay.saveFolder + Behind.NoteDay.getDefaultFile()

noteDay = Behind.NoteDay(datetime.date.today())

someKindOfWeirdThing = QApplication([])

box = Visual.Visual(noteDay.date, noteDay.notes)

Binder.setUp(noteDay, box)



someKindOfWeirdThing.exec()




