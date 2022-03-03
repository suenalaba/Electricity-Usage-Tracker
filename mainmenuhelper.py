# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 02:06:57 2022

@author: Jiaxin
"""

import datetime
from data import monthUsage
from data import monthSaved
from data import homeAppliance
from data import kitchenAppliance
from data import otherAppliance
from data import periodUsage
from data import periodSaved

#Exception Classes
class InvalidMonthException(Exception):
    pass

class InvalidYearException(Exception):
    pass

#Generic menu functions
def printMenu():
    print("----------------------------------------------------")
    print("Hi I'm E-Buddy your friendly personal assistant, what I can help you with today?")
    print(" 1. Update electricity unit price")
    print(" 2. Update my goals to save the Earth!")
    print(" 3. Edit my electricity conservation diary")
    print(" 4. Edit my electricity usage diary")
    print(" 5. Check current month's electricity details")
    print(" 6. Check historical electricity details")
    print(" 7. Exit")
    userInput = int(input("Make a selection from the above list: "))
    return userInput

def printReminder():
    if (bool(monthUsage) == False and bool(monthSaved) == False):
            return
    activityHighestConsumption = max(monthUsage, key=monthUsage.get)
    activityHighestConservation = max(monthSaved, key=monthSaved.get)
    print("Try to lower your usage on " + activityHighestConsumption + 
          ", its consuming way too much electricity!")
    print("Good job! Continue doing " + activityHighestConservation + 
          ", you have saved alot of electricity doing this!")

def printExitMessage():
    print("Keep it up, continue doing your part to save our lovely planet Earth")
    print("Till next time, good bye!")
    print("E-buddy is soooooooo greatful youre saving planeettt earthhhhh!!!")

#Menu Option 1
def updateElectricityPrice(electricityPrice):
    #global electricityPrice
    if (checkElectricityPrice(electricityPrice) == 1):
        while True:
            try:
                electricityPrice = float(input("Enter electricity price($) in kWh: "))
                if electricityPrice <= 0:
                    raise Exception("Cannot be negative")
                print("Your electricity price has been updated to $" + str(electricityPrice) + " per kWh")
                return electricityPrice
            except ValueError:
                print("The price of electricity must be numeric, try again!")
            except Exception:
                print("Price of electricity must be greater than zero, try again!")
    else:
        return electricityPrice

def checkElectricityPrice(electricityPrice):
    print("Your current electricity price is: $" + str(electricityPrice) + " per kWh")
    while True:
        try:
            userChoice = int(input("Press 1 to edit or 0 to return to main menu: "))
            if userChoice != 0 and userChoice != 1:
                raise ValueError
            return userChoice
        except ValueError: 
            print("Only enter either 1 or 0, try again.")



#Menu Option 2
def updateUsageTarget(conservationTarget):
    year,month = getMonthYear()
    printCurrentGoal(year,month,conservationTarget)
    if (confirmUpdate() == 1): 
        conservationTarget = getNewGoal(year,month)
    return conservationTarget
        
def getMonthYear():
    dateToday = datetime.datetime.now();
    year = dateToday.strftime("%Y")
    month = dateToday.strftime("%B")
    return year,month;

def printCurrentGoal(year,month,conservationTarget):
    print("You are updating your goal for " + month + " " + year)
    print("Your current goal for the month is to conserve a minimum of " + str(conservationTarget) +
          "kWh")
    
def confirmUpdate():
    while True:
        try:
            userChoice = int(input("Press 1 to edit or 0 to return to main menu: "))
            if userChoice != 0 and userChoice != 1:
                raise ValueError
            return userChoice
        except ValueError:
            print("Only enter either 1 or 0, try again")

def getNewGoal(year,month):
    while True:
        try:
            conservationTarget = float(input("Enter your new conservation target for the month: "))
            if conservationTarget <= 0:
                raise Exception("Must be greater than zero")
            print("Your new target for " + month + " " + year + " is " + str(conservationTarget) + "kWh")
            return conservationTarget
        except ValueError:
            print("Please enter a numeric target")
        except Exception:
            print("You target must be more than zero.")

#Menu Option 3
def updateSavingDiary():
    year,month = getMonthYear()
    while True:
        print("You are updating your electricity conserved for " + month + " " + year)
        print("What appliance was conserved?")
        try:
            userChoice = printApplianceMenu()
            if userChoice < 1 or userChoice > 4:
                raise ValueError
            elif userChoice == 1:
                #home
                taskDesc = getTaskDesc()
                savedHomeAppliance(taskDesc)
            elif userChoice == 2:
                #kitchen
                taskDesc = getTaskDesc()
                savedKitchenAppliance(taskDesc)
            elif userChoice == 3:
                #others
                taskDesc = getTaskDesc()
                savedOtherAppliance(taskDesc)
            elif userChoice == 4:
                printReminder()
                return
        except ValueError:
            print("Please enter a number from 1 to 4 only, try again")

def getTaskDesc():
    while True:
        try:
            taskDesc = input("Describe the little task you did to save the Earth: ")
            if len(taskDesc) <=5:
                raise Exception("Too short description")
            return taskDesc
        except Exception:
            print("Your description is too short, please enter a minimum of 6 characters")

def savedHomeAppliance(taskDesc):
    listHomeAppliance()
    while True:
        try:
            print("Which appliance's usage did you conserve?")
            applianceChoice = int(input("Please select from the list of home appliances: "))
            if applianceChoice <= 0 or applianceChoice > len(homeAppliance):
                raise ValueError
            capacity, minutes = getConservedCapacityMinutes()
            applianceItem, totalApplianceUsage = getHomeApplianceItemAndUsage(applianceChoice,capacity,minutes)
            updateMonthSaved(taskDesc,totalApplianceUsage)
            return
        except ValueError:
            print("Please enter a number only from 1 to " + str(len(homeAppliance))
                  + ", please try again")

def updateMonthSaved(applianceItem, totalApplianceUsage):
    if applianceItem in monthSaved:
      monthSaved[applianceItem] += totalApplianceUsage
    else:
      monthSaved[applianceItem] = totalApplianceUsage
    print("Your electricity conserved has been updated, " + applianceItem + " saved: " 
          + str(totalApplianceUsage) + "kWh of electricity!")  
    
def getConservedCapacityMinutes():
    while True:
        try:
            capacity = float(input("Please enter the use capacity conserved(%): "))
            if capacity < 0 or capacity > 100:
                raise ValueError
            break
        except ValueError:
            print("Only enter a number from 0 to 100, try again")
    while True:
        try:
            minutes = float(input("Please enter the minutes of use conserved: "))
            if minutes <= 0:
                raise ValueError
            return capacity, minutes
        except ValueError:
            print("Minutes must be numeric and positive")


def savedKitchenAppliance(taskDesc):
    listKitchenAppliance()
    while True:
        try:
            print("Which appliance's usage did you conserve?")
            applianceChoice = int(input("Please select from the list of kitchen appliances: "))
            if applianceChoice <= 0 or applianceChoice > len(kitchenAppliance):
                raise ValueError
            capacity, minutes = getConservedCapacityMinutes()
            applianceItem, totalApplianceUsage = getKitchenApplianceItemAndUsage(applianceChoice,capacity,minutes)
            updateMonthSaved(taskDesc,totalApplianceUsage)
            return
        except ValueError:
            print("Please enter a number only from 1 to " + str(len(kitchenAppliance))
                  + ", please try again")

def savedOtherAppliance(taskDesc):
    listOtherAppliance()
    while True:
        try:
            print("Which appliance's usage did you conserve?")
            applianceChoice = int(input("Please select from the list of other appliances: "))
            if applianceChoice <= 0 or applianceChoice > len(otherAppliance):
                raise ValueError
            capacity, minutes = getConservedCapacityMinutes()
            applianceItem, totalApplianceUsage = getOtherApplianceItemAndUsage(applianceChoice,capacity,minutes)
            updateMonthSaved(taskDesc,totalApplianceUsage)
            return
        except ValueError:
            print("Please enter a number only from 1 to " + str(len(otherAppliance))
                  + ", please try again")



#Menu Option 4
def updateUsageDiary():
    year,month = getMonthYear()
    while True:
        print("You are updating your usage for " + month + " " + year)
        userChoice = printApplianceMenu()
        if userChoice == 1:
            #home
            updateHomeAppliance()
        elif userChoice == 2:
            #kitchen
            updateKitchenAppliance()
        elif userChoice == 3:
            #others
            updateOtherAppliance()
        elif userChoice == 4:
            printReminder()
            return

def updateHomeAppliance():
    listHomeAppliance()
    while True:
        try:
            applianceChoice = int(input("Please select from the list of home appliances: "))
            if applianceChoice <= 0 or applianceChoice > len(homeAppliance):
                raise ValueError
            capacity, minutes = getCapacityMinutes()
            applianceItem, totalApplianceUsage = getHomeApplianceItemAndUsage(applianceChoice,capacity,minutes)
            updateMonthUsage(applianceItem,totalApplianceUsage)
            return
        except ValueError:
            print("Please enter a number only from 1 to " + str(len(homeAppliance))
                  + ", please try again")

                               
def listHomeAppliance():
    print("Appliance Name                          Estimated Wattage(W)")
    i = 1
    for k, v in homeAppliance.items():
        print("{:>2}. {:30} ||   {} ".format(str(i),k,str(v)))
        i+=1 

def getHomeApplianceItemAndUsage(applianceChoice,capacity,minutes):
    applianceIndex = applianceChoice - 1
    applianceItem = list(homeAppliance.items())[applianceIndex][0]
    applianceUsage = list(homeAppliance.items())[applianceIndex][1]
    totalApplianceUsage = float(float(capacity/100) * float(applianceUsage/1000) * float(minutes/60))
    return applianceItem, totalApplianceUsage

def updateMonthUsage(applianceItem, totalApplianceUsage):
    if applianceItem in monthUsage:
      monthUsage[applianceItem] += totalApplianceUsage
    else:
      monthUsage[applianceItem] = totalApplianceUsage
    print("Your usage has been updated, " + applianceItem + ": " 
          + str(totalApplianceUsage) + "kWh")  
    #for k,v in monthUsage.items():
        #print(k,v)
    
def printApplianceMenu():
    while True:
        try:
            print("----------------------------------------------------")
            print("Please select your type of appliance: ")
            print("1. Home Appliance")
            print("2. Kitchen Appliance")
            print("3. Other Appliance")
            print("4. Go back to main menu")
            userChoice = int(input("Make a selection from the above list: "))
            if userChoice <= 0 or userChoice > 4:
                raise ValueError
            return userChoice
        except ValueError:
            print("Please enter only 1 to 4, try again.")

def getCapacityMinutes():
    while True:
        try:
            capacity = float(input("Please enter the use capacity(%): "))
            if capacity < 0 or capacity > 100:
                raise ValueError
            break
        except ValueError:
            print("Only enter a number from 0 to 100, try again")
    while True:
        try:
            minutes = float(input("Please enter the minutes of use: "))
            if minutes <= 0:
                raise ValueError
            return capacity, minutes
        except ValueError:
            print("Minutes must be numeric and positive")



def updateKitchenAppliance():
    listKitchenAppliance()
    while True:
        try:
            applianceChoice = int(input("Please select from the list of kitchen appliances: "))
            if applianceChoice <= 0 or applianceChoice > len(kitchenAppliance):
                raise ValueError
            capacity, minutes = getCapacityMinutes()
            applianceItem, totalApplianceUsage = getKitchenApplianceItemAndUsage(applianceChoice,capacity,minutes)
            updateMonthUsage(applianceItem,totalApplianceUsage)
            return
        except ValueError:
            print("Please enter a number only from 1 to " + str(len(kitchenAppliance))
                  + ", please try again")


def listKitchenAppliance():
    print("Appliance Name                          Estimated Wattage(W)")
    i = 1
    for k, v in kitchenAppliance.items():
        print("{:>2}. {:30} ||   {} ".format(str(i),k,str(v)))
        i+=1 

def getKitchenApplianceItemAndUsage(applianceChoice,capacity,minutes):
    applianceIndex = applianceChoice - 1
    applianceItem = list(kitchenAppliance.items())[applianceIndex][0]
    applianceUsage = list(kitchenAppliance.items())[applianceIndex][1]
    totalApplianceUsage = float(float(capacity/100) * float(applianceUsage/1000) * float(minutes/60))
    return applianceItem, totalApplianceUsage


def updateOtherAppliance():
    listOtherAppliance()
    while True:
        try:
            applianceChoice = int(input("Please select from the list of other appliances: "))
            if applianceChoice <= 0 or applianceChoice > len(otherAppliance):
                raise ValueError
            capacity, minutes = getCapacityMinutes()
            applianceItem, totalApplianceUsage = getOtherApplianceItemAndUsage(applianceChoice,capacity,minutes)
            updateMonthUsage(applianceItem,totalApplianceUsage)
            return
        except ValueError:
            print("Please enter a number only from 1 to " + str(len(otherAppliance))
                  + ", please try again")


def listOtherAppliance():
    print("Appliance Name                          Estimated Wattage(W)")
    i = 1
    for k, v in otherAppliance.items():
        print("{:>2}. {:30} ||   {} ".format(str(i),k,str(v)))
        i+=1 

def getOtherApplianceItemAndUsage(applianceChoice,capacity,minutes):
    applianceIndex = applianceChoice - 1
    applianceItem = list(otherAppliance.items())[applianceIndex][0]
    applianceUsage = list(otherAppliance.items())[applianceIndex][1]
    totalApplianceUsage = float(float(capacity/100) * float(applianceUsage/1000) * float(minutes/60))
    return applianceItem, totalApplianceUsage

#Menu Option 5
def checkCurrentMonthDetails(electricityPrice,conservationTarget):
    year,month = getMonthYear()
    while True:
        print("You are checking your electricity details for " + month + " " + year)
        try:
            userChoice = printElectricityDetailsMenu()
            if userChoice <= 0 or userChoice > 8:
                raise ValueError
            elif userChoice == 1:
                totalConsumption = getTotalConsumption()
                printTotalConsumption(totalConsumption)
            elif userChoice == 2:
                totalConserved = getTotalConserved()
                printTotalConserved(totalConserved)
            elif userChoice == 3:
                totalBill = round(getTotalConsumption() * electricityPrice,2)
                printTotalBillPrice(totalBill)
            elif userChoice == 4:
                totalConservedPrice = round(getTotalConserved() * electricityPrice,2)
                printTotalSaved(totalConservedPrice)
            elif userChoice == 5:
                printAllUsage()
            elif userChoice == 6:
                printAllConserved()
            elif userChoice == 7:
                printUserTargetStatus(conservationTarget)
            elif userChoice == 8:
                return
        except ValueError:
            print("Please enter a number from 1 to 8 only, try again")

def printUserTargetStatus(conservationTarget):
    print("Your goal for the month is to conserve: " + "{:.2f}".format(conservationTarget)
          + "kWh of electricity")
    totalConserved = getTotalConserved()
    print("You have currently conserved " + "{:.2f}".format(totalConserved) + "kWh of electricity")
    remainingToGoal = conservationTarget - totalConserved
    if remainingToGoal > 0:
        print("You are currently " + "{:.2f}".format(remainingToGoal) + "kWh from your target")
    else: 
        print("GOOD JOB!!! You have reach your monthly target, keep saving the Earth")

def printAllUsage():
    print("Appliance                           Wattage(kWh) Consumed")
    for k,v in monthUsage.items():
        print("{:30} ||   {} ".format(k,str(v)))
    printReminder()

def printAllConserved():
    print("Action                              Wattage(kWh) Saved")
    for k,v in monthSaved.items():
        print("{:30} ||   {} ".format(k,str(v)))
    printReminder()

def printTotalSaved(totalConserved):
    print("Your total electricity bill saved this month is: $" + "{:.2f}".format(totalConserved))
    printReminder()
    "{:.2f}".format(totalConserved)
def printTotalBillPrice(totalBill):
    print("Your total electricity bill this month is: $" + "{:.2f}".format(totalBill))
    printReminder()

def getTotalConsumption():
    totalConsumption = 0
    for i in monthUsage.values():
        totalConsumption += float(i)
    return totalConsumption

def printTotalConsumption(totalConsumption):
    print("Your total current month electricity consumption is " +
          "{:.2f}".format(totalConsumption) + "kWh")
    print("You can do more to save the Earth, every little effort counts!")

def getTotalConserved():
    totalConserved = 0
    for i in monthSaved.values():
        totalConserved += float(i)   
    return totalConserved

def printTotalConserved(totalConserved):
    print("Your total current month electricity conserved is " +
          "{:.2f}".format(totalConserved) + "kWh")
    print("Keep going! Thank you for saving the Earth")

def printElectricityDetailsMenu():
    print("----------------------------------------------------")
    print("1. Calculate my total current month household usage")
    print("2. Calculate my total electricity saved this month") 
    print("3. Calculate my current month electricity bill")
    print("4. Calculate the amount saved from my conservation efforts")
    print("5. Display all current month household usage")
    print("6. Display all current month electricity saved")   
    print("7. Check how far away am I from my current goal")
    print("8. Return to main menu")
    while True:
        try:
            userChoice = int(input("Make a selection from the above list: "))
            if userChoice <= 0 or userChoice > 8:
                raise ValueError
            return userChoice
        except ValueError:
            print("Please enter a number from 1 to 8 only, try again.")



#Menu Option 6
def getMonth(month):
    if month == 1:
        return "Jan-"
    elif month==2:
        return "Feb-"
    elif month==3:
        return "Mar-"
    elif month==4:
        return "Apr-"
    elif month==5:
        return "May-"
    elif month==6:
        return "Jun-"
    elif month==7:
        return "Jul-"
    elif month==8:
        return "Aug-"
    elif month==9:
        return "Sep-"
    elif month==10:
        return "Oct-"
    elif month==11:
        return "Nov-"
    elif month==12:
        return "Dec-"



def printPastMonthMenu(period):
    print("You are checking electricity details for the period: " + period);
    print("----------------------------------------------------")
    print("1. Calculate the household usage for " + period)
    print("2. Calculate the total electricity saved for " + period) 
    print("3. Calculate the electricity bill for " + period)
    print("4. Calculate the amount of electricity bill saved for " + period) 
    print("5. Display all household usage for " + period)
    print("6. Display all electricity saved for " + period)   
    print("7. Return to main menu")

def checkPastMonths(period):
    printPastMonthMenu(period)
    while True:
        try:
            userChoice = int(input("Make a selection from the above list: "))
            if userChoice <= 0 or userChoice > 7:
                raise ValueError
            return userChoice
        except ValueError:
            print("Please enter a number from 1 to 7 only, try again.")

def getPeriod():
    while True:
        try:
            print("What period would you like to find out more about?")
            print("Please enter only numbers 1-12 for month, and 1990-2022 for year.")
            month = int(input("Please enter your month of choice: ")) #1-12
            year = int(input("Please enter your year of choice: ")) #1990-2022
            if month<1 or month>12:
                raise InvalidMonthException("Invalid month")
            if year<1900 or year>2022:
                raise InvalidYearException("Invalid Year")
            yearformatted = str(year)[2:4]
            monthformatted = getMonth(month)
            period = monthformatted+yearformatted
            return period
        except ValueError:
            print("You must enter digits only for both month and year")
        except InvalidMonthException:
            print("Month must be from 1 to 12 only")
        except InvalidYearException:
            print("Year must be digits and between 1900 and 2022")

def checkPeriodDetails(csvdata,electricityPrice):
    if csvdata is None:
        print("Since no file was loaded, you cannot check previous month's data.")
        return
    global period
    period = getPeriod()
    while True:
        userChoice = checkPastMonths(period)
        getPeriodData(csvdata)
        if (bool(periodUsage) == False and bool(periodSaved) == False):
            print("No data for this period available")
            return
        if userChoice == 1:
            totalConsumption = getPeriodTotalConsumption()
            printPeriodTotalConsumption(totalConsumption)
        elif userChoice == 2:
            totalConserved = getPeriodTotalConserved()
            printPeriodTotalConserved(totalConserved)
        elif userChoice == 3:
            totalBill = round(getPeriodTotalConsumption() * electricityPrice,2)
            printPeriodTotalBillPrice(totalBill)
        elif userChoice == 4:
            totalConservedPrice = round(getPeriodTotalConserved() * electricityPrice,2)
            printPeriodTotalSaved(totalConservedPrice)
        elif userChoice == 5:
            printPeriodAllUsage()
        elif userChoice == 6:
            printPeriodAllConserved()
        elif userChoice == 7:
            return

def getPeriodData(csvdata): 
    periodUsage.clear()
    periodSaved.clear()
    for i in range(0,len(csvdata)):
        if (csvdata[i][0] == period):
            if csvdata[i][1] in periodUsage:
                periodUsage[csvdata[i][1]] += float(csvdata[i][2])
            else:
                if csvdata[i][1] != "":
                    periodUsage[csvdata[i][1]] = float(csvdata[i][2])
            if csvdata[i][3] in periodSaved:
                periodSaved[csvdata[i][3]] += float(csvdata[i][4])
            else:
                if csvdata[i][3] != "":
                    periodSaved[csvdata[i][3]] = float(csvdata[i][4])

def printPeriodAllUsage():
    print("Electricity Usage for: " + period)
    print("Appliance                           Wattage(kWh) Consumed")
    for k,v in periodUsage.items():
        print("{:30} ||   {} ".format(k,str(v)))
    printReminder()

def printPeriodAllConserved():
    print("Electricity Usage for: " + period)
    print("Action                              Wattage(kWh) Saved")
    for k,v in periodSaved.items():
        print("{:30} ||   {} ".format(k,str(v)))
    printReminder()

def printPeriodTotalSaved(totalConserved):
    print("Your total electricity bill saved for " + period + " is: $" + "{:.2f}".format(totalConserved))
    printReminder()
    
def printPeriodTotalBillPrice(totalBill):
    print("Your total electricity bill for " + period + " is: $" + "{:.2f}".format(totalBill))
    printReminder()

def getPeriodTotalConsumption():
    totalConsumption = 0
    for i in periodUsage.values():
        totalConsumption += float(i)
    return totalConsumption

def printPeriodTotalConsumption(totalConsumption):
    print("Your total electricity consumption for " + period + " is " +
          "{:.2f}".format(totalConsumption) + "kWh")
    print("You can do more to save the Earth, every little effort counts!")

def getPeriodTotalConserved():
    totalConserved = 0
    for i in periodSaved.values():
        totalConserved += float(i)   
    return totalConserved

def printPeriodTotalConserved(totalConserved):
    print("Your total electricity conserved for " + period + " is " +
          str(totalConserved) + "kWh")
    print("Keep going! Thank you for saving the Earth")