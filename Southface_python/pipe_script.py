# Zachary Delk
# SF-IAC-KSU
# Pipe script for execution 
#------------------------------------------------------------------------------------------------------------------#
# Importing needed libraries
from KSU_IAC_Functions import *
from SF_IAC_constants import *
from tabulate import tabulate
import pandas as pd

# Loading in data set
orian_pipe = pd.read_csv('Orian_pipe_data.csv')

#------------------------------------------------------------------------------------------------------------------#
# Running initial Calculator function
pipe_calculations = round(insulation_calculator(orian_pipe), 2) # Running Data through pipe calculator from KSU_IAC_functions

# Creating list of columns for the output table
pipe_table_cols = ["ID", "Description", "Location", "Diameter_inner_in", "Length_ft", "Surface_Temp", "Q non", "Q in", "Q Diff"]

# Sub-setting calculations to only columns need in the output table
pipe_table_data = pipe_calculations[pipe_table_cols]

Q_non_total = pipe_table_data['Q non'].sum() # Total Heat Loss from Non-Insulated Pipes
Q_in_total = pipe_table_data['Q in'].sum() # Estimated Total Heat Loss from Insulated Pipes
Q_diff_total = pipe_table_data['Q Diff'].sum() # Estimated Total Difference between Non-Insulated and Insulated

# Creating Heat Savings DataFrame
pipe_heat_savings = pd.DataFrame({'Non-Insulated': [round(Q_non_total, 2)],
                      'Insulated': [round(Q_in_total, 2)], 
                      'Total Savings': [round(Q_diff_total)]})

# Energy and Cost Savings for Pipe Insulation
pipe_savings_data = pipe_saving_calc(Q_diff_total, 'Gas')

# Cost Analysis
pipe_cost_data = round(pipe_cost_n_ssp(orian_pipe, pipe_savings_data), 2) 

#------------------------------------------------------------------------------------------------------------------#
# Creating spacing for Printing tables on single excel sheet
len1 = 1
len2 = len1 + len(pipe_cost_data) + 2
len3 = len2 + len(pipe_table_data) + 2

#------------------------------------------------------------------------------------------------------------------#
# Writing function
writer = pd.ExcelWriter("Pipe_data_v1.xlsx", engine = 'xlsxwriter')

pipe_cost_data.to_excel(writer, sheet_name='Pipe Data', index=False, startcol=1, startrow=len1)
pipe_table_data.to_excel(writer, sheet_name= 'Pipe Data', index=False, startcol=1, startrow=len2)
pipe_heat_savings.to_excel(writer, sheet_name = 'Pipe Data', index=False, startcol=1, startrow=len3)

writer.close()