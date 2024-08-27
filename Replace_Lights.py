# 7/26/24 works as expected
# Replace Lights
import pandas as pd
from KSU_IAC_Functions import SFIACGeneral
# # How to use in main
#     led_replacement = LEDReplacement(75, 40, 1700, 6420)
#     led_replacement.set_costs(0.054, 13)
#     led_results = led_replacement.LED_savings()
#     led_final = led_replacement.asDataFrame(led_results)
#     print(led_final)
    

class LEDReplacement(SFIACGeneral):
    def __init__(self, dict):
        self.set_const(dict)


    def LED_savings(self):
        peak_reduction = self.num_of_bulbs * (self.current_watts - self.led_watts) / 1000
        kwh_reduction = peak_reduction * self.uptime

        peak_cost_savings = peak_reduction * self.cost_peak * 12
        kwh_cost_savings = kwh_reduction * self.cost_kwh

        reduction_savings = peak_cost_savings + kwh_cost_savings

        led_lifespan = self.led_hours / self.uptime
        fluor_lifespan = self.fluor_hours / self.uptime
        ballast_lifespan = self.ballast_hours / self.uptime

        fluor_rep_cycles = led_lifespan /fluor_lifespan
        ballast_rep_cycles = led_lifespan / ballast_lifespan

        fluor_savings_8 = (
            fluor_rep_cycles * (self.fluor_cost + self.labor_cost)
            + ballast_rep_cycles * self.ballast_cost
        ) * self.num_of_bulbs

        fluor_savings = fluor_savings_8 / led_lifespan

        total_savings = fluor_savings + reduction_savings

        imp_cost = self.num_of_bulbs * (
            self.led_bulb_cost + self.led_fix_cost / 2 + self.labor_cost
        )

        spp = imp_cost / total_savings * 12

        results = {
            "Monthly Peak kW Reduction": peak_reduction,
            "Annual kWh Savings": kwh_reduction,
            "Peak Cost Savings": peak_cost_savings,
            "kWh Cost Savings ($)": kwh_cost_savings,
            "Reduction Savings ($)": reduction_savings,
            "Led Lifespan (years)": led_lifespan,
            "Replacement Cycles Bulbs (years)": fluor_rep_cycles,
            "Replacement Cycles Ballast (years)": ballast_rep_cycles,
            "Cost Avoidance total ($)": fluor_savings_8,
            "Annual Cost Avoidance ($)": fluor_savings,
            "Total Savings($)": total_savings,
            "Implementation Cost ($)": imp_cost,
            "SPP months": spp,
        }

        return results


    def process(dict, costs):
        led_replacement = LEDReplacement(dict)
        led_replacement.set_costs(*costs) 
        led_results = led_replacement.LED_savings()
        led_final = led_replacement.asDataFrame(led_results)
        
        return led_final

class OccupancySensor(SFIACGeneral):
    def __init__(self, dict):
        self.set_const(dict)
    
            
    def occ_savings(self):
        total_bulb_count = self.bulb_per_fix * self.fix_count
        
        kwh_reduction = total_bulb_count * self.bulb_watt * (1/1000) * self.uptime * self.savings_var
        
        kwh_cost_savings = kwh_reduction * self.cost_kwh
        
        capitol = self.fix_count * self.sensor_cost
        labor = self.fix_count * self.labor_cost
        
        imp_cost = capitol + labor
        
        spp = imp_cost / kwh_cost_savings * 12
        
        results = {
            "Annual kWh Savings": kwh_reduction,
            "kWh Cost Savings ($)": kwh_cost_savings,
            "Capital Cost ($)": capitol,
            "Labor Cost ($)": labor,
            "Implementation Cost ($)": imp_cost,
            "SPP months": spp,
        }
        
        return results


    def process(dict, costs):
        occupancy_sensor = OccupancySensor(dict)
        occupancy_sensor.set_costs(*costs)
        os_results = occupancy_sensor.occ_savings()
        os_final = occupancy_sensor.asDataFrame(os_results)
        
        return os_final
    

class DaylightSensor(SFIACGeneral):
    def __init__(self,dict):
        self.set_const(dict)
    
    def daylight_savings(self):
        total_bulb_count = self.bulb_per_fix * self.fix_count
        
        kwh_reduction = total_bulb_count * self.bulb_watt * (1/1000) * self.uptime * self.savings_var
        
        kwh_cost_savings = kwh_reduction * self.cost_kwh
        
        capitol = self.fix_count * self.sensor_cost
        labor = self.fix_count * self.labor_cost
        
        imp_cost = capitol + labor
        
        spp = imp_cost / kwh_cost_savings * 12
        
        results = {
            "Annual kWh Savings": kwh_reduction,
            "kWh Cost Savings ($)": kwh_cost_savings,
            "Capital Cost ($)": capitol,
            "Labor Cost ($)": labor,
            "Implementation Cost ($)": imp_cost,
            "SPP months": spp,
        }
        
        return results
    

    def process(dict, costs):
        daylight_sensor = DaylightSensor(dict)
        daylight_sensor.set_costs(*costs)
        daylight_results = daylight_sensor.daylight_savings()
        daylight_final = daylight_sensor.asDataFrame(daylight_results)
        
        return daylight_final       