import tkinter as tk
from tkinter import filedialog
import pandas as pd
import re
import numpy as np

# Function- Receiver file to dataframe
def RecFile_toDF(File_Path):
    with open(File_Path) as f:
        Text = f.read()
    print(Text)

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

    # def DFtoVector(df, Layer_name):
    #
    #     #     Create a list of QgsField objects for each column in the dataframe
    #     field_types = {
    #         "int64": QVariant.Int,
    #         "float64": QVariant.Double,
    #         "object": QVariant.String
    #     }
    #     fields = [QgsField(col, field_types[str(df[col].dtype)]) for col in df.columns]
    #
    #     ##   fields = []
    #     ##    for col in df.columns:
    #     ##        field = QgsField(col.item(), df[col].dtype) ##ERROR at this line
    #     ##        fields.append(field)
    #     #    print(fields)
    #
    #     #     Create a QgsVectorLayer from the dataframe
    #     vl = QgsVectorLayer("Point?crs=epsg:2326", Layer_name, "memory")
    #     pr = vl.dataProvider()
    #     pr.addAttributes(fields)
    #
    #     #     Start editing the layer to add features
    #     vl.startEditing()
    #
    #     for i, row in df.iterrows():
    #         fet = QgsFeature()
    #         point = QgsPointXY(row["OPX"], row["OPY"])
    #         #        print(point)
    #
    #         #        if not point.isValid():
    #         #            print(f"Invalid point coordinates for row {i}: {row['OPX'], row['OPY']}")
    #         #            continue
    #         fet.setGeometry(QgsGeometry.fromPointXY(point))
    #         fet.setAttributes([row[col] for col in df.columns])
    #         pr.addFeature(fet)
    #
    #     #    # Iterate over the features in the layer and print their attributes and geometries
    #     #    for feature in vl.getFeatures():
    #     #        print("Attributes:", feature.attributes())
    #     #        print("Geometry:", feature.geometry().asPoint())
    #
    #     #     stop editing and save changes
    #     vl.commitChanges()
    #
    #     #     add the layer to the qgis project
    #     QgsProject.instance().addMapLayer(vl)
    #
    #     #     save the layer to a geopackage file
    #     QgsVectorFileWriter.writeAsVectorFormat(vl, Layer_name + ".gpkg", "utf-8", vl.crs(), "gpkg")
    #     return ()

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
    DF_NSR["RPT"] = DF_NSR["RPT"].astype(int)

    # print(DF_NSR)
    print(DF_NSR)

    return(DF_NSR)

    # DFtoVector(DF_NSR, 'NSR_Python')


def ROP_to_DF(File_Path):

    with open(File_Path) as f:
        text = f.read()



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
    df['Fl']=df['Fl'].astype(int)
    df['RECEIVER']=df['RECEIVER'].astype(str)
    df.replace(r"^ +| +$", r"", regex=True)
    # Changing the column name
    df.rename(columns={'All': 'Total_SPL'}, inplace=True)

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
    df.to_csv("ROP", sep='\t', index=False)
    return(df)





# Step 1: Use Tkinter to ask for file paths
root = tk.Tk()
root.withdraw()

receiver_file_path = filedialog.askopenfilename(title="Select Receiver File")
rop_file_path = filedialog.askopenfilename(title="Select ROP File")

# Step 2: Read the Receiver file and expand the 'No. of RPT' column
receiver_df = RecFile_toDF(receiver_file_path)

# Expand value to list
def expand_list(value):
    return list(range(value))
receiver_df['Fl'] = receiver_df['RPT'].apply(expand_list)
receiver_df = receiver_df.explode('Fl')
receiver_df= receiver_df.reset_index(drop=True)
print(receiver_df)
# expanded_df = pd.concat([pd.DataFrame({'Fl': range(n)}) for n in receiver_df['RPT']], ignore_index=True) # problem in this line, should use something better than concat to expand the lines
#
# receiver_df = pd.concat([receiver_df]*len(expanded_df), ignore_index=True)
# receiver_df = pd.concat([receiver_df, expanded_df], axis=1)
receiver_df  = receiver_df.sort_values(by=['NSR_ID', 'Fl'], ascending=[True, True])
receiver_df.to_csv("NSR", sep='\t', index=False)
receiver_df.dropna(subset=['Fl'], inplace=True)
receiver_df['Fl']=receiver_df['Fl'].astype(int)
receiver_df["z"] = round(receiver_df["Fl"] * receiver_df["HPF"] +receiver_df["HRA"],1)
print(receiver_df)

# Save the dataframe to a text file (For checking only)
receiver_df.to_csv('example.txt', sep='\t', index=False)

# Step 3: Read the ROP file and join it with the expanded Receiver file
rop_df = ROP_to_DF(rop_file_path)
merged_df = pd.merge(receiver_df, rop_df, left_on=['NSR_ID','Fl'], right_on=['RECEIVER','Fl'])
# Print the merged dataframe
# merged_df = merged_df.drop_duplicates()
print(merged_df)

# Retaining only specific columns by name
columns_to_retain = ['NSR_ID','HRA','HPF','RPT','Fl','OPX','OPY','z','Total_SPL']
df_Rec_ROP = merged_df[columns_to_retain]


# Sort the DataFrame by 'Column1' in ascending order and then by 'Column3' in descending order
df_Rec_ROP = df_Rec_ROP.sort_values(by=['NSR_ID', 'z'], ascending=[True, True])


print(df_Rec_ROP)

window = tk.Tk()
window.withdraw()

# Open the file dialog to select the save location
file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                         filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])

if file_path:
    # Save the DataFrame to the selected location
    df_Rec_ROP.to_csv(file_path, sep='\t', index=False)
    print("DataFrame saved successfully.")

# Run the Tkinter event loop
window.mainloop()