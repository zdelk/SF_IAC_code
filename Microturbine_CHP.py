import numpy as np
import pandas as pd

class Microturbine:
    def __init__(self, dict):
        self.set_const(dict)
        
    def set_const(self, dict):
        for key, value in dict.items():
            setattr(self, key, value)
            
    def microturbine_calc(self):
        chp_input = self.mt_power / self.energy_eff * 3412
        
        chp_usable_heat = chp_input * self.heat_eff
        
        displaced_boiler_fuel = chp_usable_heat / self.boiler_efficiency
        
        energy_chargeable = (chp_input - displaced_boiler_fuel) / self.mt_power
        
        annual_extra_gas = self.mt_count * (chp_input - energy_chargeable) * self.uptime / 1000000
        
        annual_energy_gen = self.mt_count * self.mt_power * self.uptime
        
        # Savings Calculations
        
        annual_kwh_cost_savings = self.cost_kwh * annual_energy_gen
        
        #!!!! Edit for mmbtu or therm
        # if self.cost_per_mmbtu != 0:
        #     annual_gas_cost = self.cost_per_mmbtu * annual_extra_gas
        # else:
        #     annual_gas_cost = self.cost_per_therm * annual_extra_gas * 10
        ###
        annual_gas_cost = self.cost_therm * annual_extra_gas * 10
        ###
        annual_maintenance = self.mt_count * self.maint_cost
        
        total_savings = annual_kwh_cost_savings - annual_gas_cost - annual_maintenance
        
        # Cost Calculations
        
        capital_costs = self.mt_count * self.mt_cost
        labor_costs = self.mt_count * self.mt_labor
        
        imp_cost = capital_costs + labor_costs
        
        spp = imp_cost / total_savings * 12
        
        results = {
            "CHP Input (Btu/hr)": chp_input,
            "Usable Heat (Btu/hr)": chp_usable_heat,
            "Displaced Boiler Fuel (Btu/hr)": displaced_boiler_fuel,
            "Energy Chargeable (Btu/kWh)": energy_chargeable,
            "Annual Extra NG (MMBtu)": annual_extra_gas,
            "Annual Energy Gen (kWh)": annual_energy_gen,
            "Annual kWh Cost Savings ($)": annual_kwh_cost_savings,
            "Annual Extra Gas Cost ($)": annual_gas_cost,
            "Annual Maintenance Costs ($)": annual_maintenance,
            "Total Annual Savings ($)": total_savings,
            "Capital Cost ($)": capital_costs,
            "Labor Cost ($)": labor_costs,
            "Implementation Cost": imp_cost,
            "SPP (months)": spp
        }
        
        return results
    

    def set_costs(self, per_kwh_cost, per_kw_peak_cost, per_therm_cost, per_mmbtu_cost, uptime_factory):
        self.cost_peak = per_kw_peak_cost
        self.cost_kwh = per_kwh_cost
        self.cost_therm = per_therm_cost
        self.cost_mmbtu = per_mmbtu_cost
        self.uptime = uptime_factory
    
    def asDataFrame(self, results):
        df = pd.DataFrame([results])
        return df
    

    def process(dictionaries, costs):
        microturbine_chp = Microturbine(dictionaries['Micro'])
        microturbine_chp.set_costs(*costs)
        microturbine_results = microturbine_chp.microturbine_calc()
        microturbine_final = microturbine_chp.asDataFrame(microturbine_results)
        
        return microturbine_final       