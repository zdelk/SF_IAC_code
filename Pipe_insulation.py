# 7/26/24 works as expected
import pandas as pd
import numpy as np

# To Use in main():

class Insulation:
    def __init__(self, dictionaries):
        insul_dict = dictionaries['Insul']
        self.set_const(insul_dict)
        
    def set_const(self, dict):
        for key, value in dict.items():
            setattr(self, key, value)
            
    def set_costs(self, per_kwh_cost, per_kw_peak_cost, per_therm_cost, per_mmbtu_cost, uptime_factory):
        self.cost_peak = per_kw_peak_cost
        self.cost_kwh = per_kwh_cost
        self.cost_therm = per_therm_cost
        self.cost_mmbtu = per_mmbtu_cost
        self.uptime = uptime_factory
        
    def asDataFrame(self, results):
        df = pd.DataFrame([results])
        return df
    
class PipeInsulation(Insulation):

    def __init__(self, pipe_data, pipe_dict, t_A):
        self.pipe_data = pipe_data
        self.t_A = t_A
        self.set_const(pipe_dict)

    def insulation_calculator(self):
        pipe_data = self.pipe_data.copy()
        #k_values = self.k_values.copy()
        k_val_path = "../Data/K_values.csv"
        k_values = pd.read_csv(k_val_path)
            
        for i in range(len(pipe_data)):
            # Assigning data from table to variables for ease of use
            t_p = pipe_data.loc[i, "Surface_Temp"]
            d_in = pipe_data.loc[i, "Diameter_inner_in"]
            d_out = pipe_data.loc[i, "Diameter_outer_in"]
            unit_count = pipe_data.loc[i, "Amount_of_Fittings"]

            # Checks if length of the pipe is 'RIS' (indicating special fitting)
            # If so, uses standard ris length. Else, converts length value to float
            if pipe_data.loc[i, "Length_ft"] == "RIS":
                length_pipe = self.length_ris
            else:
                length_pipe = float(pipe_data.loc[i, "Length_ft"])

            # Pulling K_val for the specific material from the k_value CSV file
            k_val = k_values.loc[
                k_values["Material"] == pipe_data.loc[i, "Material"], "K_value"
            ].values[0]

            r_out = d_out / 2  # Radius of pipe
            dT = t_p - self.t_A  # Delta T (Temperature Difference)

            d_prime_non = r_out * np.log(d_out / d_in)  # d'(Non-insulated)
            pipe_data.loc[i, "D'(non)"] = d_prime_non

            d_prime_in = (r_out + self.d_thickness) * np.log(
                (r_out + self.d_thickness) / r_out
            )  # d'(Insulated)
            pipe_data.loc[i, "D'(insulated)"] = d_prime_in

            r_non = d_prime_non / k_val  # thermal resistance (Non-insulated)
            r_in = d_prime_in / self.k_insulation  # thermal resistance (Insulated)
            pipe_data.loc[i, "R non_in"] = r_non
            pipe_data.loc[i, "R in"] = r_in

            area_non = (
                (d_in / 12) * np.pi * length_pipe
            )  # Lateral Surface Area(Non-insulated)
            area_in = (
                (d_out / 12) * np.pi * length_pipe
            )  # Lateral Surface Area(Insulated)
            pipe_data.loc[i, "Area_Non(ft^2)"] = area_non
            pipe_data.loc[i, "Area_IN(ft^2)"] = area_in

            u_non = 1 / (r_non + self.r_Air)  # Thermal transmittance(Non-insulated)
            u_in = 1 / (r_in + self.r_Air)  # Thermal transmittance(Insulated)
            pipe_data.loc[i, "U non"] = u_non
            pipe_data.loc[i, "U in"] = u_in

            q_non = dT * area_non * u_non  # Quantity of heat(Non-insulated)
            q_in = dT * area_in * u_in  # Quantity of heat(Insulated)
            q_diff = q_non - q_in  # Quantity of heat(Difference)
            pipe_data.loc[i, "Q non"] = q_non * unit_count
            pipe_data.loc[i, "Q in"] = q_in * unit_count
            pipe_data.loc[i, "Q Diff"] = q_diff * unit_count

        return pipe_data

    # -----------------------------------------------------------------------------------------------------#
    # ---------------------------------Pipe Heat and Cost Savings Calculator-------------------------------#
    # -----------------------------------------------------------------------------------------------------#
    # Calculates overall Heat Loss
    # Uses that to calculate relevant saving info
    # Also give overall cost savings
    def pipe_saving_calc(self, var):
        type = self.type  # Boiler could be Gas or Electric
        btu_per_hour_loss = var  # Reassign for readability
        if type == "Gas":  # If boiler is Gas
            annual_btu_loss = btu_per_hour_loss * self.uptime  # Getting annual BTU loss
            # Converting to MMBtu(generally it is billed)
            MMBtu_savings = (
                annual_btu_loss / self.boiler_efficiency * 10 ** (-6)
            )  # Note the efficiency

            annual_cost_saving = MMBtu_savings * self.cost_therm  # Annual Savings

            my_table = pd.DataFrame(
                {  # Creating data frame if Gas system
                    "Heat_Loss_Savings_Per_Hour": [round(var, 2)],
                    "Annual_Heat_Loss_Savings": [round(annual_btu_loss)],
                    "Annual_MMBTU_Savings": [round(MMBtu_savings, 2)],
                    "Annual_Cost_Savings": [round(annual_cost_saving, 2)],
                }
            )
            output = my_table

        elif type == "Electric":  # If boiler is Electric
            peak_reduction = btu_per_hour_loss / 3412  # Btu to Kw conversion
            annual_peak_reduction = peak_reduction * 12  # Yearly Peak Savings(KW)
            annual_kwh_reduction = (
                peak_reduction * self.uptime
            )  # Yearly Kwh Savings(Kwh) Note no efficiency

            peak_savings = (
                annual_peak_reduction * self.cost_peak
            )  # Yearly Peak Savings($)
            kwh_savings = (
                annual_kwh_reduction * self.cost_kwh
            )  # Yearly Kwh Savings($)
            annual_cost_saving = peak_savings + kwh_savings  # Annual Savings($)

            my_table = pd.DataFrame(
                {  # Creating dataframe if Electric System
                    "Heat_Loss_Savings_Per_Hour": [round(var, 2)],
                    "Peak_Demand_Reduction": [round(peak_reduction, 2)],
                    "Annual_Peak_Demand_Reduction": [round(annual_peak_reduction, 2)],
                    "Annual_KWh_Reduction": [round(annual_kwh_reduction, 2)],
                    "Cost_Savings_Peak": [round(peak_savings, 2)],
                    "Cost_Savings_KWh": [round(kwh_savings, 2)],
                    "Annual_Cost_Savings": [round(annual_cost_saving, 2)],
                }
            )
            output = my_table
        else:
            output = "Is the system Gas or Electric?"  # If system isn't Specified
        return output

    # -----------------------------------------------------------------------------------------------------#
    # ---------------------------------Pipe Implementation Cost and SPP------------------------------------#
    # -----------------------------------------------------------------------------------------------------#
    # Calculated relevant implementation costs and SPP
    def pipe_cost_n_ssp(self, savings_data):
        pipe_data = self.pipe_data.copy()
        count_RIS = 0  # Initialize number of Special Fittings
        total_feet = 0  # Initialize total length of pipe (ft)
        annual_savings = savings_data["Annual_Cost_Savings"][
            0
        ]  # Pulling Annual Cost Savings from table

        for i in range(len(pipe_data)):  # Counts number of special fitting
            if pipe_data.loc[i, "Length_ft"] == "RIS":
                count_RIS += pipe_data.loc[i, "Amount_of_Fittings"]
            else:  # Also calculates total length of pipe to be insulated
                total_feet += float(pipe_data.loc[i, "Length_ft"])

        # Self-explanatory variables
        labor_hours = total_feet * self.pipe_manhour_conversion
        labor_cost = labor_hours * self.pipe_manhour_rate
        insulation_cost = total_feet * self.pipe_mat_cost
        special_cover_cost = count_RIS * self.pipe_sf_cost
        implementation_cost = labor_cost + insulation_cost + special_cover_cost
        spp_years = implementation_cost / annual_savings
        spp_months = round(spp_years * 12, 1)

        output_table = pd.DataFrame(
            {  # Data frame for all data from function
                "Total Feet": [round(total_feet, 2)],
                "# of Special Fittings": [count_RIS],
                "Total Labour Hours": [labor_hours],
                "Labor Cost": [labor_cost],
                "Insulation Cost": [insulation_cost],
                "Special Covers Cost": [special_cover_cost],
                "Implementation Cost": [implementation_cost],
                "SSP (years)": [spp_years],
                "SPP (months)": [spp_months],
            }
        )

        return output_table

    # -----------------------------------------------------------------------------------------------------#
    # ---------------------------------Final Function to Call in Processor---------------------------------#
    # -----------------------------------------------------------------------------------------------------#
    def pipe_final(self):
        # Running initial Calculator function
        pipe_data = self.pipe_data.copy()
        pipe_calculations = round(
            self.insulation_calculator(), 2
        )  # Running Data through pipe calculator from KSU_IAC_functions

        # Creating list of columns for the output table
        pipe_table_cols = [
            "ID",
            "Description",
            "Location",
            "Diameter_inner_in",
            "Length_ft",
            "Surface_Temp",
            "Q non",
            "Q in",
            "Q Diff",
        ]

        # Sub-setting calculations to only columns need in the output table
        pipe_table_data = pipe_calculations[pipe_table_cols]

        Q_non_total = pipe_table_data[
            "Q non"
        ].sum()  # Total Heat Loss from Non-Insulated Pipes
        Q_in_total = pipe_table_data[
            "Q in"
        ].sum()  # Estimated Total Heat Loss from Insulated Pipes
        Q_diff_total = pipe_table_data[
            "Q Diff"
        ].sum()  # Estimated Total Difference between Non-Insulated and Insulated

        # Creating Heat Savings DataFrame
        pipe_heat_savings = pd.DataFrame(
            {
                "Non-Insulated": [round(Q_non_total, 2)],
                "Insulated": [round(Q_in_total, 2)],
                "Total Savings": [round(Q_diff_total)],
            }
        )

        # Energy and Cost Savings for Pipe Insulation
        pipe_savings_data = self.pipe_saving_calc(Q_diff_total)

        # Cost Analysis
        pipe_cost_data = round(self.pipe_cost_n_ssp(pipe_savings_data), 2)

        return pipe_cost_data, pipe_table_data, pipe_heat_savings, pipe_savings_data

    
    def process(self, dictionaries, costs):
        pipe_dict = dictionaries['Pipe']
        t_A = dictionaries['FC']['t_A']
        pipe_insulation = PipeInsulation(self, pipe_dict, t_A)
        pipe_insulation.set_costs(*costs)
        pipe_cost_data, pipe_table_data, pipe_heat_savings, pipe_savings_data = pipe_insulation.pipe_final()
        pipe_full = pd.concat([pipe_cost_data, pipe_table_data, pipe_heat_savings, pipe_savings_data], axis=1)
        
        return pipe_full

