# Base for Air Leaks
import numpy as np
import pandas as pd
from SF_IAC_constants import *


def air_leak_calculation(per_kw_peak_cost, per_kw_cost):
    T_1 = (t_A - 32) * 5/9 + 273.15
    T_2 = (T_line - 32) * 5/9 + 273.15


    leak_radius = diameter_leak/2
    A_leak = (leak_radius)**2 * np.pi
    
    w_comp = (n * R * T_1) / (E_comp * (n-1)) * (((P_line/P_atm)**(1-(1/n))) - 1)
    m_air = C_dis * (2 / (K + 1))**(1/(K+1)) * (P_line *1000 / (R * T_2)) * A_leak * np.sqrt(K * R * T_2 * (2 / (K + 1)))
    
    power_loss = m_air * w_comp / 1000
    
    kw_reduction = power_loss * num_leaks
    
    total_energy_savings = kw_reduction * uptime_factory
    
    total_cost_savings = total_energy_savings * per_kw_cost + kw_reduction * per_kw_peak_cost
    
    labor_cost = labor_rate * air_fix_time * air_staff_needed
    
    implementation_cost = labor_cost + cost_ultrasonic
    
    spp_air_leak = implementation_cost / total_cost_savings * 12
    
    results =  {
        'W_comp': w_comp,
        'M_air': m_air,
        'Power Loss': power_loss,
        'Kw Reduction': kw_reduction,
        'Total Kw Savings': total_energy_savings,
        'Total Savings($)': total_cost_savings,
        'Labor Cost ($)': labor_cost,
        'Implementation Cost($)': implementation_cost,
        'SPP (months)': spp_air_leak
    }
    return results
    
    
def asDataFrame(self, results):
    df = pd.DataFrame([results])
    
    return df