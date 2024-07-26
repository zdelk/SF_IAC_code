# Testing how to upack  names in constant sheet
# Goal is to streamline dictionary creation
import pandas as pd
import re

# Set Path
input_path = 'Data/test_input.xlsx'

# Import full workbook
full_workbook = pd.read_excel(input_path, engine='openpyxl', sheet_name= None)

# Save 'Constants' sheet as var
constants = full_workbook['Constants']

# Get header (first row) from sheet
full_names = list(constants.columns)


# Get column names that have 'Var' and 'Value' (Not Variables)
use_name = [word for word in full_names if (re.search(r'Var$', word) or re.search(r'Value$', word))]

print('Use Name Test:')
print(use_name)


# Loop that returns just the section names and no duplicates
section_names = []
for name in use_name:
    section_name = name.split(" ")[0]
    if section_name not in section_names:
        section_names.append(section_name)
        
        
print("Section names:")
print(section_names)


print(full_names)
# Creates a list of dictionary names for assignment
dict_name_list = []
for y in section_names:
    dict_name_list.append( y + "_dict")

# Assigns keys and values to dictionary name
for i in range(len(section_names)):
    var = section_names[i] # Section
    dict_name = dict_name_list[i] # Dictionary Name
    r = re.compile(".*" + var) # Creates Regex object
    matched_columns = list(filter(r.match, use_name)) # Filters for columns matching Regex object
    
    if len(matched_columns) >= 2: # Makes sure dict has 2 columsn
        # Assigning keys and values
        key_col, value_col = matched_columns[:2] # Just in case there are more than 2 columns
        # Creating Dictionary
        globals()[dict_name] = pd.Series(constants[value_col].dropna().values, index= constants[key_col].dropna()).to_dict()
    else:
        print(f"Not enough columns matched for {var}")
        
print("Fucntion Test:")
print(FC_dict)


print("Simple Test:")

#test_dict = pd.Series(constants[FC_dict[1]].dropna().values, index= constants[FC_dict[0]].dropna()).to_dict()

#print(test_dict)

print("Name Test:")
print(dict_name_list[0])
# for i in range(len(dict_list)):
#     dict_name = dict_name_list[i]
#     globals()[dict_name] = pd.Series(constants[dict_name[1]].dropna().values, index = constants[dict_name[0]].dropna()).to_dict()
#

print("Test for Assignment:")
print(Pipe_dict)
