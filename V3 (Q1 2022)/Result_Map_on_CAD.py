import ezdxf
import csv
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile


Result_Pts = askopenfilename(title="Choose result txt file")
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
    x = round(float(e[0]),1)
    y = round(float(e[1]),1)
    SPL = int(float(e[2]))

    print(x,y,SPL)

    if(SPL <= 70.4):
        Layer = Layer_no_exceed

    elif(SPL > 76.4):
        Layer = Layer_more_than_76

    else:
        Layer = Layer_70_to_76

    # Using a text style
    msp.add_text(SPL,
                 dxfattribs={
                     'layer': Layer,
                     'style': 'LiberationSerif',
                     'height': 1}
                 ).set_pos((x, y), align='MIDDLE_CENTER')


xref = askopenfilename(title="Choose drawing file for underlay")

print(xref)

doc.add_xref_def(filename=xref, name="dwg_xref")
msp.add_blockref(name='dwg_xref', insert=(0, 0))

f = asksaveasfile(mode='w', defaultextension=".dxf")
f.close()
f=f.name

print(f)
doc.saveas(f)
