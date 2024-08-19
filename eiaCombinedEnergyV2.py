import marimo

__generated_with = "0.8.0"
app = marimo.App(width="medium")


@app.cell
def __():
    # Imports

    import numpy as np
    import pandas as pd
    import marimo as mo
    import json
    import requests
    import calendar
    import datetime as dt
    import matplotlib.pyplot as plt
    from pandas import json_normalize
    return calendar, dt, json, json_normalize, mo, np, pd, plt, requests


@app.cell
def __():
    # Dropdown Options

    years = ["2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020"]
    # months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    states=["AL","AR","AZ","CA","CO","CT","DE","FL","GA","IA","ID","IL","IN","KS","KY","LA","MA","MD","ME","MI","MN","MO","MS","MT","NC","ND","NE","NH","NJ","NM","NV","NY","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VA","VT","WA","WI","WV","WY"]
    return states, years


@app.cell
def __(mo, states):
    # Choose a state to pull energy data from

    state = mo.ui.dropdown(states,states[0])
    mo.md(f"Choose a State: {state}")
    return state,


@app.cell
def __(mo, years):
    # Choose a starting year. Note this year is not included in the energy output

    syear = mo.ui.dropdown(years,years[len(years)-2])
    mo.md(f"Choose a starting year: {syear}")
    return syear,


@app.cell
def __(mo, syear, years):
    # Choose an ending year after the starting year. This year is included in the energy output

    syearInd = 0

    for i in range(len(years)):
        if years[i] == syear.value:
            syearInd = i
            break

    eyear = mo.ui.dropdown(years[(syearInd+1):],years[len(years)-1])
    mo.md(f"Choose an end year: {eyear}")
    return eyear, i, syearInd


@app.cell
def __(eyear, state, syear):
    # Preparing an API link for annual coal consumption based on dropdown selections

    linkCoal = "https://api.eia.gov/v2/coal/consumption-and-quality/data/?frequency=annual&data[0]=consumption&facets[location][]="+state.value+"&facets[sector][]=10&start="+syear.value+"&end="+eyear.value+"&sort[0][column]=period&sort[0][direction]=asc&offset=0&length=5000"
    print(linkCoal)
    return linkCoal,


@app.cell
def __(linkCoal, requests):
    # Getting JSON file from EIA for Coal Consumption

    urlCoal = linkCoal # + [YOUR API KEY HERE]
    print(urlCoal)

    eiaCOj = requests.get(urlCoal)
    #print(eiaCOj.status_code)
    eiaCOjs = eiaCOj.json()
    print(eiaCOjs)
    return eiaCOj, eiaCOjs, urlCoal


@app.cell
def __(eiaCOjs, pd):
    # Creating Pandas Dataset for EIA Coal Consumption

    eiaCO = pd.json_normalize(eiaCOjs['response']['data'])
    eiaCO["value"]=eiaCO["consumption"].astype("float64")
    return eiaCO,


@app.cell
def __(eiaCO, np):
    # Converting Coal consumption units from tons to trillion btu and removing initial year to match other data sets

    eiaCoal = []
    j = 0
    for c in eiaCO["value"]:
        c = c*(1.882E-5)
        if not j  == 0:
            eiaCoal = np.append(eiaCoal,c)
        j += 1

    print(eiaCoal)
    return c, eiaCoal, j


@app.cell
def __(eyear, state, syear):
    # Preparing API link for Natural Gas consumption data for industrial sector

    linkNG = "https://api.eia.gov/v2/natural-gas/cons/sum/data/?frequency=annual&data[0]=value&facets[duoarea][]=S"+state.value+"&facets[process][]=VIN&start="+syear.value+"&end="+eyear.value+"&sort[0][column]=period&sort[0][direction]=asc&offset=0&length=5000"
    print(linkNG)
    return linkNG,


@app.cell
def __(linkNG, requests):
    # Getting JSON file from EIA for natural gas consumption

    urlNG = linkNG # + [YOUR API KEY HERE]

    eiaNGj = requests.get(urlNG)
    #print(eiaNGj.status_code)
    eiaNGjs = eiaNGj.json()
    print(eiaNGjs)
    return eiaNGj, eiaNGjs, urlNG


@app.cell
def __(eiaNGjs, pd):
    # Creating Pandas dataframe from EIA Natural Gas data

    eiaNG = pd.json_normalize(eiaNGjs['response']['data'])
    eiaNG["value"]=eiaNG["value"].astype("float64")
    return eiaNG,


