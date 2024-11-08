# Python Package for Industrial Assessments
Overview:  
 - Requires relevant workbook and text file  
 - Recommendations are broken into groups
 - Some recommendations require a workbook sheet
 - Other only require relevant section in text file
 - Ran on Python 3.11
 - (SN) Denotes that a sheet is needed in the workbook for execution


### SF_IAC_Main
Main script that reads in the text file and workbook and outputs analysis workbook

### utilities_analysis
**Includes:**  
 - UtilityBill : (SN) Calculates average utilities rate based on previous bills

### Air_Line_leaks  
**Includes:**  
 - AirLeak : Air Leaks (from compressor lines)
 - ReduceAirPressure : Savings regarding reducing set air pressure on compressor  
 - TurnOffCompressor : Completley turning off a air compressor (if possible)  

### Boiler (more misc.)
**Includes:**  
 - AirFuelRatio : Cost savings from changing fuel ratio on gas boiler  
 - RepairSteamLeaks : (SN) Savings from fixing existing leaks in steam lines  
 - EfficientBelts : Replacing motor belts with efficient models
 - IsolateHotCold : Moving equipment so you are not heating a conditioned space or cooling a heated area  
 - ReplaceAirFilter : Savings from Replacing AC filters
 - ReplaceElectricMotors : (SN) Savings from upgrading electric motors to NEMA efficient models  
 - ReplaceHvacUnits : (SN) Savings from replacing HVAC units
 
### Microturbine_CHP  
**Includes:**  
 - Microturbine : Savings if a mircoturbine is installed to generate heat and power  
 
### Pipe_insulation
**Includes:**  
 - Insulation : General Class that aggregates relevant information
 - PipeInsulation : (SN) Savings from insulating bare pipe (usable on any heated pipe)
 - OvenDoorInsulation : (SN) Savings from (re)insulating oven doors  
 - TankInsulation : Savings from insulating water heaters or storage tanks  
 
### Replace_Lights 
**Includes:** 
 - LEDReplacement : Savings from replacing existing lighting with LEDs
 - OccupancySensor : Savings from installing occupancy sensor on some lights
 - DaylightSensor : Savings from installing daylight sensors on some lights

### VSD_replacement
**Includes:**  
 - VSDreplace : (SN) Savings from replacing current compressor with VSD model

