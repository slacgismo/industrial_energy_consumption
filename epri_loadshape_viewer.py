import marimo

__generated_with = "0.8.0"
app = marimo.App(width="medium")


@app.cell
def __():
    # Imports

    import numpy as np
    import pandas as pd
    import marimo as mo
    import calendar
    import datetime as dt
    import matplotlib.pyplot as plt
    return calendar, dt, mo, np, pd, plt


@app.cell
def __():
    # Useful lists

    years = ["2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020","2021","2022","2023","2024"]
    months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    states=["AL","AR","AZ","CA","CO","CT","DE","FL","GA","IA","ID","IL","IN","KS","KY","LA","MA","MD","ME","MI","MN","MO","MS","MT","NC","ND","NE","NH","NJ","NM","NV","NY","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VA","VT","WA","WI","WV","WY"]
    return months, states, years


@app.cell
def __(pd):
    # Loading EPRI Loadshapes into Python
    # NOTE: Currently this spreadsheet only includes loadshapes from WSCC for CA and NV. In future the spreadsheet will include the 
    # loadshapes for all regions. This will take time to implement

    epri_loadshapes = pd.read_excel("https://github.com/slacgismo/industrial_energy_consumption/raw/main/EPRI%20End%20Use%20Load%20Shapes.xlsx","WSCC CANV")
    print(epri_loadshapes)

    # # Converting to datetime for column headers
    # hour_range = []
    # timeDel = 0
    # for hour in epri_loadshapes.columns:
    #     if hour.startswith("HE"):
    #         timeDel = int(hour[2:]) - 1
    #         hour_range.append(pd.to_datetime("01/01/2024")+pd.to_timedelta(timeDel,unit="h"))
    # print(hour_range)

    # for h in range(len(hour_range)):
    #     epri_loadshapes = epri_loadshapes.rename(columns={epri_loadshapes.columns[4+h]: hour_range[h]})
    # print(epri_loadshapes)
    return epri_loadshapes,


@app.cell
def __(epri_loadshapes, mo, removeRepeats):
    # Dropdown to choose peak or off peak season

    seasons = removeRepeats(epri_loadshapes["Season"])
    season = mo.ui.dropdown(seasons,seasons[0])
    mo.md(f"Choose a Season: {season}")
    return season, seasons


@app.cell
def __(epri_loadshapes, mo, removeRepeats):
    # Dropdown to choose day type from weekend or weekday

    dayTypes = removeRepeats(epri_loadshapes["Day Type"])
    dayType = mo.ui.dropdown(dayTypes,dayTypes[0])
    mo.md(f"Choose a Day Type: {dayType}")
    return dayType, dayTypes


@app.cell
def __(epri_loadshapes, mo, removeRepeats):
    # Dropdown to choose industrial end use

    endUses = removeRepeats(epri_loadshapes["End Use"])
    endUse = mo.ui.dropdown(endUses,endUses[0])
    mo.md(f"Choose an End Use: {endUse}")
    return endUse, endUses


@app.cell
def __(mo):
    mo.md(r"""***""")
    return


@app.cell
def __(mo):
    # Text box to enter annual energy usage from a specific industry. Data should come from the EIA's MECS survey
    # Future work could include automating this process and allowing the user to select a specific industry to see the loadshape scaled 
    # appropriately

    annualEnergy = mo.ui.text()
    mo.md(f"Enter annual energy usage (in trillion btu) for an industry: {annualEnergy}")
    return annualEnergy,


@app.cell
def __(annualEnergy, dayType, endUse, epri_loadshapes, season):
    # Calculating the annual energy modifier and ratio based on the annual energy number provided by the EPRI Loadshape Library 8.0

    annualEnergyMod = 0
    for j in range(len(epri_loadshapes["Season"])):
        if season.value == epri_loadshapes.iloc[j,0] and dayType.value == epri_loadshapes.iloc[j,1] and endUse.value == epri_loadshapes.iloc[j,2]:
            annualEnergyMod = epri_loadshapes.iloc[j,3]

    # print(annualEnergyMod)

    if not annualEnergy.value == "":
        annualEnergyRatio = ((float(annualEnergy.value)*(0.000293071E12))/annualEnergyMod)
    else:
        annualEnergyRatio = 1

    # print(annualEnergyRatio)
    return annualEnergyMod, annualEnergyRatio, j


@app.cell
def __(
    annualEnergyRatio,
    dayType,
    endUse,
    epri_loadshapes,
    pd,
    plt,
    season,
):
    # Getting the loadshape based on the specific parameters selected in the dropdowns

    loadshape = []
    for i in range(len(epri_loadshapes["Season"])):
        if season.value == epri_loadshapes.iloc[i,0] and dayType.value == epri_loadshapes.iloc[i,1] and endUse.value == epri_loadshapes.iloc[i,2]:
            loadshape = epri_loadshapes.iloc[i,4:]
            break

    # Adjusting the loadshape based on the annual energy ratio calculated above
    loadshape = annualEnergyRatio*loadshape

    # print(loadshape)

    loadshape.plot()

    yaxis = pd.Series([0,0.2,0.4,0.6,0.8,1])
    plt.yticks(annualEnergyRatio*yaxis)

    plt.xlabel("Hour Ending")
    plt.ylabel("Normalized Energy Use (kWh)")
    return i, loadshape, yaxis


@app.cell
def __(np):
    # Useful function to remove repeated occurences of data within a list. Used for creating dropdowns above

    def removeRepeats(arr):
        newArr = []
        addVal = True
        for value in arr:
            for n in newArr:
                if value == n:
                    addVal = False
            if addVal:
                newArr = np.append(newArr,value)
            addVal = True
        return(newArr)
    return removeRepeats,


if __name__ == "__main__":
    app.run()