@app.cell
def __(eiaNG, np):
    # Converting from mmcf to trillion btu

    eiaNGBTU = []
    for n in eiaNG["value"]:
        n = n/1000 
        eiaNGBTU = np.append(eiaNGBTU,n)

    print(eiaNGBTU)
    return eiaNGBTU, n


@app.cell
def __(eyear, requests, state, syear):
    # Preparing and getting API link for annual Petroleum consumption based on selected dropdowns. Not getting exclusively industrial data

    linkPET = "https://api.eia.gov/v2/petroleum/cons/821use/data/?frequency=annual&data[0]=value&facets[duoarea][]=S"+state.value+"&start="+syear.value+"&end="+eyear.value+"&sort[0][column]=period&sort[0][direction]=asc&offset=0&length=5000"

    urlPET = linkPET # + [YOUR API KEY HERE]

    eiaPETj = requests.get(urlPET)
    eiaPETjs = eiaPETj.json()
    print(eiaPETjs)
    return eiaPETj, eiaPETjs, linkPET, urlPET


@app.cell
def __(eiaPETjs, pd):
    # Creating Pandas dataframe from API link

    eiaPET = pd.json_normalize(eiaPETjs['response']['data'])
    eiaPET["value"]=eiaPET["value"].astype("float64")
    return eiaPET,


@app.cell
def __(eiaPET, np):
    # Filtering out exclusively industrial consumption data

    industrialIndices = np.where(eiaPET["process"]=="VIN")[0]
    # print(industrialIndices)
    eiaPETIndustrial = eiaPET.iloc[industrialIndices,[0,4,8,9,10]]
    eiaPETIndustrial["value"] = eiaPETIndustrial["value"].astype("float64")
    # print(eiaPETIndustrial)
    return eiaPETIndustrial, industrialIndices


@app.cell
def __(eiaNG, eiaPETIndustrial, np, removeRepeats):
    # Preparing Index for combined energy dataframe

    period = removeRepeats(eiaNG["period"])
    # print(period)

    # Preparing list of oil types for Petroleum data

    oilTypes = removeRepeats(eiaPETIndustrial["product-name"])
    # print(oilTypes)

    # Converting to trillion btu based on amount of btu produced per gallon for the given petroleum type

    totalPETUse = []
    totalPET = 0
    for year in period:
        for k in range(len(eiaPETIndustrial["value"])):
            if eiaPETIndustrial.iloc[k,0] == year:
                if eiaPETIndustrial.iloc[k,1] == oilTypes[0]:
                    totalPET += ((eiaPETIndustrial.iloc[k,3])/13500)
                elif eiaPETIndustrial.iloc[k,1] == oilTypes[1]:
                    totalPET += ((eiaPETIndustrial.iloc[k,3])/13850)
                elif eiaPETIndustrial.iloc[k,1] == oilTypes[2]:
                    totalPET += ((eiaPETIndustrial.iloc[k,3])/13850)
                elif eiaPETIndustrial.iloc[k,1] == oilTypes[3]:
                    totalPET += ((eiaPETIndustrial.iloc[k,3])/13870)
                elif eiaPETIndustrial.iloc[k,1] == oilTypes[4]:
                    totalPET += ((eiaPETIndustrial.iloc[k,3])/14000)
                elif eiaPETIndustrial.iloc[k,1] == oilTypes[5]:
                    totalPET += ((eiaPETIndustrial.iloc[k,3])/14970)
                elif eiaPETIndustrial.iloc[k,1] == oilTypes[6]:
                    totalPET += ((eiaPETIndustrial.iloc[k,3])/14500)
                elif eiaPETIndustrial.iloc[k,1] == oilTypes[7]:
                    totalPET += ((eiaPETIndustrial.iloc[k,3])/13850)
                elif eiaPETIndustrial.iloc[k,1] == oilTypes[8]:
                    totalPET += ((eiaPETIndustrial.iloc[k,3])/13850)
        totalPETUse = np.append(totalPETUse,totalPET)
        totalPET = 0

    # print(totalPETUse)
    return k, oilTypes, period, totalPET, totalPETUse, year


