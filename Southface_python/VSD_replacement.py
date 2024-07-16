# Compressor Replacement
import numpy as np
import pandas as pd

# # How to use in Main():
#     vsd_sheet = input_workbook['VSD Replacement']
#     vsd_df = vsd_sheet.set_index(vsd_sheet.columns[0])

#     vsd_replacement = VSDreplace(vsd_df)
#     vsd_replacement.read_values()
#     vsd_replacement.set_costs(per_kwh_cost, per_kw_peak_cost, uptime_factory, 4500, 22500)
#     vsd_results = vsd_replacement.VSDcalc()
#     vsd_final = vsd_replacement.asDataFrame(vsd_results)
#     print(vsd_final)


class VSDreplace:
    def __init__(self, df, dict):
        self.data = df
        self.set_const(dict)

    def read_values(self):
        self.pre_values = self.data.loc["Pre"]
        self.post_values = self.data.loc["Post"]
    
    def set_const(self, dict):
        for key, value in dict.items():
            setattr(self, key, value)
        

    def VSDcalc(self):
        pre_motor_hp = self.pre_values["Motor Hp"]
        pre_motor_eff = self.pre_values["Motor Efficiency"]
        pre_comp_load_1 = self.pre_values["Load Consumption"]
        pre_comp_load_2 = self.pre_values["Unload Consumption"]

        post_motor_hp = self.post_values["Motor Hp"]
        post_motor_eff = self.post_values["Motor Efficiency"]
        post_comp_load_1 = self.post_values["Load Consumption"]
        post_comp_load_2 = self.post_values["Unload Consumption"]

        pre_load_1 = pre_motor_hp * self.const * pre_comp_load_1 * 1 / pre_motor_eff
        pre_load_2 = pre_motor_hp * self.const * pre_comp_load_2 * 1 / pre_motor_eff

        pre_total = pre_load_1 + pre_load_2

        post_load_1 = post_motor_hp * self.const * post_comp_load_1 * 1 / post_motor_eff
        post_load_2 = post_motor_hp * self.const * post_comp_load_2 * 1 / post_motor_eff

        post_total = post_load_1 + post_load_2

        peak_kw_savings = pre_total - post_total

        annual_kw_savings = peak_kw_savings * self.uptime / 2

        peak_cost_savings = peak_kw_savings * self.cost_peak
        kw_cost_savings = annual_kw_savings * self.cost_kw

        total_savings = peak_cost_savings + kw_cost_savings

        implement_cost = self.vsd_cost + self.labor_cost

        spp = implement_cost / total_savings * 12

        results = {
            "Pre Loaded Cons(KW)": pre_load_1,
            "Pre Unloaded Cons(KW)": pre_load_2,
            "Pre Total Cons(KW)": pre_total,
            "Post Loaded Cons(KW)": post_load_1,
            "Post Unloaded Cons(KW)": post_load_2,
            "Post Total Cons(KW)": post_total,
            "Peak KW Savings": peak_kw_savings,
            "Annual KWh Savings": annual_kw_savings,
            "Peak KW Cost Savings($)": peak_kw_savings,
            "Annual KWh Cost Savings($)": annual_kw_savings,
            "Total Savings($)": total_savings,
            "Capitol Cost($)": self.vsd_cost,
            "Labor Cost($)": self.labor_cost,
            "Implementation Cost($)": implement_cost,
            "SPP (Months)": spp,
        }

        return results

    def set_costs(
        self, per_kwh_cost, per_kw_peak_cost, uptime_factory
    ):
        self.cost_peak = per_kw_peak_cost
        self.cost_kw = per_kwh_cost
        self.uptime = uptime_factory

    def asDataFrame(self, results):
        df = pd.DataFrame([results])
        return df
