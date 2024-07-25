# SF-IAC Main v1
# Created by: Zachary Delk
# --------------------------------------------------------------------------#
# Imports (Need to update placements)
import pandas as pd
import re
from VSD_replacement import VSDreplace
from Replace_Lights import LEDReplacement
from utilities_analysis import UtilityBill
from Pipe_insulation import PipeInsulation
from Air_Line_leaks import AirLeak

# --------------------------------------------------------------------------#
# Input and Output Paths
input_path = "Data/test_input.xlsx"
output_path = "Data/test_output_7.xlsx" # Set to not overwrite
k_val_path = "Data/K_values.csv"

# ---------------------------------------------------------------------------#
# Dictionary Maker (Could put in a seperate script)
def dictonary_maker(constants):
    full_names = list(constants.columns)
    # Get column names that have 'Var' and 'Value' (Not Variables)
    use_name = [word for word in full_names if 
                (re.search(r"Var$", word) or re.search(r"Value$", word))]
    
    # Loop that returns just the section names and no duplicates
    section_names = []
    for name in use_name:
        section_name = name.split(" ")[0]
        if section_name not in section_names:
            section_names.append(section_name)
            
    dictionaries = {}
    
    for section in section_names:
        r = re.compile(".*" + section)
        matched_columns = list(filter(r.match, use_name))
        if len(matched_columns) >= 2:
            key_col, value_col = matched_columns[:2]
            dictionaries[section] = pd.Series(
                constants[value_col].dropna().values, index=constants[key_col].dropna()
            ).to_dict()
        else:
            print(f"Not enough columns matched for {section}")
        
    return dictionaries

def name_to_class(name):
    return name.title().replace(" ","")
# Main Function

def main(input_path, output_path):
    print_dict = {}
    # Loading input workbook
    input_workbook = pd.read_excel(input_path, engine="openpyxl", sheet_name=None)
    constants = input_workbook["Constants"]
    dictionaries = dictonary_maker(constants)

    uptime_factory = dictionaries['FC']['uptime_factory']
    # Bill Analysis
    # !!!!!Always first!!!!!
    ub_sheet = input_workbook["Utility Bills"]
    utillity_bill = UtilityBill(ub_sheet)
    per_kwh_cost, per_kw_peak_cost, per_therm_cost, combined_bill_data = utillity_bill.processUtilityBill()
    
    print_dict['Utility Bills'] = combined_bill_data
    
    k_vals = pd.read_csv(k_val_path)
    costs = (per_kwh_cost, per_kw_peak_cost, per_therm_cost, uptime_factory)
    
    # VSD
    vsd_sheet = input_workbook['VSD Replacement']
    vsd_final = VSDreplace.processVSD(vsd_sheet, dictionaries, costs)
    print_dict['VSD Replacement'] = vsd_final

    # LED Replacment
    led_final = LEDReplacement.processLEDReplacment(dictionaries, costs)
    print_dict['LED Replacement'] = led_final
    
    # Pipe Insulation
    pipe_sheet = input_workbook['Pipe Data']
    pipe_final = PipeInsulation.process(pipe_sheet, dictionaries, costs)
    print_dict['Pipe Insulation'] = pipe_final
    
    # Air Leaks
    air_leak_final = AirLeak.process(dictionaries, costs)
    print_dict['Air Leak Fix'] = air_leak_final
    #--------------------------------------------------------------------------#
    # # Writing Section
    # writer = pd.ExcelWriter(output_path, engine = 'xlsxwriter')
    
    # for name, df in print_dict.items():
    #     df.to_excel(writer, sheet_name=name,index=False)
        
    # writer.close()
    # return print("Process is complete!")
    test_list = ['AirLeak','VSDreplace']
    for name in test_list:
        cls = globals()[name]
        output = cls.process(dictionaries, costs)
        print(output)
        # Need to update to append to print_dictionary
    # test = test_list[1]
    # test_final = test.process(dictionaries, costs)
    # print(test_final)

    # name_list = list(input_workbook.keys())
    # for name in name_list:
    #     class_name = name_to_class(name)
    #     cls = globals()[class_name]
    #     output = cls.process(stuff)


if __name__ == "__main__":
    main(input_path, output_path)
