import re
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from io import StringIO
import re
import numpy as np

def open_file_dialog():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename()


def save_file_dialog():
    root = tk.Tk()
    root.withdraw()
    return filedialog.asksaveasfilename(defaultextension=".csv")


def ReadROP():

    # get the input file location from the user
    print("Select the input file:")
    input_file = open_file_dialog()

    # read the text from the input file
    with open(input_file, "r") as f:
        text = f.read()
    # print(text)


    # replace multiple spaces with a single space
    text = re.sub(r"\s+", " ", text)

    # regular expression to match the required pattern
    pattern = r"([\w-]+)@RPT= 1NSR per Col\s+(\d+)\s+(\d+\.\d+)"
    # print(pattern)
    # find all matches of the pattern in the text
    matches = re.findall(pattern, text)
    # print(matches)
    # create a DataFrame from the matches


    df = pd.DataFrame(matches, columns=["RECEIVER", "Fl", "All"])
    df['Fl'].astype(int)
    df.replace(r"^ +| +$", r"", regex=True)

    print(df)
    # get the output file location from the user
    # print("Select the output file:")
    # output_file = save_file_dialog()
    #
    # # save the DataFrame to the output file
    # df.to_csv(output_file, index=False)
    #
    # # print a message indicating the output file location
    # print("Output file saved to:", output_file)
    print(df.dtypes)

    return(df)

df_ROP=ReadROP()

def ReadREC():

    # get the input file location from the user
    print("Select the input file:")
    input_file = open_file_dialog()

    # read the text from the input file
    with open(input_file, "r") as f:
        Text = f.read()
    # print(Text)

    def Split_Group_text(Text, Spliter_Text):
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

        #    if Text_groups:
        #        print("Found Text groups:")
        #        for i, group in enumerate(Text_groups):
        #            print(f"Group {i + 1}:")
        #            for line in group:
        #                print(f"  {line}")
        else:
            print("No '" + Spliter_Text + " ' groups found.")

        return (Text_groups)


    def Get_value_from_lines(TextGroups, ID_Text):
        Text_pattern = r"{}\s*=\s*(\d+\.\d)".format(ID_Text)
        # print(Text_pattern)
        Value_list = []

        for Grp in TextGroups:
            Text_value = []
            for line in Grp:
                match_text = re.search(Text_pattern, line)
                if match_text:
                    Text_value = float(match_text.group(1))
                    # print(Text_value)
                    # print(f"Found value:"+ID_Text+ "Text_value}")
            if Text_value == []:
                Text_value = None

            Value_list.append(Text_value)

        return (Value_list)


    Grouped_text = Split_Group_text(Text, "TEXT")

    # Get NSRID
    NSR_ID = []
    for i in Grouped_text:
        NSR_ID.append(i[1])
    #
    # print(NSR_ID)
    #
    DF_NSR = pd.DataFrame(NSR_ID, columns=['NSR_ID'])
    DF_NSR["NSR_ID"] = DF_NSR["NSR_ID"].str.lstrip()
    DF_NSR["NSR_ID"] = DF_NSR["NSR_ID"].str.replace("@RPT= 1NSR per Col", '')
    # print(DF_NSR)
    # Get Parameters
    Parameters = ["OPX", "OPY", "HRA", "REF", "HPF", "RPT", "AN1", "AN2"]

    Dict = {}
    List_DF_content = []
    for i in Parameters:
        List_DF_content.append(Get_value_from_lines(Grouped_text, i))
    #
    # print(List_DF_content)

    DF_Features = pd.DataFrame(np.array(List_DF_content).transpose(), columns=Parameters)
    # Combine Data frame
    DF_NSR = pd.concat([DF_NSR, DF_Features], axis=1, join='inner')
    # print(DF_NSR)


    DF_NSR = DF_NSR.ffill(axis=0)
    DF_NSR = DF_NSR[DF_NSR['OPX'].notna()]
    print(DF_NSR)

    return(DF_NSR)

df_REC=ReadREC()

def generate_list(n):
    return list(range(int(n+1)))

df_REC['RPT List'] =  df_REC['RPT'].apply(generate_list)

df_REC = df_REC.explode('RPT List')
df_REC.rename(columns={'RPT List': 'Fl'}, inplace=True)

# reset the index
df_REC.reset_index(drop=True, inplace=True)
print(df_REC)

df_REC['mpD']=df_REC['HRA']+df_REC['Fl']*df_REC['HPF']
print(df_REC)



# # get the output file location from the user
# print("Select the output file:")
# output_file = save_file_dialog()
#
# # save the DataFrame to the output file
# # df_REC.to_csv(output_file, index=False)
#
# # print a message indicating the output file location
# print("Output file saved to:", output_file)
print(df_ROP.dtypes)
print(df_REC.dtypes)
# Change the data type of 'col2' from float to integer (rounded to the nearest integer)
df_REC['Fl'].astype(int)
df_REC['mpD'].astype(int)
df_REC.replace(r"^ +| +$", r"", regex=True)
print(df_REC.dtypes)
# Merge the two DataFrames using the 'key_a' and 'key_b' columns from df1 and the 'key_c' and 'key_d' columns from df2
df_Merged = pd.merge(df_REC, df_ROP, left_on=['NSR_ID', 'Fl'], right_on=['RECEIVER', 'Fl'])


output_file = save_file_dialog()

# save the DataFrame to the output file
df_Merged.to_csv(output_file, index=False)

print(df_Merged)