# Test for main
import pandas as pd
from VSD_replacement import VSDreplace
from Replace_Lights import LEDReplacement
from utilities_analysis import UtilityBill


input_path = 'test_input.xlsx'
output_path = 'test_output.xlsx'

def main(input_path, output_path):
    input_workbook = pd.read_excel(input_path, engine = 'openpyxl', sheet_name = None)
    
    # Bill Analysis
    # Always first
    utility_bill = input_workbook['Utility Bills']
    bill_analysis = UtilityBill(utility_bill)
    
    annual_bill, per_kwh_cost, per_kw_peak_cost, per_therm_cost = bill_analysis.utility_analysis()
    print(annual_bill)
    
    # VSD replacement
    vsd_sheet = input_workbook['VSD Replacement']
    vsd_df = vsd_sheet.set_index(vsd_sheet.columns[0])
    
    vsd_replacement = VSDreplace(vsd_df)
    vsd_replacement.read_values()
    vsd_replacement.set_costs(per_kwh_cost, per_kw_peak_cost, 6240, 45000, 22500)
    vsd_results = vsd_replacement.VSDcalc()
    vsd_final = vsd_replacement.asDataFrame(vsd_results)
    print(vsd_final)
    
    led_replacement = LEDReplacement(75, 40, 1700, 6420)
    led_replacement.set_costs(per_kwh_cost, per_kw_peak_cost)
    led_results = led_replacement.LED_savings()
    led_final = led_replacement.asDataFrame(led_results)
    print(led_final)
    
    


if __name__=='__main__':
    main(input_path, output_path)