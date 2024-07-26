# 7/26/24 works as expected
# Replace Lights
import pandas as pd

# # How to use in main
#     led_replacement = LEDReplacement(75, 40, 1700, 6420)
#     led_replacement.set_costs(0.054, 13)
#     led_results = led_replacement.LED_savings()
#     led_final = led_replacement.asDataFrame(led_results)
#     print(led_final)
    

class LEDReplacement:
    def __init__(self, dict):
        self.set_const(dict)
    
    def set_const(self, dict):
        for key, value in dict.items():
            setattr(self, key, value)

    def LED_savings(self):
        peak_reduction = self.num_of_bulbs * (self.current_watts - self.led_watts) / 1000
        kwh_reduction = peak_reduction * self.uptime

        peak_cost_savings = peak_reduction * self.per_peak * 12
        kwh_cost_savings = kwh_reduction * self.per_kwh

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
            "kWh Cost Savings($)": kwh_cost_savings,
            "Reduction Savings($)": reduction_savings,
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

    def set_costs(self, per_kwh_cost, per_kw_peak_cost, per_therm_cost, uptime_factory):
        self.per_kwh = per_kwh_cost
        self.per_peak = per_kw_peak_cost
        self.per_therm = per_therm_cost
        self.uptime = uptime_factory

    def asDataFrame(self, results):
        df = pd.DataFrame([results])

        return df

    def process(dictionaries, costs):
        led_replacement = LEDReplacement(dictionaries["LED"])
        led_replacement.set_costs(*costs) 
        led_results = led_replacement.LED_savings()
        led_final = led_replacement.asDataFrame(led_results)
        
        return led_final
