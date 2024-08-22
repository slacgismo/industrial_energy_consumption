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
def __(mo):
    # Enter a year to browse all of the PGE public data from the year. Note: Must have downloaded any PGE data you want to look at

    year = mo.ui.text("2023")
    year
    return year,


@app.cell
def __(np, pd, removeRepeats, year):
    # To load electricity data, you need to have the relevant csv files downloaded to your computer or uploaded to github

    dataQ1 = pd.read_csv("https://github.com/slacgismo/industrial_energy_consumption/raw/main/PGE_"+year.value+"_Q1_ElectricUsageByZip.csv")
    dataQ2 = pd.read_csv("https://github.com/slacgismo/industrial_energy_consumption/raw/main/PGE_"+year.value+"_Q2_ElectricUsageByZip.csv")
    dataQ3 = pd.read_csv("https://github.com/slacgismo/industrial_energy_consumption/raw/main/PGE_"+year.value+"_Q3_ElectricUsageByZip.csv")
    dataQ4 = pd.read_csv("https://github.com/slacgismo/industrial_energy_consumption/raw/main/PGE_"+year.value+"_Q4_ElectricUsageByZip.csv")

    # year = data.iloc[0,2]
    # print(year)

    # Adding months to months list

    months = []
    for month in dataQ1["MONTH"]:
        if len(months) == 0:
            months = np.append(months,str(month))
        elif not month < int(months[len(months)-1]):
            months = np.append(months,month)
        else:
            break
    for month in dataQ2["MONTH"]:
        if not month < int(months[len(months)-1]):
            months = np.append(months,month)
        else:
            break
    for month in dataQ3["MONTH"]:
        if not month < int(months[len(months)-1]):
            months = np.append(months,month)
        else:
            break
    for month in dataQ4["MONTH"]:
        if not month < int(months[len(months)-1]):
            months = np.append(months,month)
        else:
            break
    # print(months)

    sectors = removeRepeats(dataQ1["CUSTOMERCLASS"])
    # print(sectors)
    return dataQ1, dataQ2, dataQ3, dataQ4, month, months, sectors


@app.cell
def __(mo, sectors):
    # Use this dropdown to choose a sector to look at a specific sector

    sector = mo.ui.dropdown(sectors,sectors[0])
    sector
    return sector,


@app.cell
def __(
    dataQ1,
    dataQ2,
    dataQ3,
    dataQ4,
    np,
    removeRepeats,
    sector,
    sortAscending,
    strAll,
):
    # Creating a list of zipcodes where there is data

    zipcodes = []
    for i in range(len(dataQ1["ZIPCODE"])):
        if dataQ1.iloc[i,3] == sector.value:
            if not dataQ1.iloc[i,6] == "0":
                zipcodes = np.append(zipcodes,dataQ1.iloc[i,0])

    for i in range(len(dataQ2["ZIPCODE"])):
        if dataQ2.iloc[i,3] == sector.value:
            if not dataQ2.iloc[i,6] == "0":
                zipcodes = np.append(zipcodes,dataQ2.iloc[i,0])

    for i in range(len(dataQ3["ZIPCODE"])):
        if dataQ3.iloc[i,3] == sector.value:
            if not dataQ3.iloc[i,6] == "0":
                zipcodes = np.append(zipcodes,dataQ3.iloc[i,0])

    for i in range(len(dataQ4["ZIPCODE"])):
        if dataQ4.iloc[i,3] == sector.value:
            if not dataQ4.iloc[i,6] == "0":
                zipcodes = np.append(zipcodes,dataQ4.iloc[i,0])

    # Sorting and removing repeat zipcodes

    zipcodes = sortAscending(zipcodes)
    zipcodes = removeRepeats(zipcodes)
    zipcodes = strAll(zipcodes)
    print(zipcodes)
    return i, zipcodes


@app.cell
def __(mo, zipcodes):
    # Dropdown to choose a zipcode to view the yearly electricity use for a sector in a specific zipcode

    zipcode = mo.ui.dropdown(zipcodes,zipcodes[0])
    zipcode
    return zipcode,


