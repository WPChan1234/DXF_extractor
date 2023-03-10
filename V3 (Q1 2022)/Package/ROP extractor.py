import re
import pandas as pd
import tkinter as tk
from tkinter import filedialog


def open_file_dialog():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename()


def save_file_dialog():
    root = tk.Tk()
    root.withdraw()
    return filedialog.asksaveasfilename(defaultextension=".csv")


# get the input file location from the user
print("Select the input file:")
input_file = open_file_dialog()

# read the text from the input file
with open(input_file, "r") as f:
    text = f.read()
print(text)
# replace multiple spaces with a single space
text = re.sub(r"\s+", " ", text)

# regular expression to match the required pattern
pattern = r"([\w-]+)@RPT= 1NSR per Col\s+(\d+)\s+(\d+\.\d+)"
print(pattern)
# find all matches of the pattern in the text
matches = re.findall(pattern, text)
print(matches)
# create a DataFrame from the matches
df = pd.DataFrame(matches, columns=["RECEIVER", "Fl", "All"])

print(df)
# get the output file location from the user
print("Select the output file:")
output_file = save_file_dialog()

# save the DataFrame to the output file
df.to_csv(output_file, index=False)

# print a message indicating the output file location
print("Output file saved to:", output_file)
