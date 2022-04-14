from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile
import ezdxf
import tkinter.messagebox
import collections

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
                Speed_kph=List[5][1]
                Rd_Width=float(List[8][1])
                Half_RD_Wid=str(round((Rd_Width/2),1))
                FlowID=List[3][1]

                ## LNRS
                if List[6][1] =="Y":
                  LNRS = str(2.0)
                else: LNRS=str(1.0)

                First_eff_bar ="{:>8}".format("-"+str(round(float(List[7][1]),1)))

                while S_OPXY == '##################': ## error message for corrupted SEG block
                    tkinter.messagebox.showinfo("Error","SEG block corrupted, rebuild coor. attribute")
                    break

                    exit

                S_OPX = str(round(float(S_OPXY.split(",")[0]),1))
                S_OPY = str(round(float(S_OPXY.split(",")[1]),1))
                E_OPX = str(round(float(E_OPXY.split(",")[0]),1))
                E_OPY = str(round(float(E_OPXY.split(",")[1]),1))



                ListFile.append(SEG_ID + ","+ S_OPX + ","+ S_OPY + ","+ S_Z+ ","+ E_OPX + ","+ E_OPY + ","+ E_Z+  ","+Speed_kph+","+Half_RD_Wid)


                SegFile.append("TEXT")
                SegFile.append(SEG_ID)

                SegLine1="UFN="+FlowID+"CAT=     1.0"+"RSX="+S_OPX+"RSY="+S_OPY+"HCS=    "+S_Z+"HCG=     0.0"
                SegLine2="SEG=     1.0NCY=     1.0WCY=     "+ Half_RD_Wid + "DCY=     0.0HCY=     0.0"
                SegLine3 = "RST=     "+LNRS+"RTD=     1.0GND=     0.0NBA="+First_eff_bar+"RCT=     0.0"
                SegLine4 = "REX=" + E_OPX + "REY=" + E_OPY + "HCE=    " + E_Z + "SEND      .0"

                SegFile.append(SegLine1)
                SegFile.append(SegLine2)
                SegFile.append(SegLine3)
                SegFile.append(SegLine4)
                SegFile.append("")

SegFile.append("RETN     0.0")

print(ListFile)




with open('ListFile.Rec', 'w') as f:
    for item in ListFile:
        f.write("%s\n" % item)

f = asksaveasfile(mode='w', defaultextension=".txt",title='Save Rec Detail file as',initialfile="Segment info list.txt")
for item in ListFile:
    f.write("%s\n" % item)
f.close()

with open('SegFile.seg', 'w') as f:
    for item in SegFile:
        f.write("%s\n" % item)

f = asksaveasfile(mode='w', defaultextension=".txt",title='Save Noisemap Seg file as',initialfile="Segment.seg")
for item in SegFile:
    f.write("%s\n" % item)
f.close()