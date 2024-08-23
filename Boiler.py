# Boiler Related Classes
import numpy as np
import pandas as pd
from KSU_IAC_Functions import SFIACGeneral


class AirFuelRatio(SFIACGeneral):
    def __init__(self, dict):
        self.set_const(dict)

    def calculator(self):

        fuel_per_year = (
            self.fuel_cons_hr * self.boiler_percent * self.uptime * self.fire_percent
        )

        percent_ratio = self.eff_current / self.eff_improve

        annual_gas_save = fuel_per_year * (1 - percent_ratio)

        annual_cost = annual_gas_save * self.cost_mmbtu

        annual_person_cost = self.uptime_weeks * self.hrs_week * self.labor_cost

        net_save = annual_cost - annual_person_cost

        spp_months = self.implement_cost / net_save * 12

        output = pd.DataFrame(
            {
                "Fuel Consumption (MMbtu/year)": [round(fuel_per_year, 2)],
                "Gas Savings (MMbtu/year)": [round(annual_gas_save, 2)],
                "Cost Saving ($/year)": [round(annual_cost, 2)],
                "Personal Cost ($/year)": [round(annual_person_cost, 2)],
                "Net Savings ($/year)": [round(net_save, 2)],
                "SPP (Months)": [round(spp_months, 2)],
            }
        )

        return output

    def process(dictionaries, costs):
        ratio_dict = dictionaries["Ratio"]
        air_fuel_ratio = AirFuelRatio(ratio_dict)
        air_fuel_ratio.set_costs(*costs)
        afr_final = air_fuel_ratio.calculator()

        return afr_final

class RepairSteamLeaks(SFIACGeneral):
    def __init__(self, df, dict):
        self.leak_data = df
        self.set_const(dict)
        
    def calculator(self):
        leak_data = self.leak_data.copy()
        
        leak_bar = (self.psi_gauge + self.psi_to_abs) * self.abs_to_bar
        
        btu_per_lb = self.boiler_input / self.steam_out
        
        for i in range(len(leak_data)):
            leak_diameter = leak_data.loc[i, 'Diameter of Leak (mm)']
            
            leak_area = np.pi / 4 * (leak_diameter) ** 2
            leak_data.loc[i, 'Area of Leak Total (mm^2)'] = leak_area
            
            m_steam = self.steam_const * leak_area * leak_bar
            leak_data.loc[i, 'Leakage Rate (kg/hr)'] = m_steam
            
            energy_waste = leak_data.loc[i, 'Number of Leaks'] * m_steam * btu_per_lb * self.uptime
            leak_data.loc[i, 'Energy Waste (MMbtu/year)'] = energy_waste
            
        
        energy_save = leak_data['Energy Waste (MMbtu/year)'].sum()
        
        cost_save = energy_save * self.cost_mmbtu
        
        equip_num = leak_data['Number of Leaks'].sum()
        
        capital_cost = equip_num * self.valve_cost
        
        labor_cost = equip_num * self.man_hours * self.labor_cost
        
        implement_cost = capital_cost + labor_cost
        
        spp = implement_cost / cost_save
        spp_months = spp * 12
        
        output = pd.DataFrame({
            'Energy Savings (MMbtu/year)': [round(energy_save, 2)],
            'Cost Savings ($/year)': [round(cost_save, 2)],
            'Capital Cost ($/year)': [round(capital_cost, 2)],
            'Labor Cost ($/year)': [round(labor_cost, 2)],
            'Implementation Cost ($/year)': [round(implement_cost, 2)],
            'SPP (years)': [round(spp, 2)],
            'SPP (months)': [round(spp_months, 2)]
        })
        
        return leak_data, output
    
    def process(self, dictionaries, costs):
        steam_leak_dict = dictionaries['SteamLeak']
        steam_leak = RepairSteamLeaks(self, steam_leak_dict)
        steam_leak.set_costs(*costs)
        leak_data, cost_data = steam_leak.calculator()
        steam_leak_full = pd.concat([leak_data, cost_data], axis=1)
        
        return steam_leak_full
    
