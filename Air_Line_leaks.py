# 7/26/24 works as expected
# Class for Air Leaks
import numpy as np
import pandas as pd

class AirLeak:
    def __init__(self, AirLeak_dict, t_A):
        self.set_const(AirLeak_dict)
        self.t_A = t_A
        
    def set_const(self, dict):
        for key, value in dict.items():
            setattr(self, key, value)
            
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
        
        total_cost_savings = total_energy_savings * self.per_kwh_cost + kw_reduction * self.per_kw_peak_cost
        
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
    
    def set_costs(self, per_kwh_cost, per_kw_peak_cost, per_therm_cost, uptime_factory):
        self.per_kw_peak_cost = per_kw_peak_cost
        self.per_kwh_cost = per_kwh_cost
        self.per_therm_cost = per_therm_cost
        self.uptime = uptime_factory
    
    def asDataFrame(self, results):
        df = pd.DataFrame([results])
        
        return df
    
    def process( dictionaries, costs):
        al_dict = dictionaries['AirLeak']
        t_A = dictionaries['FC']['t_A']
        air_leaks = AirLeak(al_dict, t_A)
        air_leaks.set_costs(*costs)
        air_leak_results = air_leaks.air_leak_calculation()
        air_leak_final = air_leaks.asDataFrame(air_leak_results)
        
        return air_leak_final