class OvenDoorInsulation(Insulation):
    
    def __init__(self, door_data, door_dict, t_A):
        self.door_data = door_data
        self.t_A = t_A
        self.set_const(door_dict)

            
    def calculator(self):
        k_val_path = "../Data/K_values.csv"
        k_values = pd.read_csv(k_val_path)
        door_data = self.door_data.copy()
        
        for i in range(len(self.door_data)):
            
            t_p = door_data.loc[i, "Surface_Temp"]
            door_length = door_data.loc[i, "Length (ft)"]
            door_width = door_data.loc[i, "Width (ft)"]
            door_thick = door_data.loc[i, "Thickness (ft)"]
            door_count = door_data.loc[i, "Number of Doors"]
            print(door_count)
            dT = t_p - self.t_A
            
            k_door = k_values.loc[k_values["Material"] == door_data.loc[i, "Material"], "K_value"].values[0]

            print(k_door)
            
            R_door = door_thick / k_door
            door_data.loc[i, "R door"] = R_door
            
            R_in = self.thick_insul / self.K_insul
            door_data.loc[i, "R insul"] = R_in
            
            U_non = 1 / (R_door + self.R_surface)
            U_in = 1 / (R_door + R_in)
            
            door_data.loc[i, "U non"] = U_non
            door_data.loc[i, "U in"] = U_in
            
            A_total = door_length * door_width * door_count
            A_use = 2*door_thick * (door_length + door_width - 2*door_thick)
            door_data.loc[i, "Area Total (ft^2)"] = A_total
            door_data.loc[i, "Area Used (ft^2)"] = A_use
            
            q_non = dT * A_use * U_non
            q_in = dT * A_use * U_in
            q_diff = q_non - q_in
            door_data.loc[i, "Q non"] = q_non
            door_data.loc[i, "Q in"] = q_in
            door_data.loc[i, "Q diff"] = q_diff
            print("Q_diff: ", q_diff)
            
            
        area_total = door_data["Area Total (ft^2)"].sum()
        q_non_total = door_data["Q non"].sum()
        q_in_total = door_data["Q in"].sum()
        q_diff_total = door_data["Q diff"].sum()
        print(q_diff_total)
        print(q_non_total)
        print(q_in_total)
        
        heat_table = pd.DataFrame({
            "Heat Loss non-insul (BTU/hr)": [round(q_non_total,2)],
            "Heat Loss insul (BTU/hr)": [round(q_in_total,2)],
            "Heat Loss Diff. (BTU/hr)": [round(q_diff_total,2)]
        })
        
        if self.type == 'Gas':
            annual_btu = q_diff_total * self.uptime
            MMbtu_savings = annual_btu / self.boiler_efficency * 10**(-6)
            MMbtu_cost_save = MMbtu_savings * self.mmbtu_cost
            
            my_table = pd.DataFrame({
                "Heat Loss (BTU/hr)": [q_diff_total],
                "Heat Loss (BTU/year)": [annual_btu],
                "Heat Loss (MMBTU/year)": [MMbtu_savings],
                "MMBTU Cost Saving ($/yr)": [MMbtu_cost_save],
            })
            
            savings_table = my_table
            
        elif self.type == 'Electric':
            peak_reduce = q_diff_total / 3412
            annual_peak_reduce = peak_reduce * 12
            annual_kwh_reduce = peak_reduce * self.uptime
            
            peak_save = annual_peak_reduce * self.cost_peak
            kwh_save = annual_kwh_reduce * self.cost_kwh
            
            total_savings = peak_save + kwh_save
            
            my_table = pd.DataFrame({
                "Heat Loss (BTU/hr)": [q_diff_total],
                "Peak Reduction (KW)": [peak_reduce],
                "Annual Peak Reduction (KW/year)": [annual_peak_reduce],
                "Annual KWh Reduction (KWh/year)": [annual_kwh_reduce],
                "Peak Savings ($/year)": [peak_save],
                "KWh Savings ($/year)": [kwh_save],
                "Total Savings ($/year)": [total_savings]
            })
            
            savings_table = my_table
        
        else:
            savings_table = "Is system 'Gas' or 'Electric'"
            
        capital_cost = area_total * self.insul_cost
        
        labor_cost = capital_cost * self.labor_factor
        
        implment_cost = capital_cost + labor_cost
        
        spp = implment_cost / total_savings
        spp_months = spp * 12
        
        cost_table = pd.DataFrame({
            "Insulation Needed (ft^2)": [area_total],
            "Capital Cost ($)": [capital_cost],
            "Labor Cost ($)": [labor_cost],
            "Implementation Cost ($)": [implment_cost],
            "SPP (year)": [spp],
            "SPP (months)": [spp_months]
        })
        
        return door_data, heat_table, savings_table, cost_table

    
    def process(self, dictionaries, costs):
        door_dict = dictionaries['Door']
        t_A = dictionaries['FC']['t_A']
        door_insulation = OvenDoorInsulation(self, door_dict, t_A)
        door_insulation.set_costs(*costs)
        door_data, heat_table, savings_table, cost_table = door_insulation.calculator()
        door_full = pd.concat([door_data, heat_table, savings_table, cost_table], axis=1)
        
        return door_full
    
