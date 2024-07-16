# Plan: Simple script that will take in a workbook,
# preform the analysis, and then output to another workbook
import pandas as pd
from utilities_analysis import utility_analysis
from KSU_IAC_Functions import pipe_final
from Air_Line_leaks import air_leak_calculation


input_path = 'test_input.xlsx'
output_path = 'test_output.xlsx'

# Input should just be the path of the orginal workbook,
# and path of the output

def IAC_function(input_path, output_path):
    input_workbook = pd.read_excel(input_path, engine = 'openpyxl', sheet_name = None)
    
    # Bill anlysis should output rates for utilites
    # Those values are then used in subsequent functions
    utility_bill = input_workbook['Utility Bills']
    annual_bill, per_kwh_cost, per_kw_peak_cost, per_therm_cost = utility_analysis(utility_bill)
    
    # Returning Cost of energy for rest of function
    bill_analysis = pd.DataFrame({
        'per_kwh_cost': [per_kwh_cost],
        'per_kw_peak_cost': [per_kw_peak_cost],
        'per_therm_cost': [per_therm_cost]
    })
    
    # Pipe Portion
    pipe_data = input_workbook['Pipe Data']
    pipe_cost_data, pipe_table_data, pipe_heat_savings = pipe_final(pipe_data, per_kw_peak_cost, per_kwh_cost, 
                     per_MMBTU_cost=None, fuel_source='Electric')
    
    len1 = 1
    len2 = len1 + len(pipe_cost_data) + 2
    len3 = len2 + len(pipe_table_data) + 2
    # End Pipe Portion
    #################
    # Air Leak
    air_leak_data = air_leak_calculation(per_kw_peak_cost, per_kwh_cost)

    writer = pd.ExcelWriter(output_path, engine = 'xlsxwriter')

    bill_analysis.to_excel(writer, sheet_name='Bill Analysis', index=False)
        
    pipe_cost_data.to_excel(writer, sheet_name='Pipe Data', index=False, startcol=1, startrow=len1)
    pipe_table_data.to_excel(writer, sheet_name= 'Pipe Data', index=False, startcol=1, startrow=len2)
    pipe_heat_savings.to_excel(writer, sheet_name = 'Pipe Data', index=False, startcol=1, startrow=len3)

    writer.close()
    return print('Process is complete')


IAC_function(input_path, output_path)