class EfficientBelts(SFIACGeneral):
    def __init__(self, dict):
        self.set_const(dict)
        
    def calculator(self):
        kw_reduce = self.eff_belt * self.num_motors * self.hp_motors * self.draw_motors * self.load_motors
        
        kwh_reduce = kw_reduce * self.uptime

        kw_save = kw_reduce * self.cost_peak * 12
        kwh_save = kwh_reduce * self.cost_kwh
        
        total_save = kw_save + kwh_save
        
        labor_cost = self.labor_cost * self.labor_time
        capital_cost = self.num_motors * self.belt_per_motor * self.belt_cost
        
        total_cost = labor_cost + capital_cost
        
        spp = total_cost / total_save
        spp_months = spp * 12
        
        output = pd.DataFrame({
            'Peak Reduction (KW)': [round(kw_reduce, 2)],
            'Annual KWh Recduction (KWh/year)': [round(kwh_reduce, 2)],
            'Annual Peak Savings ($/year)': [round(kw_save, 2)],
            'Annual KWh Savings ($/year)': [round(kwh_save, 2)],
            'Total Annual Savings ($/year)': [round(total_save, 2)],
            'Labor Cost ($)': [round(labor_cost, 2)],
            'Capital Cost ($)': [round(capital_cost, 2)],
            'Implementation Cost ($)': [round(capital_cost, 2)],
            'SPP (years)': [round(spp, 2)],
            'SPP (months)': [round(spp_months, 2)]
        })
        
        return output
    
    def process(dictionaries, costs):
        belts_dict = dictionaries['Belts']
        belts_out = EfficientBelts(belts_dict)
        belts_out.set_costs(*costs)
        belts_final = belts_out.calculator()
        
        return belts_final
    
class IsolateHotCold(SFIACGeneral):
    def __init__(self, dict):
        self.set_const(dict)
        
    def calculator(self):
        load_hours = self.load_percent * self.uptime
        unload_hours = 8760 - load_hours
        
        bhp = self.count_comp * self.hp_comp * self.conv_bhp
        
        load_heat = self.heat_percent * bhp * self.conv_factor * (self.cooling_months / 12) * load_hours
        unload_heat = self.heat_percent * self.unload_draw * bhp * self.conv_factor * (self.cooling_months / 12) * unload_hours
        
        total_heat = load_heat + unload_heat
        
        total_energy = (total_heat / self.eer_hvac) / 1000
        
        cost_save = total_energy * self.cost_kwh

        implement_cost = self.count_comp * (self.cost_takeoff + self.cost_odsensor + (self.cost_duct * self.ft_duct))
        
        spp = implement_cost / cost_save
        spp_months = spp * 12
        
        output = {
            'Load Hours (hr/year)': load_hours,
            'Unload Hours (hr/year)': unload_hours,
            'Total bhp': bhp,
            'Heat Gen:Load (Btu/year)': load_heat,
            'Heat Gen:Unload (Btu/year)': unload_heat,
            'Heat Gen:Total (Btu/year)': total_heat,
            'Energy Savings (KWh/year)': total_energy,
            'Annual Cost Savings ($/year)': cost_save,
            'Implementation Cost ($)': implement_cost,
            'SPP (years)': spp,
            'SPP (months)': spp_months
        }
        
        return output
    
    def process(dict, costs):
        isolate_dict = dict['Isolate']
        isolate = IsolateHotCold(isolate_dict)
        isolate.set_costs(*costs)
        isolate_out = isolate.calculator()
        isolate_final = isolate.asDataFrame(isolate_out)
        
        return isolate_final
    
    
class ReplaceAirFilter(SFIACGeneral):
    def __init__(self, dict):
        self.set_const(dict)
        
    def calculator(self):
        peak_reduce = self.count_units * self.avg_hp * self.hp_to_kw * self.load_reduce
        use_time = (self.months_per_year / 12) * self.uptime

        kwh_reduce = peak_reduce * use_time
        
        peak_save = peak_reduce * self.cost_peak * self.months_per_year
        kwh_save = kwh_reduce * self.cost_kwh

        total_save = peak_save + kwh_save
        
        filter_count = self.count_units * self.filter_per_unit
        capital_cost =  filter_count * self.cost_filter
        labor_cost = self.man_hours * self.cost_labor
        
        total_cost = capital_cost + labor_cost
        
        spp = total_cost / total_save
        spp_month = spp * 12
        
        output = {
            'Filters needed': filter_count,
            'Use hours (hrs/year)': use_time,
            'Peak Reduction (KW)': peak_reduce,
            'KWh Reduction (KWh/year)': kwh_save,
            'Peak Savings ($/year)': peak_save,
            'KWh Savings ($/year)': kwh_save,
            'Total Savings ($/year)': total_save,
            'Capital Cost ($)': capital_cost,
            'Labor Cost ($)': labor_cost,
            'Total Cost ($)': total_cost,
            'SPP (years)': spp,
            'SPP (months)': spp_month
        }
        
        return output
    
    def process(dict, costs):
        filter_dict = dict['AirFilter']
        filter_obj = ReplaceAirFilter(filter_dict)
        filter_obj.set_costs(*costs)
        filter_out = filter_obj.calculator()
        filter_final = filter_obj.asDataFrame(filter_out)
        
        return filter_final