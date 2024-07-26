# 7/26/24 works as expected
# SF-IAC Main v1
# Created by: Zachary Delk
# --------------------------------------------------------------------------#
# Imports (Need to update placements)
import pandas as pd
import re
from utilities_analysis import UtilityBill
import importlib
from KSU_IAC_Functions import *

# --------------------------------------------------------------------------#
# Input and Output Paths
input_path = "Data/test_input.xlsx"
output_path = "Data/test_output_8.xlsx" # Set to not overwrite

# Main Function

def main(input_path, output_path):
    print_dict = {}
    # Loading input workbook
    input_workbook = pd.read_excel(input_path, engine="openpyxl", sheet_name=None)
    constants = input_workbook["Constants"]
    dictionaries, section_names = dictonary_maker(constants)

    uptime_factory = dictionaries['FC']['uptime_factory']
    # Bill Analysis
    # !!!!!Always first!!!!!
    ub_sheet = input_workbook["Utility Bills"]
    utillity_bill = UtilityBill(ub_sheet)
    per_kwh_cost, per_kw_peak_cost, per_therm_cost, combined_bill_data = utillity_bill.process()
    
    print_dict['Utility Bills'] = combined_bill_data
    
    costs = (per_kwh_cost, per_kw_peak_cost, per_therm_cost, uptime_factory)

    section_to_class_map = {
        'AirLeak': ('Air_Line_leaks', 'AirLeak'),
        'Pipe': ('Pipe_insulation', 'PipeInsulation'),
        'LED': ('Replace_Lights', 'LEDReplacement'),
        'VSD': ('VSD_replacement', 'VSDreplace')
    }

    
    sheet_list = list(input_workbook.keys())
    
    for name in section_names:
        sheet_name = next((title for title in sheet_list if re.search(name + r".*", title)), None)
        
        try:
            module_name, class_name = section_to_class_map[name]
        except KeyError as e:
            print(f"{name} has no associated class: {e}")
            continue
        
        if class_name is None:
            print(f"No class found for section: {name}")
            continue
        
        try:
            cls = dynamic_import(module_name, class_name)
        except ImportError as e:
            print(f"Error importing class {class_name} from {module_name}: {e}")
            continue
        
        print(f"Processing section: {name}")
        print(f"Class name: {class_name}")
        print(f"Sheet name: {sheet_name}")
        
        if sheet_name:
            print(f'{name} has a sheet in the workbook')
            output = cls.process(input_workbook[sheet_name], dictionaries, costs)
        else:
            print(f'{name} does not have a sheet in the workbook')
            output = cls.process(dictionaries, costs)
        
        
        print_dict[class_name] = output
 
    #--------------------------------------------------------------------------#
    # Writing Section
    writer = pd.ExcelWriter(output_path, engine = 'xlsxwriter')
    
    for name, df in print_dict.items():
        df.to_excel(writer, sheet_name=name,index=False)
        
    writer.close()
    return print("Process is complete!")
    
    #--------------------------------------------------------------------------#




if __name__ == "__main__":
    main(input_path, output_path)
