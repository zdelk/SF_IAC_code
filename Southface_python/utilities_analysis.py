# Bill Analysis
import pandas as pd

#test_bill = pd.read_excel('bill_data(polycom).xlsx')

def utility_analysis(utility_bill):
    annual_bill = utility_bill.iloc[:,1:].sum(axis=0) # columns averages
    
    per_kwh_cost = annual_bill.loc['Kwh Charge ($)'] / annual_bill.loc['Kwh Usage']
    per_kw_peak_cost = annual_bill.loc['Peak Charge ($)'] / annual_bill.loc['Peak Kw Usage']
    
    per_therm_cost = None # Initialize as null value
    if 'Natural Gas Usage (Therms)' in utility_bill.columns: #if gas is used, updates value
        per_therm_cost = annual_bill.loc['therm_charge'] / annual_bill.loc['therm_charge']
    
    return annual_bill, per_kwh_cost, per_kw_peak_cost, per_therm_cost



#print(utility_analysis(test_bill))
# # print(kwh_rate)
# # print(peak_rate)

# # Gas Calculations
# gas_usage = utility_bill["gas_usage"].sum()

# gas_cost = utility_bill["gas_cost"].sum()

# gas_rate = gas_cost / gas_usage