# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 02:11:10 2022

@author: Joshua
"""
import csv as csv 
import datetime


#to get current period that matches date format "Jan-22"
def getCurrentPeriod():
    dateToday = datetime.datetime.now();
    year = dateToday.strftime("%y")
    month = dateToday.strftime("%b")
    period = month + "-" + year
    return period

currentperiodcount = 0 #to prevent duplicate rows when loading csv

#load in data for electricity price, and user savings goal
#note every month, user will be prompted to enter a new one
#within the same month, user has option to update both, but will not be prompted 
#on start to key in the data
def loadUserData():
    try:
        csv_file_object2 = csv.reader(open('usagesummarydata.csv', 'rt'))
        next(csv_file_object2)
        
        userdata=[]
        
        for row in csv_file_object2:
            userdata.append(row)
        
        global electricityPrice
        global conservationTarget

        if (userdata[len(userdata)-1][0] != getCurrentPeriod()) or (userdata is None):
            while True:
                try:    
                    electricityPrice = float(input("Enter electricity price for this month($): "))
                    conservationTarget = float(input("Enter your conservation target this month in kWh: "))
                    break
                except ValueError:
                    print("Please enter integers or floating point numbers only")
        else: 
            electricityPrice = float(userdata[len(userdata)-1][1])
            conservationTarget = float(userdata[len(userdata)-1][2])
            userdata = userdata[:-1]
        return userdata,electricityPrice,conservationTarget
    except FileNotFoundError:
        print('Data file does not exist, no data was loaded.')
    except PermissionError:
        print("File must be closed before running program, no data loaded.")

def saveUserData(userdata,electricityPrice,conservationTarget):
    try:
        updatedData = [[getCurrentPeriod() , electricityPrice, conservationTarget]]
        userTargetHeader = ["Period" , "Electricity Price", "Conservation Target"]
        with open('usagesummarydata.csv', 'w',  newline='') as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(userTargetHeader)

            # write multiple rows
            writer.writerows(userdata)
            writer.writerows(updatedData)
    except PermissionError:
        print("File must be closed before running program, no data saved.")


#temp dictionary at runtime to store periodic usage data
periodUsage = {}
#temp dictionary at runtime to store periodic conserved data
periodSaved = {}


#stores electricity usage of current month
monthUsage = {}
#stores electricity conserved for the current month
monthSaved = {}



#read in data
def loadData():
    try:
        csv_file_object = csv.reader(open('electricitydata.csv', 'rt'))
        
        next(csv_file_object)
        csvdata=[]
        
        for row in csv_file_object:
            csvdata.append(row)
        return csvdata
    except FileNotFoundError:
        print('Data file does not exist, no data was loaded.')
    except PermissionError:
        print("File must be closed before running program, no data loaded.")

#convert data to dictionary    
def getMonthData(csvdata):    
    if csvdata is None:
        return
    for i in range(0,len(csvdata)):
        if (csvdata[i][0] == getCurrentPeriod()):
            global currentperiodcount
            currentperiodcount += 1
            if csvdata[i][1] in monthUsage:
                monthUsage[csvdata[i][1]] += float(csvdata[i][2])
            else:
                if csvdata[i][1] != "":
                    monthUsage[csvdata[i][1]] = float(csvdata[i][2])
            if csvdata[i][3] in monthSaved:
                monthSaved[csvdata[i][3]] += float(csvdata[i][4])
            else:
                if csvdata[i][3] != "":
                    monthSaved[csvdata[i][3]] = float(csvdata[i][4])


#write data
#convert both monthly usage and saved data dictionary to 2d array        
def dicTo2dArray():
    if (len(monthUsage) <= len(monthSaved)):
        output = [[0 for x in range(5)] for x in range(len(monthSaved))]
        for i in range(0,len(monthUsage)):
            output[i][0] = getCurrentPeriod()
            output[i][1] = list(monthUsage)[i]
            output[i][2] = list(monthUsage.values())[i]
            output[i][3] = list(monthSaved)[i]
            output[i][4] = list(monthSaved.values())[i]
        for i in range(len(monthUsage),len(monthSaved)):
            output[i][0] = getCurrentPeriod()
            output[i][1] = ""
            output[i][2] = ""
            output[i][3] = list(monthSaved)[i]
            output[i][4] = list(monthSaved.values())[i]
    elif (len(monthUsage) > len(monthSaved)):
        output = [[0 for x in range(5)] for x in range(len(monthUsage))]
        for i in range(0,len(monthSaved)):
            output[i][0] = getCurrentPeriod() 
            output[i][1] = list(monthUsage)[i]
            output[i][2] = list(monthUsage.values())[i]
            output[i][3] = list(monthSaved)[i]
            output[i][4] = list(monthSaved.values())[i]
        for i in range(len(monthSaved),len(monthUsage)):
            output[i][0] = getCurrentPeriod() 
            output[i][1] = list(monthUsage)[i]
            output[i][2] = list(monthUsage.values())[i]
            output[i][3] = ""
            output[i][4] = ""
    return output                    

header = ["Period" , "Appliance" , "Wattage Consumed" ,"Action","Amount Saved"]

#concatenate old data with new data and export to csv
def writeDataToCsv(csvdata):
    csvdata = csvdata[:-currentperiodcount]
    try:
        output = dicTo2dArray()
        with open('electricitydata.csv', 'w', newline='') as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(header)

            # write multiple rows
            writer.writerows(csvdata)
            writer.writerows(output)
    except PermissionError:
        print("File must be closed before running program, no data saved.")


#list of predefined appliances grouped into home,kitchen & others
#Source = https://www.calculator.net/electricity-calculator.html
homeAppliance = {"Air-con(HVAC)": 5000,
            "Air-Con(Window)": 3000,
            "Heater(Home)": 10000,
            "Heater(Portable)": 1500,
            "Humidifier": 350,
            "Dehumidifier": 750,
            "Fan (ceiling or table)": 200,
            "Light bulb (LED)":	25,
            "Light bulb (incandescent)": 200,
            "Electric water heater": 6600
            }

kitchenAppliance = {"Refrigerator":	1000,
                    "Electric range/oven": 5000,
                    "Electric cooktop/stove": 5000,
                    "Microwave oven": 1500,
                    "Dishwasher": 2000,
                    "Coffee maker": 1200,
                    "Toaster": 1500,
                    "Electric kettle": 2000,
                    "Electric cooker": 1500
                    }

otherAppliance = {"Electric vehicle charger": 20000,
                    "Television": 500,
                    "Washing machine": 1500,
                    "Clothes dryer": 5000,
                    "Clothes iron":	2000,
                    "Hair dryer": 2000,
                    "Desktop computer":	250,
                    "Laptop computer": 150,
                    "Smart phone charger": 25,
                    "Water pump/motor": 2000
                    }
