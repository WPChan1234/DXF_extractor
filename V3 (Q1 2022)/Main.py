
from tkinter import *


class Checkbar(Frame):
   def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
      Frame.__init__(self, parent)
      self.vars = []
      for pick in picks:
         var = IntVar()
         chk = Checkbutton(self, text=pick, variable=var)
         chk.pack(side=side, anchor=anchor, expand=YES)
         self.vars.append(var)
   def state(self):
      return map((lambda var: var.get()), self.vars)

if __name__ == '__main__':
   root = Tk()
   root.geometry('600x200')
   root.title('Noisemap file generator/ Result map generator')

   R = Label(root, text="Receiver file extraction and related tools")
   R.pack()

   Receiver = Checkbar(root, ['.rec(1NSR per column (Default)','.rec(1NSR per floor)', 'NSR rename'])
   Receiver.pack(side=TOP, fill=X)

   Receiver.config(relief=GROOVE, bd=2)

   w = Label(root, text="Noisemap file generator from .dxf files (other than receiver files):")
   w.pack()
   DXF_extraction = Checkbar(root, ['.bar', '.pro', '.seg'])



   DXF_extraction.pack(side=TOP,  fill=X)

   DXF_extraction.config(relief=GROOVE, bd=2)

   E = Label(root, text=".txt result files to .dxf :")
   E.pack()

   Excel_to_DXF = Checkbar(root, ['.xls to SPL map', '.xls to mitigation map'])
   Excel_to_DXF.pack(side=TOP, fill=X)

   Excel_to_DXF.config(relief=GROOVE, bd=2)



   def allstates():

      State = list(Receiver.state())
      print(State)
      if State[0] == 1:
         import DXF_2_REC_1_NSR_per_Column
      if State[1] == 1:
         import DXF_2_REC_1NSR_per_floor
      if State[2] == 1:
         import NSR_rename

      State=list(DXF_extraction.state())
      print(State)


      if State[2] == 1:
         import Barrier_Extractor_from_CAD_Polyline
      if State[3] == 1:
         import Contour_extractor_from_Polyline
      if State[4] == 1:
         import Road_noise_segement_file_generator_v2

      to_dxf = list(Excel_to_DXF.state())

      if to_dxf[0]==1:
          import Result_Map_on_CAD
      if to_dxf[1] == 1:
         import Mit_Map_on_CAD



   Button(root, text='Quit', command=root.quit).pack(side=RIGHT)
   Button(root, text='Excute', command=allstates).pack(side=RIGHT)
   root.mainloop()

print(DXF_extraction[0])

