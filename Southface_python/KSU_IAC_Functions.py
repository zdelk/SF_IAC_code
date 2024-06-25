import pandas as pd
import numpy as np
from SF_IAC_constants import *

data = pd.read_csv('BF_pipe_data.csv')
k_data = pd.read_csv('K_values.csv')

def insulation_calculator(pipe_data, k_values = k_data):
    pipe_data = pipe_data.copy()
    
    for i in range(len(pipe_data)):
        t_p = pipe_data.loc[i, 'Surface_Temp']
        d_in = pipe_data.loc[i, 'Diameter_inner_in']
        d_out = pipe_data.loc[i, 'Diameter_outer_in']
        
        if pipe_data.loc[i, 'Length_ft'] == "RIS":
            length_pipe = length_ris
        else:
            length_pipe = float(pipe_data.loc[i, 'Length_ft'])
            
        k_val = k_values.loc[k_values['Material'] == pipe_data.loc[i, 'Material'], 'K_value'].values[0]
        
        r_out = d_out / 2
        dT = t_p - t_A
        
        d_prime_non = r_out * np.log(d_out / d_in)
        pipe_data.loc[i, "D'(non)"] = d_prime_non
        
        d_prime_in = (r_out + d_thickness) * np.log((r_out + d_thickness)/ r_out)
        pipe_data.loc[i, "D'(insulated)"] = d_prime_in
        
        r_non = d_prime_non / k_val
        r_in = d_prime_in / k_insulation
        pipe_data.loc[i, "R non_in"] = r_non
        pipe_data.loc[i, "R in"] = r_in
        
        area_non = (d_in / 12) * np.pi * length_pipe
        area_in = (d_out / 12) * np.pi * length_pipe
        pipe_data.loc[i, "Area_Non(ft^2)"] = area_non
        pipe_data.loc[i, "Area_IN(ft^2)"] = area_in
        
        u_non = 1 / (r_non + r_Air)
        u_in = 1 / (r_in + r_Air)
        pipe_data.loc[i, "U non"] = u_non
        pipe_data.loc[i, "U in"] = u_in
        
        q_non = dT * area_non * u_non
        q_in = dT * area_in * u_in
        q_diff = q_non - q_in
        pipe_data.loc[i, "Q non"] = q_non
        pipe_data.loc[i, "Q in"] = q_in
        pipe_data.loc[i, "Q Diff"] = q_diff
        
    return(pipe_data)

def pipe_saving_calc(var, fuel_source = 'None'):
    type = fuel_source
    btu_per_hour_loss = var
    if type == 'Gas':
        annual_btu_loss = btu_per_hour_loss * uptime_factory
        
        MMBtu_savings = annual_btu_loss * boiler_efficiency * 10**(-6)
        
        annual_cost_saving = MMBtu_savings * per_MMBTU_cost
        
        my_table = pd.DataFrame[('Heat_Loss_Savings_Per_Hour','Annual_Heat_Loss_Savings', 'Annual_MMBTU_Savings','Annual_Cost_Savings'),
                    (round(var, 2), round(annual_btu_loss, 2), round(MMBtu_savings, 2), round(annual_cost_saving, 2))]
        output = my_table
    
    elif type == 'Electric':
        peak_reduction = btu_per_hour_loss / 3412
        annual_peak_reduction = peak_reduction * 12
        annual_kwh_reduction = peak_reduction * uptime_factory
        
        per_kw_savings = annual_peak_reduction * per_kw_peak_cost
        peak_savings = annual_kwh_reduction * per_kwh_cost
        annual_cost_saving = per_kw_savings + peak_savings

        my_table = pd.DataFrame[('Heat_Loss_Savings_Per_Hour', 'Peak_Demand_Reduction', 'Annual_Peak_Demand_Reduction', 
                     'Annual_KWh_Reduction', 'Cost_Savings_Peak', 'Cost_Savings_KWh', 'Annual_Cost_Savings'),
                    (round(var, 2), round(peak_reduction, 2), round(annual_peak_reduction, 2), round(annual_kwh_reduction, 2),
                     round(peak_savings, 2), round(per_kw_savings, 2), round(annual_cost_saving, 2))]
        output = my_table
    else:
        output = "Is the system Gas or Electric"
    return(output)

#def pipe_cost_n_ssp