# 7/26/24 works as expected
# Class for Air Leaks
import numpy as np
import pandas as pd
from KSU_IAC_Functions import SFIACGeneral

class AirLeak(SFIACGeneral):
    def __init__(self, AirLeak_dict):
        self.set_const(AirLeak_dict)
            
    def air_leak_calculation(self):
        # Unpacking a short variables for Readabiliy
        n = self.n
        R = self.R
        E_comp = self.E_comp
        P_line = self.P_line
        P_atm = self.P_atm
        C_dis = self.C_dis
        K = self.K 

        
        T_1 = (self.t_A - 32) * 5/9 + 273.15
        T_2 = (self.T_line - 32) * 5/9 + 273.15


        leak_radius = self.diameter_leak / 2
        A_leak = (leak_radius)**2 * np.pi
        
        w_comp = (n * R * T_1) / (E_comp * (n-1)) * (((P_line/P_atm)**(1-(1/n))) - 1)
        m_air = C_dis * (2 / (K + 1))**(1/(K+1)) * (P_line / (R * T_2)) * A_leak * np.sqrt(K * (R*1000)* T_2 * (2 / (K + 1))) # R*1000 to make units equal
        
        power_loss = m_air * w_comp  # in kW
        
        kw_reduction = power_loss * self.num_leaks
        
        total_energy_savings = kw_reduction * self.uptime
        
        total_cost_savings = total_energy_savings * self.cost_kwh + kw_reduction * self.cost_peak
        
        labor_cost = self.labor_rate * self.air_fix_time * self.air_staff_needed
        
        implementation_cost = labor_cost + self.cost_ultrasonic
        
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
    
    def process( dict, costs):
        air_leaks = AirLeak(dict)
        air_leaks.set_costs(*costs)
        air_leak_results = air_leaks.air_leak_calculation()
        air_leak_final = air_leaks.asDataFrame(air_leak_results)
        
        return air_leak_final
    
class ReduceAirPressure(SFIACGeneral):
    def __init__(self, dict):
        self.set_const(dict)
        
    def calculator(self):
        psi_reduced = self.psi_current - self.psi_reduce
        
        n_exp = (self.n - 1) / self.n
        
        eq_top = (psi_reduced / self.psi_input) ** (n_exp) - 1
        eq_bot = (self.psi_current / self.psi_input) ** (n_exp) - 1
        
        f_reduce = 1 - (eq_top / eq_bot)
        
        kw_comp = self.hp_comp * self.count_comp * self.hp_to_kw
        
        kw_reduce = f_reduce * kw_comp * self.load_percent * self.uptime

        cost_save = kw_reduce * self.cost_kwh
        
        implement_cost = self.cost_labor * self.hours_labor
        
        spp = implement_cost / cost_save
        spp_months = spp * 12
        
        output = {
            'Saving Factor': f_reduce,
            'Compressor Draw (KW)': kw_comp,
            'Energy Savings (KWh/year)': kw_reduce,
            'Cost Savings ($/year)': cost_save,
            'Implementation Cost ($)': implement_cost,
            'SPP (years)': spp,
            'SPP (months)': spp_months
        }
        
        return output
    
    def process(dict, costs):
        reduce_obj = ReduceAirPressure(dict)
        reduce_obj.set_costs(*costs)
        reduce_out = reduce_obj.calculator()
        reduce_final = reduce_obj.asDataFrame(reduce_out)
        
        return reduce_final
    
class TurnOffCompressor(SFIACGeneral):
    def __init__(self, dict):
        self.set_const(dict)
        
    def calculator(self):
        peak_save = self.hp_comp * self.hp_to_kw * self.unload_comp
        
        if self.off_completely == True:
            kwh_save = peak_save * self.uptime

        else:
            idle_hours = self.off_hours_per_week * 52
            kwh_save = peak_save * idle_hours
            
        kwh_cost = kwh_save * self.cost_kwh
        
        output = {
            'Peak Reduction (KW)': peak_save,
            'KWh Reduction (KW/year)': kwh_save,
            'Cost Savings ($/year)': kwh_cost,
        }
        
        return output
    
    def process(dict, costs):
        off_obj = TurnOffCompressor(dict)
        off_obj.set_costs(*costs)
        off_table = off_obj.calculator()
        off_final = off_obj.asDataFrame(off_table)
        
        return off_final