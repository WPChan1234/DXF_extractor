import csv

import pandas as pd
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from tkinter import messagebox


# Obtain ROP A
ROP_path=askopenfilename(title="Choose ROP txt file")
with open(ROP_path) as f:
    ROP = f.read()
print(ROP)

Df_ROP= pd.read_csv(ROP_path, header=None)

print(Df_ROP)

#Row ID with ROP result header
StRowID= Df_ROP[Df_ROP[0].str.contains('RECEIVER                 Fl   All')].index[0]
print(StRowID)

EdRowID= Df_ROP[Df_ROP[0].str.contains('Calculation Run')].index[0]
print(EdRowID)

Df_ROP=Df_ROP.iloc[StRowID+1: , :]
Df_ROP[0]=Df_ROP[0].str.strip()  #remove head and tail spaces
print(Df_ROP)

Df_ROP[['NSR', 'FL & SPL']] = Df_ROP[0].str.split('@RPT= 1NSR per Col', n=1, expand=True)
Df_ROP['FL & SPL']=Df_ROP['FL & SPL'].str.strip()  #remove head and tail spaces
Df_ROP[['FL', 'SPL']] = Df_ROP['FL & SPL'].str.split(' ', n=1, expand=True)
Df_ROP=Df_ROP[['NSR','FL', 'SPL']]

Df_ROP= Df_ROP.astype({'NSR': str, 'FL': int,'SPL': float}, errors = 'ignore').dropna()
print(Df_ROP)