@app.cell
def __(
    dataQ1,
    dataQ2,
    dataQ3,
    dataQ4,
    months,
    np,
    pd,
    plt,
    sector,
    zipcode,
):
    averageEnergies = []

    # Finding specific indices for zipcodes and sectors that match the dropdowns

    selectedIndicesQ1 = []
    number = ""
    selectedZipsQ1 = np.where(dataQ1["ZIPCODE"] == int(zipcode.value))[0]
    selectedSectorsQ1 = np.where(dataQ1["CUSTOMERCLASS"] == sector.value)[0]
    # print(selectedZipsQ1)
    # print(selectedSectorsQ1)

    # Adding specific energies for indices that match both the zipcode and sector

    for z in selectedZipsQ1:
        for s in selectedSectorsQ1:
            if z == s:
                selectedIndicesQ1 = np.append(selectedIndicesQ1,z)
    # print(selectedIndices)
    if len(selectedIndicesQ1) == 3:
        for index in selectedIndicesQ1:
            energy = dataQ1.iloc[int(index),7]
            if dataQ1.iloc[int(index),6] == "0":
                averageEnergies = np.append(averageEnergies,0)
            else:
                for digit in dataQ1.iloc[int(index),7]:
                    if not digit == "," and not digit == " ":
                        number+=digit
                averageEnergies = np.append(averageEnergies,int(number))
                number = ""
    # If the spreadsheet has no values, add all 0s
    elif len(selectedIndicesQ1) == 0:
        averageEnergies = np.append(averageEnergies,0)
        averageEnergies = np.append(averageEnergies,0)
        averageEnergies = np.append(averageEnergies,0)
    # If the spreadsheet has one value, figure out where it is and add 0s everywhere else
    elif len(selectedIndicesQ1) == 1:
        if dataQ1.iloc[int(selectedIndicesQ1[0]),1] == 1:
            for digit in dataQ1.iloc[int(selectedIndicesQ1[0]),7]:
                if not digit == "," and not digit == " ":
                    number+=digit
            averageEnergies = np.append(averageEnergies,int(number))
            number = ""
            averageEnergies = np.append(averageEnergies,0)
            averageEnergies = np.append(averageEnergies,0) 
        elif dataQ1.iloc[int(selectedIndicesQ1[0]),1] == 2:
            averageEnergies = np.append(averageEnergies,0)
            for digit in dataQ1.iloc[int(selectedIndicesQ1[0]),7]:
                if not digit == "," and not digit == " ":
                    number+=digit
            averageEnergies = np.append(averageEnergies,int(number))
            number = ""
            averageEnergies = np.append(averageEnergies,0) 
        elif dataQ1.iloc[int(selectedIndicesQ1[0]),1] == 3:
            averageEnergies = np.append(averageEnergies,0)
            averageEnergies = np.append(averageEnergies,0)
            for digit in dataQ1.iloc[int(selectedIndicesQ1[0]),7]:
                if not digit == "," and not digit == " ":
                    number+=digit
            averageEnergies = np.append(averageEnergies,int(number))
            number = ""

    # print(averageEnergies)

    # The below code is the same as above but for the following months
    selectedIndicesQ2 = []
    number = ""
    selectedZipsQ2 = np.where(dataQ2["ZIPCODE"] == int(zipcode.value))[0]
    selectedSectorsQ2 = np.where(dataQ2["CUSTOMERCLASS"] == sector.value)[0]

    for z in selectedZipsQ2:
        for s in selectedSectorsQ2:
            if z == s:
                selectedIndicesQ2 = np.append(selectedIndicesQ2,z)
    # print(selectedIndices)
    if len(selectedIndicesQ2) == 3:
        for index in selectedIndicesQ2:
            energy = dataQ2.iloc[int(index),7]
            if dataQ2.iloc[int(index),6] == "0":
                averageEnergies = np.append(averageEnergies,0)
            else:
                for digit in dataQ2.iloc[int(index),7]:
                    if not digit == "," and not digit == " ":
                        number+=digit
                averageEnergies = np.append(averageEnergies,int(number))
                number = ""
    elif len(selectedIndicesQ2) == 0:
        # Appending 0s where no data exists
        averageEnergies = np.append(averageEnergies,0)
        averageEnergies = np.append(averageEnergies,0)
        averageEnergies = np.append(averageEnergies,0)
    elif len(selectedIndicesQ2) == 1:
        # Appending 0s based on where the single index is
        if dataQ2.iloc[int(selectedIndicesQ2[0]),1] == 4:
            for digit in dataQ2.iloc[int(selectedIndicesQ2[0]),7]:
                if not digit == "," and not digit == " ":
                    number+=digit
            averageEnergies = np.append(averageEnergies,int(number))
            number = ""
            averageEnergies = np.append(averageEnergies,0)
            averageEnergies = np.append(averageEnergies,0) 
        elif dataQ2.iloc[int(selectedIndicesQ2[0]),1] == 5:
            averageEnergies = np.append(averageEnergies,0)
            for digit in dataQ2.iloc[int(selectedIndicesQ2[0]),7]:
                if not digit == "," and not digit == " ":
                    number+=digit
            averageEnergies = np.append(averageEnergies,int(number))
            number = ""
            averageEnergies = np.append(averageEnergies,0) 
        elif dataQ2.iloc[int(selectedIndicesQ2[0]),1] == 6:
            averageEnergies = np.append(averageEnergies,0)
            averageEnergies = np.append(averageEnergies,0)
            for digit in dataQ2.iloc[int(selectedIndicesQ2[0]),7]:
                if not digit == "," and not digit == " ":
                    number+=digit
            averageEnergies = np.append(averageEnergies,int(number))
            number = ""

    # print(averageEnergies)

    selectedIndicesQ3 = []
    number = ""
    selectedZipsQ3 = np.where(dataQ3["ZIPCODE"] == int(zipcode.value))[0]
    selectedSectorsQ3 = np.where(dataQ3["CUSTOMERCLASS"] == sector.value)[0]
    # print(selectedZipsQ3)
    # print(selectedSectorsQ3)

    for z in selectedZipsQ3:
        for s in selectedSectorsQ3:
            if z == s:
                selectedIndicesQ3 = np.append(selectedIndicesQ3,z)
    # print(selectedIndices)
    if len(selectedIndicesQ3) == 3:
        for index in selectedIndicesQ3:
            energy = dataQ3.iloc[int(index),7]
            if dataQ3.iloc[int(index),6] == "0":
                averageEnergies = np.append(averageEnergies,0)
            else:
                for digit in dataQ3.iloc[int(index),7]:
                    if not digit == "," and not digit == " ":
                        number+=digit
                averageEnergies = np.append(averageEnergies,int(number))
                number = ""
    elif len(selectedIndicesQ3) == 0:
        averageEnergies = np.append(averageEnergies,0)
        averageEnergies = np.append(averageEnergies,0)
        averageEnergies = np.append(averageEnergies,0)
    elif len(selectedIndicesQ3) == 1:
        if dataQ3.iloc[int(selectedIndicesQ3[0]),1] == 7:
            for digit in dataQ3.iloc[int(selectedIndicesQ3[0]),7]:
                if not digit == "," and not digit == " ":
                    number+=digit
            averageEnergies = np.append(averageEnergies,int(number))
            number = ""
            averageEnergies = np.append(averageEnergies,0)
            averageEnergies = np.append(averageEnergies,0) 
        elif dataQ3.iloc[int(selectedIndicesQ3[0]),1] == 8:
            averageEnergies = np.append(averageEnergies,0)
            for digit in dataQ3.iloc[int(selectedIndicesQ3[0]),7]:
                if not digit == "," and not digit == " ":
                    number+=digit
            averageEnergies = np.append(averageEnergies,int(number))
            number = ""
            averageEnergies = np.append(averageEnergies,0) 
        elif dataQ3.iloc[int(selectedIndicesQ3[0]),1] == 9:
            averageEnergies = np.append(averageEnergies,0)
            averageEnergies = np.append(averageEnergies,0)
            for digit in dataQ3.iloc[int(selectedIndicesQ3[0]),7]:
                if not digit == "," and not digit == " ":
                    number+=digit
            averageEnergies = np.append(averageEnergies,int(number))
            number = ""
    # print(averageEnergies)

    selectedIndicesQ4 = []
    number = ""
    selectedZipsQ4 = np.where(dataQ4["ZIPCODE"] == int(zipcode.value))[0]
    selectedSectorsQ4 = np.where(dataQ4["CUSTOMERCLASS"] == sector.value)[0]

    for z in selectedZipsQ4:
        for s in selectedSectorsQ4:
            if z == s:
                selectedIndicesQ4 = np.append(selectedIndicesQ4,z)
    # print(selectedIndices)
    if len(selectedIndicesQ3) == 3:
        for index in selectedIndicesQ4:
            energy = dataQ4.iloc[int(index),7]
            if dataQ4.iloc[int(index),6] == "0":
                averageEnergies = np.append(averageEnergies,0)
            else:
                for digit in dataQ4.iloc[int(index),7]:
                    if not digit == "," and not digit == " ":
                        number+=digit
                averageEnergies = np.append(averageEnergies,int(number))
                number = ""
    elif len(selectedIndicesQ4) == 0:
        averageEnergies = np.append(averageEnergies,0)
        averageEnergies = np.append(averageEnergies,0)
        averageEnergies = np.append(averageEnergies,0)
    elif len(selectedIndicesQ4) == 1:
        if dataQ4.iloc[int(selectedIndicesQ4[0]),1] == 10:
            for digit in dataQ4.iloc[int(selectedIndicesQ4[0]),7]:
                if not digit == "," and not digit == " ":
                    number+=digit
            averageEnergies = np.append(averageEnergies,int(number))
            number = ""
            averageEnergies = np.append(averageEnergies,0)
            averageEnergies = np.append(averageEnergies,0) 
        elif dataQ4.iloc[int(selectedIndicesQ4[0]),1] == 11:
            averageEnergies = np.append(averageEnergies,0)
            for digit in dataQ4.iloc[int(selectedIndicesQ4[0]),7]:
                if not digit == "," and not digit == " ":
                    number+=digit
            averageEnergies = np.append(averageEnergies,int(number))
            number = ""
            averageEnergies = np.append(averageEnergies,0) 
        elif dataQ4.iloc[int(selectedIndicesQ4[0]),1] == 12:
            averageEnergies = np.append(averageEnergies,0)
            averageEnergies = np.append(averageEnergies,0)
            for digit in dataQ4.iloc[int(selectedIndicesQ4[0]),7]:
                if not digit == "," and not digit == " ":
                    number+=digit
            averageEnergies = np.append(averageEnergies,int(number))
            number = ""
    # print(averageEnergies)

    # Create a Pandas series and plot it with Matplotlib
    # print(averageEnergies)
    energyUse = pd.Series(averageEnergies,index=months)
    energyUse.plot()

    plt.xlabel("Month")
    plt.ylabel("Electricity Use (kWh)")
    return (
        averageEnergies,
        digit,
        energy,
        energyUse,
        index,
        number,
        s,
        selectedIndicesQ1,
        selectedIndicesQ2,
        selectedIndicesQ3,
        selectedIndicesQ4,
        selectedSectorsQ1,
        selectedSectorsQ2,
        selectedSectorsQ3,
        selectedSectorsQ4,
        selectedZipsQ1,
        selectedZipsQ2,
        selectedZipsQ3,
        selectedZipsQ4,
        z,
    )


@app.cell
def __():
    # Function to find the minimum value in an array

    def findMinimum(arr):
        min = arr[0]
        for n in arr:
            if n < min:
                min = n
        return min
    return findMinimum,


@app.cell
def __(findMinimum, np):
    # Function to sort an array by ascending number

    def sortAscending(arr):
        sortedArr = []
        for j in range(len(arr)):
            min = findMinimum(arr)
            sortedArr = np.append(sortedArr,min)
            arr = np.delete(arr,np.where(arr == min)[0][0])
        return sortedArr
    return sortAscending,


@app.cell
def __(np):
    # Function to remove repeated values from an array

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


@app.cell
def __(np):
    # Function to convert all values in an array to strings

    def strAll(arr):
        newArr = []
        for i in range(len(arr)):
            newArr = np.append(newArr,str(int(arr[i])))
        return(newArr)
    return strAll,


if __name__ == "__main__":
    app.run()
