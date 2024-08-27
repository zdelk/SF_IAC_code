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
input_path = "../Data/WS_input.xlsx"
input_text = "../Data/KS2434_WS.txt"
output_path = "../Data/WS_out_v1.xlsx" # Set to not overwrite

# Main Function

def main(input_path, input_text, output_path):
    print_dict = {}
    # Loading input workbook
    input_workbook = pd.read_excel(input_path, engine="openpyxl", sheet_name=None)
    
    dictionaries, section_names = dictionary_2(input_text)
    # print(dictionaries)
    uptime_factory = dictionaries['FC']['uptime_factory']
    t_A = dictionaries['FC']['t_A']
    # Bill Analysis
    # !!!!!Always first!!!!!
    ub_sheet = input_workbook["Utility Bills"]
    utillity_bill = UtilityBill(ub_sheet)
    per_kwh_cost, per_kw_peak_cost, per_therm_cost, per_mmbtu_cost, combined_bill_data = utillity_bill.process()
    
    print_dict['Utility Bills'] = combined_bill_data
    
    costs = (per_kwh_cost, per_kw_peak_cost, per_therm_cost, per_mmbtu_cost, uptime_factory, t_A)
    
    section_to_class_map = {
        'AirLeak': ('Air_Line_leaks', 'AirLeak'),
        'SteamPipe': ('Pipe_insulation', 'PipeInsulation'),
        'CondensatePipe': ('Pipe_insulation', 'PipeInsulation'),
        'Door': ('Pipe_insulation', 'OvenDoorInsulation'),
        'Tank':('Pipe_insulation', 'TankInsulation'),
        'LED': ('Replace_Lights', 'LEDReplacement'),
        'Occupancy': ('Replace_Lights', 'OccupancySensor'),
        'Daylight': ('Replace_Lights', 'DaylightSensor'),
        'VSD': ('VSD_replacement', 'VSDreplace'),
        'Micro': ('Microturbine_CHP', 'Microturbine'),
        'Ratio': ('Boiler', 'AirFuelRatio'),
        'SteamLeak': ('Boiler', 'RepairSteamLeaks'),
        'Belts': ('Boiler', 'EfficientBelts'),
        'Isolate':('Boiler', 'IsolateHotCold'),
        'ReduceAir':('Air_Line_leaks', 'ReduceAirPressure'),
        'OffComp': ('Air_Line_leaks', 'TurnOffCompressor'),
        'AirFilter':('Boiler', 'ReplaceAirFilter'),
        'NEMA': ('Boiler', 'ReplaceElectricMotors'),
        'HVAC': ('Boiler', 'ReplaceHvacUnits')
    }

    
    sheet_list = list(input_workbook.keys())
    print(sheet_list)
    
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
            output = cls.process(input_workbook[sheet_name], dictionaries[name], costs)
        else:
            print(f'{name} does not have a sheet in the workbook')
            output = cls.process(dictionaries[name], costs)
        
        
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
    main(input_path, input_text, output_path)
