# Bill Analysis
import pandas as pd

utility_bill = pd.read_csv("bill_data(polycom).csv")

def utility_analysis(utility_bill):
    annual_bill = utility_bill.iloc[:,1:].sum(axis=0)
    
    per_kwh_cost = annual_bill.loc['kwh_charge'] / annual_bill.loc['kwh_usage']
    per_kw_peak_cost = annual_bill.loc['peak_charge'] / annual_bill.loc['peak_usage']
    return per_kwh_cost, per_kw_peak_cost

    
    




# # print(kwh_rate)
# # print(peak_rate)

# # Gas Calculations
# gas_usage = utility_bill["gas_usage"].sum()

# gas_cost = utility_bill["gas_cost"].sum()

# gas_rate = gas_cost / gas_usage