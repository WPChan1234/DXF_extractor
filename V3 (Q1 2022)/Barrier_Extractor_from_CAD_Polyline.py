import ezdxf
import os
from tkinter import Tk
import tkinter as tk
import tkinter.messagebox
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile
import ezdxf

root = Tk()
root.withdraw()
tk.messagebox.showinfo('DXF 2 Noisemap (Barrier): Introduction', 'Convert DXF polyline to Noisemap File// ' 
                                            'Select file & polyline containing layers ')

docPath = askopenfilename(title='Select DXF File')

doc = ezdxf.readfile(docPath)
print(docPath)
root.destroy()

# iterate over all entities in modelspace
msp = doc.modelspace()

List_Output = ["layer,Xs,Ys,Zs,Xe,Ye,Ze"]
CRTN_Output = ["Text","Barrier File",""]

BarID = 9000
Pline = msp.query('LWPOLYLINE')
no_of_pline=len(Pline)
print(no_of_pline)

# All layers
All_Layers = []
for Layer in doc.layers:
    All_Layers.append(Layer.dxf.name)
print(All_Layers)

root = Tk()
root.withdraw()

app = tk.Tk()
app.geometry("500x600")
app.title('Select Polyline layer to be extracted')

# Tinker interface for layer selection
Layer_for_extract=[]

def clicked():
    print("clicked")
    selected = box.curselection()  # returns a tuple
    for idx in selected:
        Layer_for_extract.append(box.get(idx))

box = tk.Listbox(app, selectmode=tk.MULTIPLE, height=30)
values = All_Layers
for val in values:
    box.insert(tk.END, val)
box.pack()

button = tk.Button(app, text='Select layer to be extracted', width=50, command=clicked)
button.pack()

exit_button = tk.Button(app, text='Excute', width=50, command=app.destroy)
exit_button.pack()
root.destroy()

app.mainloop()


print(Layer_for_extract)

# function for Line segment extraction
def print_entity(e):
    layer = e.dxf.layer
    st = e.dxf.start
    end = e.dxf.end




    st_x = str(round(st[0],1))
    st_y = str(round(st[1],1))
    st_z = str(round(st[2],1))


    End_x = str(round(end[0],1))
    End_y = str(round(end[1],1))
    End_z = str(round(end[2],1))


    info = [BarID, layer, st, end]
    List_Output.append(info)

    Bar_Output1 = "NBA="+str(BarID)+"BSX="+st_x+"BSY="+st_y+"BEX="+End_x+"BEY="+End_y
    Bar_Output2 = "HBS=" + st_z + "HBE=" + End_z
    CRTN_Output.append("Text")
    CRTN_Output.append(layer)
    CRTN_Output.append(Bar_Output1)
    CRTN_Output.append(Bar_Output2)
    CRTN_Output.append("")

# Layer filtering and polyline explode


for e in msp.query("LWPOLYLINE"):
    if e.dxf.layer in Layer_for_extract:
        print(e)
        e.explode()
for line in msp.query("LINE"):
    if line.dxf.layer in Layer_for_extract:
        print(line)
        print_entity(line)
        BarID = BarID+1

CRTN_Output.append("RETN     0.0")
print(CRTN_Output)



f = asksaveasfile(mode='w', defaultextension=".bar", title='Save Noisemap barrier file as',initialfile = "Barrier")
for item in CRTN_Output:
    f.write("%s\n" % item)
f.close()