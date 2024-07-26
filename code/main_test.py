# Test for main
import pandas as pd
import re
from VSD_replacement import VSDreplace
from Replace_Lights import LEDReplacement
from utilities_analysis import UtilityBill
from Pipe_insulation import PipeInsulation
from Air_Line_leaks import AirLeak


input_path = 'Data/test_input.xlsx'
output_path = 'Data/test_output_5.xlsx'
k_val_path = 'Data/K_values.csv'
uptime_factory = 0

    
def dictonary_maker(constants):
    full_names = list(constants.columns)

    # Get column names that have 'Var' and 'Value' (Not Variables)
    use_name = [word for word in full_names if (re.search(r'Var$', word) or re.search(r'Value$', word))]

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
            dictionaries[section] = pd.Series(constants[value_col].dropna().values, index= constants[key_col].dropna()).to_dict()
        else:
            print(f"Not enough columns matched for {section}")
        
        return dictionaries
    # # Creates a list of dictionary names for assignment
    # dict_name_list = []
    # for y in section_names:
    #     dict_name_list.append( y + "_dict")
        
    # # Assigns keys and values to dictionary name
    # for i in range(len(section_names)):
    #     var = section_names[i] # Section
    #     dict_name = dict_name_list[i] # Dictionary Name
    #     r = re.compile(".*" + var) # Creates Regex object
    #     matched_columns = list(filter(r.match, use_name)) # Filters for columns matching Regex object
        
    #     if len(matched_columns) >= 2: # Makes sure dict has 2 columsn
    #         # Assigning keys and values
    #         key_col, value_col = matched_columns[:2] # Just in case there are more than 2 columns
    #         # Creating Dictionary
    #         globals()[dict_name] = pd.Series(constants[value_col].dropna().values, index= constants[key_col].dropna()).to_dict()
    #     else:
    #         print(f"Not enough columns matched for {var}")
            
        
    
def main(input_path, output_path):
    input_workbook = pd.read_excel(input_path, engine = 'openpyxl', sheet_name = None)
    constants = input_workbook['Constants']
    dictionaries = dictonary_maker(constants)
    
    #facility_dict, vsd_dict, led_dict, pipe_dict = load_variables(constants)
    # dictonary_maker(constants)
    # for var_name, var_value in FC_dict.items():
    #     globals()[var_name] = var_value
        
    # Bill Analysis
    # !!!!!Always first!!!!!
    utility_bill = input_workbook['Utility Bills']
    per_kwh_cost, per_kw_peak_cost, per_therm_cost, combined_bill_data = utility_bill.processUtilityBill()
    
    # bill_analysis = UtilityBill(utility_bill)
    # annual_bill, energy_costs = bill_analysis.utility_analysis()
    # per_kwh_cost = energy_costs['Price per kWh ($)']
    # per_kw_peak_cost = energy_costs['Price per Peak kW ($)']
    # per_therm_cost = energy_costs['Price per Therm ($)']
    # #per_therm_cost = 10
    
    # energy_costs_df = bill_analysis.asDataFrame(energy_costs)
    # annual_bill = bill_analysis.asDataFrame(annual_bill)
    #--------------------------------------------------------------------------#
    # VSD replacement
    vsd_sheet = input_workbook['VSD Replacement']
    vsd_df = vsd_sheet.set_index(vsd_sheet.columns[0])
    
    vsd_replacement = VSDreplace(vsd_df, VSD_dict)
    vsd_replacement.read_values()
    vsd_replacement.set_costs(per_kwh_cost, per_kw_peak_cost, uptime_factory)
    vsd_results = vsd_replacement.VSDcalc()
    vsd_final = vsd_replacement.asDataFrame(vsd_results)
    # print(vsd_final)
    
    #--------------------------------------------------------------------------#
    # LED Replacement
    led_replacement = LEDReplacement(LED_dict)
    led_replacement.set_costs(per_kwh_cost, per_kw_peak_cost, uptime_factory) 
    led_results = led_replacement.LED_savings()
    led_final = led_replacement.asDataFrame(led_results)
    # print(led_final)
    
    #--------------------------------------------------------------------------#
    # Pipe insulation
    k_vals = pd.read_csv(k_val_path)
    pipe_sheet = input_workbook['Pipe Data']
    pipe_insulation = PipeInsulation(pipe_sheet, k_vals, Pipe_dict)
    pipe_insulation.set_costs(per_kwh_cost, per_kw_peak_cost, per_therm_cost, uptime_factory, t_A)
    pipe_cost_data, pipe_table_data, pipe_heat_savings = pipe_insulation.pipe_final()

    len1 = 1
    len2 = len1 + len(pipe_cost_data) + 2
    len3 = len2 + len(pipe_table_data) + 2

    #--------------------------------------------------------------------------#
    air_leaks = AirLeak(AirLeak_dict)
    air_leaks.set_costs(per_kw_peak_cost, per_kwh_cost, uptime_factory, t_A)
    air_leak_results = air_leaks.air_leak_calculation()
    air_leak_final = air_leaks.asDataFrame(air_leak_results)
    
    #--------------------------------------------------------------------------#
    # Writing Section
    writer = pd.ExcelWriter(output_path, engine = 'xlsxwriter')

    combined_bill_data.to_excel(writer, sheet_name='Bill Analysis', index=False)
    
    vsd_final.to_excel(writer, sheet_name= "VSD Replacment", index = False)
    
    led_final.to_excel(writer, sheet_name="LED Replacement", index=False)
    
    pipe_cost_data.to_excel(writer, sheet_name='Pipe Data', index=False, startcol=1, startrow=len1)
    pipe_table_data.to_excel(writer, sheet_name= 'Pipe Data', index=False, startcol=1, startrow=len2)
    pipe_heat_savings.to_excel(writer, sheet_name = 'Pipe Data', index=False, startcol=1, startrow=len3)
    
    air_leak_final.to_excel(writer, sheet_name="Air Leak", index = False)

    writer.close()
    return print("Process is complete!")
    


if __name__=='__main__':
    main(input_path, output_path)