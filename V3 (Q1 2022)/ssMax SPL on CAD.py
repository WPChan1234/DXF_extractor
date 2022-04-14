import ezdxf
import csv
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile


Result_Pts = askopenfilename()
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
    x = e[0]
    y = e[1]
    SPL = int(e[2])

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

doc.saveas("Result map.dxf")


f = asksaveasfile(mode='w', defaultextension=".dxf")
f.close()
f=f.name

print(f)
doc.saveas(f)
