from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile
import ezdxf
import tkinter.messagebox
import collections
from Utilities import round_half_up



tkinter.messagebox.showinfo('DXF 2 Noisemap (Receiver): Introduction', 'Convert DXF REC block to Noisemap File' )

docPath = askopenfilename(title='Select DXF File with "REC" Blocks only ------------------(MIN 2 REC BLOCKS!!)')
doc = ezdxf.readfile(docPath)
print(docPath)


msp = doc.modelspace()
List = []
RecList=[]
RecFile=[]
ListFile=["Zone, RecID, Tower, Unit"]

RecFile.append("TEXT \nREC \n")


print("TEXT \nREC \n")

# NSR duplicacy check#

for insert in msp.query('INSERT'):
            List = [(attrib.dxf.tag, attrib.dxf.text) for attrib in insert.attribs]
            if any("NSR_ID" in s for s in List): ### Filter applied to search NSR blocks only ###
                RecID = List[7][1]
                RecList.append(RecID)
print(RecList)

Duplicated_NSR = [item for item, count in collections.Counter(RecList).items() if count > 1]


tkinter.messagebox.showinfo("NSR Duplicate Check","Duplicated NSR "
                                                  "(Gd to go if no duplicated NSRs) = "+ str(Duplicated_NSR))


# Rec file formation#
for insert in msp.query('INSERT'):


            List = [(attrib.dxf.tag, attrib.dxf.text) for attrib in insert.attribs]
            if any("NSR_ID" in s for s in List):### Filter applied to search NSR blocks only ###
                print(List)

                RecID = List[7][1]



                OPXY  = List[0][1].replace('"', '')

                while OPXY == '##################': ## error message for corrupted REC block
                    tkinter.messagebox.showinfo("Error","Receiver block corrupted, rebuild coor. attribute")
                    break

                    exit

                OPX = str(round_half_up(float(OPXY.split(",")[0]),1))
                OPY = str(round_half_up(float(OPXY.split(",")[1]),1))
                HRA = str(round_half_up(float(List[1][1]), 2))
                HPF = str(round_half_up(float(List[3][1]),2))
                RPT = round_half_up(float(List[2][1]),1)
                Unit = str(List[4][1])
                Zone = str(List[5][1])
                Tower = str(List[6][1])


                ListFile.append(Zone+ "," + RecID  + "," + Tower + "," + Unit )


                # Current_Flr_level = str(round_half_up(float(HRA)+n*float(HPF),1))

                RecFile.append("TEXT")
                RecFile.append(RecID+"@RPT= 1NSR per Col")
                RecLine="HRA=    "+HRA+"HRG=     0.0OPX="+OPX+"OPY="+OPY+"AN1=     0.0AN2=   360.0"
                RecFile.append(RecLine)
                RecFile.append("REF=     1.0GO        .0")
                RecFile.append("HPF=     "+str(round_half_up(float(HPF),1))+"RPT=     "+str(round_half_up(RPT,1)))
                RecFile.append("")


RecFile.append("RETN     0.0")

print(RecFile)
print(ListFile)


with open('RecFile.Rec', 'w') as f:
    for item in RecFile:
        f.write("%s\n" % item)

f = asksaveasfile(mode='w', defaultextension=".txt",title='Save Noisemap Rec file as',initialfile="Receiver.rec")
for item in RecFile:
    f.write("%s\n" % item)
f.close()

with open('ListFile.Rec', 'w') as f:
    for item in ListFile:
        f.write("%s\n" % item)

f = asksaveasfile(mode='w', defaultextension=".txt",title='Save Rec Detail file as',initialfile="Receiver info list.txt")
for item in ListFile:
    f.write("%s\n" % item)
f.close()