import collections
import tkinter.messagebox
from tkinter.filedialog import askopenfilename
from tkinter import filedialog, Tk
from tkinter.filedialog import asksaveasfile
import pandas as pd

import ezdxf


# Procedure
# Select DXF
# Extract all NSR info into pandas
# Group info by Tower, Unit
# identify NSR with smallest x and then y
#calculate distance from the smallest x and y
# sort within group and rank
# Name = Tower + Unit + Rank
# write back into dxf by matching coordinate



tkinter.messagebox.showinfo('Rec info extraction: Introduction', 'Convert DXF REC block to Rec info')

docPath = askopenfilename(title='Select DXF File with "REC" Blocks only ------------------(MIN 2 REC BLOCKS!!)')
doc = ezdxf.readfile(docPath)


msp = doc.modelspace()
List = []
RecList = []
RecFile = []
ListFile = ["RecID, Room, Tower, Unit, Window"]

RecFile.append("TEXT \nREC \n")



# NSR duplicacy check#

for insert in msp.query('INSERT'):

    List = [(attrib.dxf.tag, attrib.dxf.text) for attrib in insert.attribs]
    if any("NSR_ID" in s for s in List):  ### Filter applied to search NSR blocks only ###
        RecID = List[7][1]
        RecList.append(RecID)

Duplicated_NSR = [item for item, count in collections.Counter(RecList).items() if count > 1]

tkinter.messagebox.showinfo("NSR Duplicate Check", "Duplicated NSR "
                                                   "(Gd to go if no duplicated NSRs) = " + str(Duplicated_NSR))

# Rec file formation#
NSR=[]
for insert in msp.query('INSERT'):

    List = [(attrib.dxf.tag, attrib.dxf.text) for attrib in insert.attribs]
    if any("NSR_ID" in s for s in List):  ### Filter applied to search NSR blocks only ###
        print(List)


        RecID = List[7][1]
        OPXY = List[0][1].replace('"', '')
        OPX = round(float(OPXY.split(",")[0]), 1)
        OPY = round(float(OPXY.split(",")[1]), 1)
        Unit = str(List[4][1])
        Tower = str(List[6][1])



        Current_NSR = {"RecID": RecID,
                       "Tower": Tower,
                       "X": OPX,
                       "Y": OPY,
                        "Unit": Unit

                       }

        NSR.append(Current_NSR)



Df_NSR = pd.DataFrame(NSR)







root = Tk()  # this is to close the dialogue box later
try:
    # with block automatically closes file
    with filedialog.asksaveasfile(mode='w', defaultextension=".xlsx",title='Save Rec Detail file as',initialfile="Receiver info list.xlsx") as file:
        Df_NSR.to_excel(file.name)
except AttributeError:
    # if user cancels save, filedialog returns None rather than a file object, and the 'with' will raise an error
    print("The user cancelled save")

root.destroy()

tkinter.messagebox.showinfo('End','NSR ID successfully exported in .xlsx file.')



#Df_NSR.to_excel(f)