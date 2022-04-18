import csv
import tkinter.messagebox
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile
import test_ezdxf2png


import ezdxf

tkinter.messagebox.showinfo('Txt to DXF  result map', ' Result list conversion to dxf map')
tkinter.messagebox.showinfo('Notes for Data Source', 'Select list of results in format of [X,Y,SPL] in txt file')

Result_Pts = askopenfilename(
    title='Select txt file with list of coordinates and noise levels (in X,Y, SPL separated by comma)')
print(Result_Pts)

doc = ezdxf.new('R12', setup=True)
msp = doc.modelspace()

with open(Result_Pts, newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

Layer_no_exceed = 'SPL_No_Exceedance'
Layer_70_to_76 = 'SPL_Between_70_and_76dB'
Layer_more_than_76 = 'SPL_More_than_76dB'

doc.layers.new(name=Layer_no_exceed, dxfattribs={'color': 3})
doc.layers.new(name=Layer_70_to_76, dxfattribs={'color': 30})
doc.layers.new(name=Layer_more_than_76, dxfattribs={'color': 1})

for e in data:
    x = float(e[0])
    y = float(e[1])
    SPL = int(e[2])

    print(type(SPL))

    if (SPL <= 70.4):
        Layer = Layer_no_exceed

    elif (SPL > 76.4):
        Layer = Layer_more_than_76

    else:
        Layer = Layer_70_to_76

    # Using a text style
    msp.add_text(SPL,
                 dxfattribs={
                     'layer': Layer,
                     'style': 'Standard',
                     'height': 1.5}
                 ).set_pos((x, y), align='MIDDLE_CENTER')

MLP_Path = askopenfilename(
    title='Select MLP underlay in .dxf')


doc.add_xref_def(filename=MLP_Path,name="MLP_xref")
msp.add_blockref(name='MLP_xref', insert=(0, 0))

test_ezdxf2png.convert_dxf2img()

f = asksaveasfile(mode='w', defaultextension=".dxf", title='Save DXF file as', initialfile="Result Map.dxf")
f.close()
f = f.name

print(f)
doc.saveas(f)
