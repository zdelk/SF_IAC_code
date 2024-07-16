# Replace Lights
import pandas as pd

# # How to use in main
#     led_replacement = LEDReplacement(75, 40, 1700, 6420)
#     led_replacement.set_costs(0.054, 13)
#     led_results = led_replacement.LED_savings()
#     led_final = led_replacement.asDataFrame(led_results)
#     print(led_final)
    

class LEDReplacement:
    def __init__(self, current_watts, led_watts, num_of_bulbs, uptime_factory):
        self.c_watts = current_watts
        self.l_watts = led_watts
        self.num_bulbs = num_of_bulbs
        self.uptime = uptime_factory

        self.led_hours = 50000
        self.fluor_hours = 24000
        self.ballist_hours = 40000

        self.fluor_cost = 9.21
        self.fluor_labor = 6.67
        self.ballast_cost = 11.96

        self.led_fix_cost = 142
        self.led_bulb_cost = 13.90

    def LED_savings(self):
        peak_reduction = self.num_bulbs * (self.c_watts - self.l_watts) / 1000
        kwh_reduction = peak_reduction * self.uptime

        peak_cost_savings = peak_reduction * self.per_peak * 12
        kwh_cost_savings = kwh_reduction * self.per_kwh

        reduction_savings = peak_cost_savings + kwh_cost_savings

        led_lifespan = self.led_hours / self.uptime
        fluor_lifespan = self.fluor_hours / self.uptime
        ballast_lifespan = self.ballast_cost / self.uptime

        fluor_rep_cycles = fluor_lifespan / led_lifespan
        ballast_rep_cycles = ballast_lifespan / led_lifespan

        fluor_savings_8 = (
            fluor_rep_cycles * (self.fluor_cost + self.fluor_labor)
            + ballast_rep_cycles * self.ballast_cost
        ) * self.num_bulbs

        fluor_savings = fluor_savings_8 / led_lifespan

        total_savings = fluor_savings + reduction_savings

        imp_cost = self.num_bulbs * (
            self.led_bulb_cost + self.led_fix_cost / 2 + self.fluor_labor
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

    def set_costs(self, per_kwh_cost, per_kw_peak_cost):
        self.per_kwh = per_kwh_cost
        self.per_peak = per_kw_peak_cost

    def asDataFrame(self, results):
        df = pd.DataFrame([results])

        return df
