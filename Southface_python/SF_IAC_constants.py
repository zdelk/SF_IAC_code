# Constants Script for IAC calculations
# Some need to be updated for each facility
# ----------------------------------------------#
# ---------------Update per Facility------------#
# ----------------------------------------------#

t_A = 70  # Ambient Temperature of the Facility

uptime_factory = 6240  # Uptime of the Facility
boiler_efficiency = 0.8  # Standard Efficiency of a boiler (Could be updated)

E_comp = 0.90 # Compressor Efficiency
C_dis = 0.61 # Loss coefficient at leak location (0.61 to 0.97)
P_line = 933 # line pressure in kPa
T_line = 90 # Temperature of line (F)
diameter_leak = 1.35 * 10**-3 # Daimeter of leak in m
num_leaks = 20 # Number of leaks
air_fix_time = 8 # Time to fix air leaks
air_staff_needed = 2 # Number of staff to fix air leaks


#per_therm_cost = 2.33  # Price per therm for Facility
# per_kwh_cost = 0.054 # Price per KWH for Facility
# per_kw_peak_cost = 13 # Price per Peak KW for Facility
#per_MMBTU_cost = 9.3  # Price per MMBtu for Facility

# ----------------------------------------------#
# -Standard Vals Don't Change unless necessary-#
# ----------------------------------------------#

r_Air = 0.3  # R-value of Air (standard)
k_insulation = 0.32  # K-value of Insulation (From Data Sheet)
d_thickness = 2  # Standard insulation thickness (From Data Sheet)
length_ris = 1.5  # Length of Removable Insulation System (From Data Sheet)

pipe_manhour_conversion = 0.12  # Time to install one foot of insulation (Standard)
pipe_manhour_cost = 91.63  # Per hour rate of labor (Standard)
pipe_mat_cost = 9.53  # Cost of one foot of insulation (Standard)
pipe_sf_cost = 133  # Cost of one special fitting/RIS

n = 1.4 # isentropic constant for ideal gas
K = 1.4 # Specific heat ratio
P_atm = 101 # Atmospheric Pressure in kPa
R = 287 # Air Ideal Gas Constant in j/kg*K

cost_ultrasonic = 5000 # Cost of Ultrasonic Leak Detector
labor_rate = 30 # Personnel Labor Rate