@app.cell
def __(eyear, state, syear):
    # Preparing API link for electricity generated by coal, natural gas, and petroleum annually

    linkEl = "https://api.eia.gov/v2/electricity/electric-power-operational-data/data/?frequency=annual&data[0]=consumption-for-eg-btu&facets[fueltypeid][]=COW&facets[fueltypeid][]=NG&facets[fueltypeid][]=PET&facets[location][]="+state.value+"&facets[sectorid][]=97&start="+syear.value+"&end="+eyear.value+"&sort[0][column]=period&sort[0][direction]=asc&offset=0&length=5000"
    print(linkEl)
    return linkEl,


@app.cell
def __(linkEl, requests):
    # Getting JSON file for electricity generation data

    urlEl = linkEl # + [YOUR API KEY HERE]

    eiaElj = requests.get(urlEl)
    #print(eiaElj.status_code)
    eiaEljs = eiaElj.json()
    print(eiaEljs)
    return eiaElj, eiaEljs, urlEl


@app.cell
def __(eiaEljs, np, pd):
    # Creating Pandas dataframe with electricity generation data

    eiaEl = pd.json_normalize(eiaEljs['response']['data'])
    #print(eiaEl["consumption-for-eg-btu"])
    eiaEl["consumption-for-eg-btu"]=eiaEl["consumption-for-eg-btu"].astype("float64")

    #print(eiaEl["consumption-for-eg-btu"])

    # Sorting generation by different fuel types into individual arrays

    ng = []
    coal = []
    pet = []
    row = 0

    for energy in eiaEl["consumption-for-eg-btu"]:
        if eiaEl.iloc[row,5] == "NG":
            ng = np.append(ng,energy)
        elif eiaEl.iloc[row,5] == "COW":
            coal = np.append(coal,energy)
        elif eiaEl.iloc[row,5] == "PET":
            pet = np.append(pet,energy)
        row += 1

    #print(len(ng))
    #print(len(coal))
    return coal, eiaEl, energy, ng, pet, row


@app.cell
def __(mo):
    mo.md(r"""***""")
    return


@app.cell
def __(eiaCoal, eiaNGBTU, pd, period, plt, state, totalPETUse):
    eiaTE = pd.DataFrame(
        {
            "Coal": eiaCoal,
            "Natural Gas": eiaNGBTU,
            "Petroleum": totalPETUse,
        },
        index = period
    )

    eiaTE.plot()

    plt.xlabel("Year")
    plt.ylabel("Energy Use in Trillion BTU")
    plt.title("Amount of fuels used per year in " + state.value)
    return eiaTE,


@app.cell
def __(mo):
    mo.md(r"""***""")
    return


@app.cell
def __(
    coal,
    eiaCoal,
    eiaNGBTU,
    ng,
    np,
    pd,
    period,
    pet,
    plt,
    state,
    totalPETUse,
):
    percentCoalforEG = []
    percentNGforEG = []
    percentPETforEG = []

    # Calculating percentages of each fuel type used for electricity generation

    for pos in range(len(eiaCoal)):
        if coal[pos] < eiaCoal[pos]:
            percentCoalforEG = np.append(percentCoalforEG,(coal[pos]/eiaCoal[pos]))
        else:
            percentCoalforEG = np.append(percentCoalforEG,1) 
                # If more fuel is consumed for electricity generation than in total, ratio is set to 1
        if ng[pos] < eiaNGBTU[pos]:
            percentNGforEG = np.append(percentNGforEG,(ng[pos]/eiaNGBTU[pos]))
        else:
            percentNGforEG = np.append(percentNGforEG,1)
                # If more fuel is consumed for electricity generation than in total, ratio is set to 1
        if pet[pos] < totalPETUse[pos]:
            percentPETforEG = np.append(percentPETforEG,(pet[pos]/totalPETUse[pos]))
        else:
            percentPETforEG = np.append(percentPETforEG,1)
                # If more fuel is consumed for electricity generation than in total, ratio is set to 1

    percentEG = pd.DataFrame(
        {
            "Coal": percentCoalforEG,
            "Natural Gas": percentNGforEG,
            "Petroleum": percentPETforEG
        },
        index = period
    )

    percentEG.plot()

    plt.yticks([0,0.2,0.4,0.6,0.8,1])
    plt.xlabel("Year")
    plt.ylabel("Percent of Fuel Used for Electricity Generation")
    plt.title("Ratios of different fuels used for Electricity Generation in " + state.value)
    return percentCoalforEG, percentEG, percentNGforEG, percentPETforEG, pos


@app.cell
def __(np):
    # Removes repeated elements from a list and returns a list with unique elements

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
