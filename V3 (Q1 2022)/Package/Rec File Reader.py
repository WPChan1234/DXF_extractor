import pandas as pd
from tkinter.filedialog import askopenfilename
from io import StringIO
import re


# Reference:https://allenlu2007.wordpress.com/2019/01/13/%E5%A2%9E%E9%80%B2%E5%B7%A5%E7%A8%8B%E5%B8%AB%E6%95%88%E7%8E%87-text-parsing-using-panda-and-regex/#

Path=askopenfilename(title="Choose .REC txt file")


with open(Path) as f:
    Text = f.read()
print(Text)

def Split_Group_text(Text,Spliter_Text):
    lines = Text.splitlines()

    Text_groups = []
    group = []
    for line in lines:
        match = re.search(Spliter_Text, line)
        if match:
            if group:
                Text_groups.append(group)
            group = []
        group.append(line)

    if Text_groups:
        print("Found Text groups:")
        for i, group in enumerate(Text_groups):
            print(f"Group {i + 1}:")
            for line in group:
                print(f"  {line}")
    else:
        print("No '"+Spliter_Text+" ' groups found.")

    return(Text_groups)

def Get_value_from_lines(TextGroups,ID_Text):
    Text_pattern = r"{}\s*=\s*(\d+)".format(ID_Text)
    # print(Text_pattern)
    Value_list=[]

    for Grp in TextGroups:
        Text_value=[]
        for line in Grp:
            match_text = re.search(Text_pattern, line)
            if match_text:
                Text_value = float(match_text.group(1))
                # print(Text_value)
                # print(f"Found value:"+ID_Text+ "Text_value}")
        if Text_value==[]:
            Text_value=None

        Value_list.append(Text_value)

    return(Value_list)


Grouped_text=Split_Group_text(Text,"TEXT")


#Get NSRID
NSR_ID=[]
for i in Grouped_text:
    NSR_ID.append(i[1])

print(NSR_ID)

DF_NSR=pd.DataFrame(NSR_ID,columns=['NSR_ID'])
print(DF_NSR)
#Get Parameters
Parameters= ["OPX","OPY","HRA","REF","HPF","RPT","AN1","AN2"]

Dict={}
for i in Parameters:
    globals()[i]=Get_value_from_lines(Grouped_text, i)
    Dict[i]=globals()[i]


DF_parameters=pd.DataFrame.from_dict(Dict,orient='index').transpose()
print(DF_parameters)
DF_parameters.to_csv('C:/Users/chanw/PycharmProjects/DXF_extractor/output/Para_output.csv')
DF_NSR=pd.merge(DF_NSR,DF_parameters, left_index=True, right_index=True)
print(DF_NSR)
DF_NSR=DF_NSR.ffill(axis=0)
DF_NSR=DF_NSR[DF_NSR['OPX'].notna()]
print(DF_NSR)


DF_NSR.to_csv('C:/Users/chanw/PycharmProjects/DXF_extractor/output/REC_output.csv')
