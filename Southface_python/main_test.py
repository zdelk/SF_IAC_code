# Test for main
import pandas as pd
from VSD_replacement import VSDreplace
from Replace_Lights import LEDReplacement
from utilities_analysis import UtilityBill


input_path = 'test_input.xlsx'
output_path = 'test_output_2.xlsx'
def load_variables(constants):
    facility_dict = pd.Series(constants['FC Value'].values, index =constants['FC Var']).to_dict()
    vsd_dict = pd.Series(constants['VSD Value'].dropna().values, index = constants['VSD Var'].dropna()).to_dict()
    led_dict = pd.Series(constants['LED Value'].dropna().values, index = constants['LED Var'].dropna()).to_dict()
    
    return facility_dict, vsd_dict, led_dict
    
def main(input_path, output_path):
    input_workbook = pd.read_excel(input_path, engine = 'openpyxl', sheet_name = None)
    
    constants = input_workbook['Constants']
    
    facility_dict, vsd_dict, led_dict = load_variables(constants)
    
    for var_name, var_value in facility_dict.items():
        globals()[var_name] = var_value
        
    # Bill Analysis
    # !!!!!Always first!!!!!
    utility_bill = input_workbook['Utility Bills']
    bill_analysis = UtilityBill(utility_bill)
    
    annual_bill, energy_costs = bill_analysis.utility_analysis()
    
    per_kwh_cost = energy_costs['Price per kWh ($)']
    per_kw_peak_cost = energy_costs['Price per Peak kW ($)']
    per_therm_cost = energy_costs['Price per Therm ($)']
    
    energy_costs_df = bill_analysis.asDataFrame(energy_costs)
    annual_bill = bill_analysis.asDataFrame(annual_bill)
    # print(annual_bill)
    # print(energy_costs_df)

    # VSD replacement
    
    vsd_sheet = input_workbook['VSD Replacement']
    vsd_df = vsd_sheet.set_index(vsd_sheet.columns[0])
    
    vsd_replacement = VSDreplace(vsd_df, vsd_dict)
    vsd_replacement.read_values()
    vsd_replacement.set_costs(per_kwh_cost, per_kw_peak_cost, uptime_factory)
    vsd_results = vsd_replacement.VSDcalc()
    vsd_final = vsd_replacement.asDataFrame(vsd_results)
    # print(vsd_final)
    
    # LED Replacement
    led_replacement = LEDReplacement(led_dict)
    led_replacement.set_costs(per_kwh_cost, per_kw_peak_cost, uptime_factory)
    led_results = led_replacement.LED_savings()
    led_final = led_replacement.asDataFrame(led_results)
    # print(led_final)
    
    
    
    
    
    
    writer = pd.ExcelWriter(output_path, engine = 'xlsxwriter')

    energy_costs_df.to_excel(writer, sheet_name='Bill Analysis', index=False)
    annual_bill.to_excel(writer, sheet_name='Bill Analysis', index=False, startrow = 10)
    
    vsd_final.to_excel(writer, sheet_name= "VSD Replacment", index = False)
    
    led_final.to_excel(writer, sheet_name="LED Replacement", index=False)
    
    # # pipe_cost_data.to_excel(writer, sheet_name='Pipe Data', index=False, startcol=1, startrow=len1)
    # # pipe_table_data.to_excel(writer, sheet_name= 'Pipe Data', index=False, startcol=1, startrow=len2)
    # # pipe_heat_savings.to_excel(writer, sheet_name = 'Pipe Data', index=False, startcol=1, startrow=len3)

    # writer.close()
    return print("Process is complete!")
    


if __name__=='__main__':
    main(input_path, output_path)