# industrial_energy_consumption
## Data gathering and analysis of national industrial data consumption (SULI 2024)  
This repository contains relevant data for industrial energy consumption. Included are 2023 spreadsheets which include PGE public meter data, EPRI simulated load shapes for industrial end uses, and browser codes for PGE, EPRI, and EIA data. Below is some information for requirements and specifics of the data.

### EIA Combined Energy Browser
***
The eiaCombinedEnergyV2.py file contains code which can be used to see fossil fuel consumption by industry per state annually. This data includes coal consumption, natural gas consumption, and total petroleum consumption, which includes fuel oils and kerosene. In this program, you can also see what percentage of the fuels are used for electricity generation. For more information about how this code works, see the report.

Viewing this data requires an API key from the EIA. You can register for one at https://eia.gov/openada/. In the code, you will find sections which read:

```# + [YOUR API KEY HERE]```

In those places, replace the bracketed statement with a string containing your api key, and uncomment the code. 

### EPRI Load Shapes
***
To view EPRI load shapes, there are two relevant files, the Excel spreadsheet and the Python viewing program.

The Python program imports the data from the Excel spreadsheet and loads it to a Pandas dataframe and plots the load curves in MatPlotLib. In this program, you can view single loadshapes by peak or off-peak season and by peak weekday, average weekday, or weekend. There is also an option for you to scale the loadshape based on the amount of energy actually consumed. You can input a number in trillion btu and it will automatically scale the loadshape to reflect the actual energy used. 

The Excel spreadsheet contains all load shapes for the WSCC regions in CA and NV. The other load shapes from EPRI have not been added and must be added manually. 

For more information about the load shape library, please visit https://loadshape.epri.com/

### PGE CSV Viewer
***
To view PGE public data, there is one csv reader program and several csv files from PGE.

The PGE csv viewer Python program allows you to combine 4 spreadsheets from different quarters in the same year and look at annual electricity usage. The program includes dropdowns to filter by zipcode and sector, and plots the data in MatPlotLib. The program also allows you to change the year, however for that you will need to download the relevant data files to your computer. The program does however work for 2023 data and does not require data download. 

The PGE public data files include 4 csvs containing electricity usage data from the 4 quarters of 2023, and one quarter of natural gas data from 2023. The gas dataset does not contain industrial or agricultural sector information, only residential and commercial. The electricity data does contain industrial and agricultural information, as well as residential and commercial.

For more datasets or more information, please visit https://pge-energydatarequest.com/public_datasets

## How to use these programs
***
To use these programs, you will need to use marimo. You can do this using:

```pip install marimo```

To run or edit the code, use the command:

```marimo edit [APP NAME HERE]```

For more information on editing a marimo notebook, please refer to the marimo documentation. 
