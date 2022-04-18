import collections
import tkinter.messagebox
from tkinter.filedialog import askopenfilename
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



tkinter.messagebox.showinfo('Rename NSRs in .dxf')

docPath = askopenfilename(title='Select DXF File with "REC" Blocks' )
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

# tkinter.messagebox.showinfo("NSR Duplicate Check", "Duplicated NSR "
#                                                    "(Gd to go if no duplicated NSRs) = " + str(Duplicated_NSR))

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
                       "X": OPX,
                       "Y": OPY,
                       "Tower": Tower,
                        "Unit": Unit,
                       "Tower+unit": Tower +"-"+ Unit

                       }

        NSR.append(Current_NSR)



Df_NSR = pd.DataFrame(NSR)

Df_NSR["Dist_from_origin"]=(Df_NSR["X"]**2+Df_NSR["Y"]**2)**0.5
print(Df_NSR)


#determin coordinate of first NSR by unit (most SE NSR)

Df_1st_NSR_X= Df_NSR.groupby("Tower+unit")["X"]
Df_1st_NSR_Y= Df_NSR.groupby("Tower+unit")["Y"]
Df_1st_NSR_Dist= Df_NSR.groupby("Tower+unit")["Dist_from_origin"]


Df_NSR["Min X within Unit"]=Df_1st_NSR_X.transform(min)
Df_NSR["ID for Min X "]=Df_1st_NSR_X.transform("idxmin")
Df_NSR["Rank"]=Df_1st_NSR_X.transform("rank").astype(int)
#Df_NSR["Min Y within Unit"]=Df_1st_NSR_Y.transform(min)#Not used
Df_NSR["RecID"]= Df_NSR["Tower+unit"]+Df_NSR["Rank"].astype(str)
Df_NSR["Coor"]=Df_NSR["X"].astype(str)+", "+Df_NSR["Y"].astype(str)

#print(Df_NSR)#Not used


#Change NSR ID
for REC_ID in Df_NSR["RecID"]:
    print(REC_ID)
    for insert in msp.query('INSERT'):
        if any("NSR_ID" in s for s in List):
            OPXY = List[0][1].replace('"', '')
            for attrib in insert.attribs:
                if  attrib.dxf.text==OPXY:
                    if  attrib.dxf.tag == "NSR_ID":
                        attrib.dxf.text = REC_ID
                        print(REC_ID)

def RecID_from_coor(Coor):
    Index=Df_NSR[Df_NSR["Coor"] == Coor].index.values
    Rec_ID=Df_NSR.at[Index[0], 'RecID']
    return Rec_ID

#print(RecID_from_coor("845823.2, 817438.5"))


for insert in msp.query('INSERT'):

    List = [(attrib.dxf.tag, attrib.dxf.text) for attrib in insert.attribs]
    if any("NSR_ID" in s for s in List):  ### Filter applied to search NSR blocks only ###

        OPXY = List[0][1].replace('"', '')
        RecID_block=RecID_from_coor(OPXY)
        #print(RecID_block)
        for attrib in insert.attribs:
            if attrib.dxf.tag == "NSR_ID":
                attrib.dxf.text = RecID_block


        #print(OPXY)


doc.save()
tkinter.messagebox.showinfo('End','NSR ID successfully updated in current .dxf file.')


#Df_NSR.to_excel("Receiver list.xlsx")

