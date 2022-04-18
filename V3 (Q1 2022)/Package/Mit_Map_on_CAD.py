import ezdxf
import csv
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile
import tkinter.messagebox

tkinter.messagebox.showinfo('Txt to DXF NMM map' , ' NMM schedule conversion to dxf map' )
tkinter.messagebox.showinfo('Notes for Data Source' , 'Select list of results in format of [X,Y,NMM with floor levels] in txt file')

Result_Pts = askopenfilename(title='Select txt file with list of coorinates and noise levels (in X,Y, NMM with floor levels)')
print(Result_Pts)

doc = ezdxf.new('R12', setup=True)
msp = doc.modelspace()



with open(Result_Pts, newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

Layer_Mit = 'AC_Mitigation_MAP'


doc.layers.new(name=Layer_Mit, dxfattribs={'color': 3})


for e in data:
    x = float(e[0])
    y = float(e[1])
    Mit = str(e[2])



    # Using a text style
    msp.add_text(Mit,
                 dxfattribs={
                     'layer': Layer_Mit,
                     'style': 'LiberationSerif',
                     'height': .5}
                 ).set_pos((x, y), align='MIDDLE_CENTER')


f = asksaveasfile(mode='w', defaultextension=".dxf",title='Save DXF file as',initialfile="Mitigation Map.dxf")
f.close()
f=f.name

print(f)
doc.saveas(f)