class TankInsulation(Insulation):
    def __init__(self, tank_dict):
        self.set_const(tank_dict)
        
        
    def calculator(self):
        tank_area = np.pi * self.tank_diameter * (self.tank_length + self.tank_diameter/2) * self.tank_count
        
        heat_loss = self.esf * tank_area
        
        if self.type == 'Gas':
            annual_energy_save = heat_loss * self.uptime / self.boiler_efficiency * 10**(-6)
            total_savings = annual_energy_save * self.cost_mmbtu
            
            savings_table = pd.DataFrame({
                'Heat Loss (BTU/hr)': [round(heat_loss, 2)],
                'Heat Loss Annual w/eff (MMBTU/year)': [round(annual_energy_save, 2)],
                'Cost Savings ($/year)': [round(total_savings, 2)]
            })
            
        elif self.type == 'Electric':
            peak_reduce = heat_loss / 3412
            annual_peak_save = peak_reduce * 12
            annual_kwh_save = peak_reduce * self.uptime
            
            annual_peak_cost = annual_peak_save * self.cost_peak
            annual_kwh_cost = annual_kwh_save * self.cost_kwh
            total_savings = annual_peak_cost + annual_kwh_cost
            
            savings_table = pd.DataFrame({
                'Heat Loss (BTU/hr)': [round(heat_loss, 2)],
                'Peak Reduction (KW)': [round(peak_reduce, 2)],
                'Annual Peak Reduction (KW/year)': [round(annual_peak_save, 2)],
                'Annual KWh Reduction (KWh/year)': [round(annual_kwh_save, 2)],
                'Annual Peak Savings ($/year)': [round(annual_peak_cost, 2)],
                'Annual KWh Savings ($/year)': [round(annual_kwh_cost, 2)],
                'Total Annual Savings ($/year)': [round(total_savings, 2)]
            })
            
        else:
            savings_table = "Is system 'Gas' or 'Electric'"
            
        capital_cost = self.insul_cost * tank_area
        labor_cost = self.workers * self.man_hours * self.labor_cost
        
        implement_cost = capital_cost + labor_cost
        
        spp = implement_cost / total_savings
        spp_months = spp * 12
        
        cost_table = pd.DataFrame({
            'Capital Cost ($)': [round(capital_cost, 2)],
            'Labor Cost ($)': [round(labor_cost, 2)],
            'Implementation Cost ($)': [round(labor_cost, 2)],
            'SPP (years)': [round(spp, 2)],
            'SPP (months)': [round(spp_months, 2)]
        })
        
        return savings_table, cost_table
    

    def process(dictionaries, costs):
        tank_insulation = TankInsulation(dictionaries['Tank'])
        tank_insulation.set_costs(*costs)
        savings_table, cost_table = tank_insulation.calculator()
        tank_full = pd.concat([savings_table, cost_table], axis=1)
        
        return tank_full
    