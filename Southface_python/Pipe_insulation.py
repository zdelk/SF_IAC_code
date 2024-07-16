import pandas as pd
import numpy as np


class PipeInsulation:
    def __init__(self, pipe_data, k_values, pipe_dict):
        self.pipe_data = pipe_data
        self.k_values = k_values
        self.set_const(pipe_dict)

    def set_const(self, dict):
        for key, value in dict.items():
            setattr(self, key, value)

    def insulation_calculator(self):
        pipe_data = self.pipe_data.copy()
        k_values = self.k_values.copy()

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
            annual_btu_loss = btu_per_hour_loss * self.uptime  # Getting annual BTU los
            # Converting to MMBtu(generally it is billed)
            MMBtu_savings = (
                annual_btu_loss * self.boiler_efficiency * 10 ** (-6)
            )  # Note the efficiency

            annual_cost_saving = MMBtu_savings * self.per_MMBTU_cost  # Annual Savings

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

            per_kw_savings = (
                annual_peak_reduction * self.per_peak_cost
            )  # Yearly Peak Savings($)
            peak_savings = (
                annual_kwh_reduction * self.per_kwh_cost
            )  # Yearly Kwh Savings($)
            annual_cost_saving = per_kw_savings + peak_savings  # Annual Savings($)

            my_table = pd.DataFrame(
                {  # Creating dataframe if Electric System
                    "Heat_Loss_Savings_Per_Hour": [round(var, 2)],
                    "Peak_Demand_Reduction": [round(peak_reduction, 2)],
                    "Annual_Peak_Demand_Reduction": [round(annual_peak_reduction, 2)],
                    "Annual_KWh_Reduction": [round(annual_kwh_reduction, 2)],
                    "Cost_Savings_Peak": [round(peak_savings, 2)],
                    "Cost_Savings_KWh": [round(per_kw_savings, 2)],
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

        return pipe_cost_data, pipe_table_data, pipe_heat_savings

    def set_costs(self, per_kwh_cost, per_kw_peak_cost, per_MMBTU_cost, uptime_factory):
        self.per_kwh_cost = per_kwh_cost
        self.per_peak_cost = per_kw_peak_cost
        self.per_MMBTU_cost = per_MMBTU_cost
        self.uptime = uptime_factory

    def asDataFrame(self, results):
        df = pd.DataFrame([results])
        return df