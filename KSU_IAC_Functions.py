# Reusing this file name since it already existed
# Now it will hold general functions to be used in main
import pandas as pd
import re
import numpy as np
import importlib

# ---------------------------------------------------------------------------#
# Dictionary Maker (Could put in a seperate script)
# def dictonary_maker(constants):
#     full_names = list(constants.columns)
#     # Get column names that have 'Var' and 'Value' (Not Variables)
#     use_name = [word for word in full_names if 
#                 (re.search(r"Var$", word) or re.search(r"Value$", word))]
    
#     # Loop that returns just the section names and no duplicates
#     section_names = []
#     for name in use_name:
#         section_name = name.split(" ")[0]
#         if section_name not in section_names:
#             section_names.append(section_name)
    
#     # print(section_names)
#     dictionaries = {}
    
#     for section in section_names:
#         r = re.compile(".*" + section)
#         matched_columns = list(filter(r.match, use_name))
#         if len(matched_columns) >= 2:
#             key_col, value_col = matched_columns[:2]
#             dictionaries[section] = pd.Series(
#                 constants[value_col].dropna().values, index=constants[key_col].dropna()
#             ).to_dict()
#         else:
#             print(f"Not enough columns matched for {section}")
        
#     return dictionaries, section_names

def dictionary_2(file_path):
    name = None
    dictionaries = {}
    section_dict = {}
    
    with open(file_path) as f:
        for line in f:

            if line.startswith("#") or line.strip() == '':
                continue
            
            elif line.startswith("!"):
                
                if name:
                    dictionaries[name] = section_dict
                    
                name = line[1:].strip()
                section_dict = {}
                
            else:
                key, value = line.strip().split(" = ")
                try:
                    value = float(value)
                except:
                    value = value
                    
                section_dict[key] = value
                
            if name:
                dictionaries[name] = section_dict
            

    section_names = list(dictionaries.keys())
    
    return dictionaries, section_names


def dynamic_import(module_name, class_name):
    module = importlib.import_module(module_name)
    return getattr(module, class_name)
    
# # Need to decide if function is neccesarry
# def full_analysis(input_workbook, section_names):
    
#     sheet_list = list(input_workbook.keys())
    
#     for name in section_names:
#         sheet_name = next((title for title in sheet_list if re.search(name + r".*", title)), None)
        
#         try:
#             module_name, class_name = section_to_class_map[name]
#         except KeyError as e:
#             print(f"{name} has no associated class: {e}")
#             continue
        
#         if class_name is None:
#             print(f"No class found for section: {name}")
#             continue
        
#         try:
#             cls = dynamic_import(module_name, class_name)
#         except ImportError as e:
#             print(f"Error importing class {class_name} from {module_name}: {e}")
#             continue
        
#         print(f"Processing section: {name}")
#         print(f"Class name: {class_name}")
#         print(f"Sheet name: {sheet_name}")
        
#         if sheet_name:
#             print(f'{name} has a sheet in the workbook')
#             output = cls.process(input_workbook[sheet_name], dictionaries, costs)
#         else:
#             print(f'{name} does not have a sheet in the workbook')
#             output = cls.process(dictionaries, costs)
            
#             print_dict[class_name] = output
#         return print_dict

class SFIACGeneral:
    def __init__(self, dict):
        self.set_const(dict)
        
    
    def set_const(self, dict):
        for key, value in dict.items():
            setattr(self, key, value)
        

    def set_costs(
        self, per_kwh_cost, per_kw_peak_cost, per_therm_cost, per_mmbtu_cost, uptime_factory, t_A
    ):
        self.cost_peak = per_kw_peak_cost
        self.cost_kwh = per_kwh_cost
        self.cost_therm = per_therm_cost
        self.cost_mmbtu = per_mmbtu_cost
        self.uptime = uptime_factory
        self.t_A = t_A

    def asDataFrame(self, results):
        df = pd.DataFrame([results])
        return df
    