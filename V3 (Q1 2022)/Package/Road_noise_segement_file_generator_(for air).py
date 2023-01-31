from tkinter.filedialog import askopenfilename
from tkinter import filedialog, Tk
from tkinter.filedialog import asksaveasfile
import ezdxf
import tkinter.messagebox
import collections
import pandas as pd
import openpyxl

## Road segment extractor for air
## Flow ID can be with characters

tkinter.messagebox.showinfo('DXF 2 Segment list: Introduction', 'Convert line segment to segment list' )

docPath = askopenfilename(title='Select DXF File with "Railway Segement" Blocks only ------------------(MIN 2 BLOCKS!!)')
doc = ezdxf.readfile(docPath)
print(docPath)


msp = doc.modelspace()
List = []
SegList=[]
SegFile=[]
ListFile=["SegID,S-X,S-Y,S-Z,E-X,E-Y,E-Z,Speed_kph,Half RD Wid"]

SegFile.append("TEXT")
SegFile.append("SegFile")
SegFile.append("")

# NSR duplicacy check#

for insert in msp.query('INSERT'):
            List = [(attrib.dxf.tag, attrib.dxf.text) for attrib in insert.attribs]
            if any("RD_SEG_ID" in s for s in List): ### Filter applied to search Segment blocks only ###
                SEG_ID = List[0][1]
                SegList.append(SEG_ID)



print(SegList)

Duplicated_SEG = [item for item, count in collections.Counter(SegList).items() if count > 1]


tkinter.messagebox.showinfo("Segment Duplicate Check","Duplicated SEG_ID "
                                                  "(Gd to go if no duplicated SEG_ID) = "+ str(Duplicated_SEG))

Content=[]

# SEG file formation#
for insert in msp.query('INSERT'):


            List = [(attrib.dxf.tag, attrib.dxf.text) for attrib in insert.attribs]
            if any("RD_SEG_ID" in s for s in List):### Filter applied to search NSR blocks only ###
                print(List)

                SEG_ID = List[0][1]

                S_OPXY  = List[4][1].replace('"', '')
                E_OPXY = List[5][1].replace('"', '')
                S_Z = List[1][1]
                E_Z = List[2][1]
                Road_Type=List[6][1]
                Rd_Width=float(List[7][1])
                FlowID=List[3][1]

                # ## LNRS
                # if List[6][1] =="Y":
                #   LNRS = str(2.0)
                # else: LNRS=str(1.0)
                #
                # First_eff_bar ="{:>8}".format("-"+str(round(float(List[7][1]),1)))
                #
                # while S_OPXY == '##################': ## error message for corrupted SEG block
                #     tkinter.messagebox.showinfo("Error","SEG block corrupted, rebuild coor. attribute")
                #     break
                #
                #     exit

                S_OPX = str(round(float(S_OPXY.split(",")[0]),1))
                S_OPY = str(round(float(S_OPXY.split(",")[1]),1))
                E_OPX = str(round(float(E_OPXY.split(",")[0]),1))
                E_OPY = str(round(float(E_OPXY.split(",")[1]),1))

                Current_segment = {"SegID": SEG_ID,

                               "S_X": S_OPX,
                               "S_Y": S_OPY,
                                "S_Z":S_Z ,
                               "E_X": E_OPX,
                               "E_Y": E_OPY,
                               "E_Z": E_Z,
                               "Rd_Width": Rd_Width,
                               "Rd_Type":Road_Type,
                               "Flow_ID":FlowID


                               }

                Content.append(Current_segment)

Df_NSR = pd.DataFrame(Content)

root = Tk()  # this is to close the dialogue box later
try:
    # with block automatically closes file
    with filedialog.asksaveasfile(mode='w', defaultextension=".xlsx", title='Save Rec Detail file as',
                                  initialfile="Segment info list.xlsx") as file:
        Df_NSR.to_excel(file.name)
except AttributeError:
    # if user cancels save, filedialog returns None rather than a file object, and the 'with' will raise an error
    print("The user cancelled save")

root.destroy()

tkinter.messagebox.showinfo('End', 'Segment successfully exported in .xlsx file.')

# Df_NSR.to_excel(f)