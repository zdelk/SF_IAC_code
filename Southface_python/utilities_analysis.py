# Bill Analysis
import pandas as pd

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
        
        
        return annual_bill, per_kwh_cost, per_kw_peak_cost, per_therm_cost


