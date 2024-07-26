# 7/26/24 works as expected
# Will need to be changed if different types of terms are used
# Bill Analysis
import pandas as pd
import numpy as np

#test_bill = pd.read_excel('bill_data(polycom).xlsx')
class UtilityBill:
    def __init__(self, df):
        self.data = df
        
        
    def utility_analysis(self):
        utility_bill = self.data
        
        annual_bill = utility_bill.iloc[:,1:].sum(axis=0) # columns averages
        
        per_kwh_cost = annual_bill.loc['Kwh Charge ($)'] / annual_bill.loc['Kwh Usage']
        per_kw_peak_cost = annual_bill.loc['Peak Charge ($)'] / annual_bill.loc['Peak Kw Usage']
        
        per_therm_cost = None # Initialize as null value
        if 'Natural Gas Usage (Therms)' in utility_bill.columns: #if gas is used, updates value
            per_therm_cost = annual_bill.loc['therm_charge'] / annual_bill.loc['therm_charge']
        
        energy_costs = {
            "Price per kWh ($)": per_kwh_cost,
            "Price per Peak kW ($)": per_kw_peak_cost,
            "Price per Therm ($)": per_therm_cost
        }
        return annual_bill, energy_costs

    def asDataFrame(self, results):
        df = pd.DataFrame([results])
        return df
    
    def process(self):
        annual_bill, energy_costs = self.utility_analysis()
        per_kwh_cost = energy_costs['Price per kWh ($)']
        per_hw_peak_cost = energy_costs['Price per Peak kW ($)']
        per_therm_cost = energy_costs['Price per Therm ($)']
        energy_costs_df = self.asDataFrame(energy_costs)
        annual_bill_df = self.asDataFrame(annual_bill)
        blank_col = pd.DataFrame(np.nan, index=energy_costs_df, columns=['---'])
        combined_bill_data = pd.concat([energy_costs_df, blank_col, annual_bill_df], axis=1)
        return per_kwh_cost, per_hw_peak_cost, per_therm_cost, combined_bill_data

