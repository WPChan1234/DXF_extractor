from openpyxl import load_workbook
import tkinter.messagebox
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile

import ezdxf


Workbook_Link = askopenfilename( title='Select result summary file")')
print(Workbook_Link)

Workbook = load_workbook(filename=Workbook_Link)
print(Workbook.worksheets)

Sheet =  Workbook["Input 2"]

Column= Sheet['B']

first_row=2

