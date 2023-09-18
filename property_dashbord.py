import datetime
import pandas as pd
import matplotlib.pyplot as plt
#reads the csv file into a pandas dataframe
df = pd.read_csv('data.csv')
#creates a dictionary which can be used to link a region code to a region
region_dict = {
 "1": "London",
 "2": "Bristol",
 "3": "Cardiff",
 "4": "Leeds",
 "5": "Manchester",
 "6": "Birmingham",
 "7": "Edinburgh",
 "8": "Glasgow"
}
#Gives the user a menu of options to choose between and will return their choice
def mainmenu():
 print("\t\t****Welcome to the Dashboard****")
 print('1) Return all current data')
 print('2) Return data for a specific region')
 print('3) Return data for different property types within a specific region')
 print('4) Return data for different property sizes within a specific region')
 print('5) Compare overall increase in property value by region')
 print('To quit, enter any other value')
 #I removed the int() from the input in order to prevent the program from crashing when a non-numeric value is entered
 return input("")

#prints all the data from the csv file
def alldata():
 print(df)

#displays a line graph showing the average percentage increase for a specified region over a specified time period
def region_check(region, startdate, enddate): 
 #region,startdate,enddate
 #creates an extract of the dataframe which only has the data within the specified time period
  df1 = df.loc[:, startdate:enddate]
  df2 = df.loc[:, 'Region Code':'Rooms']
  result = pd.concat([df2, df1], axis=1, join='inner').where(df2["Region"] == region)
  result = pd.DataFrame(result)
  result.dropna(inplace = True)
  print(result)
 #plots a line graph using the mean percentage increase from each month within the specified time period
  ave = df1.mean()
  ave.plot()
 #titles the graph appropriatley and includes the values inputted by the user
  plt.title("Average percentage increase in " + region + " from " + startdate + " to " + enddate)
  plt.show()
  return result
#displays a line graph showing the average percentage increase for each property type in a specified region over a specified time period
def property_types(region, startdate, enddate):
 #creates an extract of the dataframe only including rows where the region matches the "region" value and only includes the columns that are between the start and end date
 df1 = df.loc[(df["Region"] == region)].loc[:, startdate:enddate]
 #this line will use the concat function to add back in the "Property Type" column to the dataframe extract
 df1 = pd.concat([df["Property Type"], df1], axis=1, join='inner')
 for property_type in df1["Property Type"].unique():
  extract = df1.loc[(df1["Property Type"] == property_type)]
 #this line removes the "Property Type" column again as to not include it when determining the mean of all the values
 extract = extract.iloc[:, 1:]
 #plots a line of the average percentage increase for this property type in this region over time
 extract.mean().plot()
 plt.legend([property_type for property_type in df1["Property Type"].unique()], title="Property Types:")
 #titles the graph appropriatley and includes the values inputted by the user
 plt.title("Different property types in " + region + " from " + 
startdate + " to " + enddate)
 #displays the graph
 plt.show()
#displays a line graph showing the average percentage increase for each property size in a specified region over a specified time period
def property_sizes(region, startdate, enddate):
 #creates an extract of the dataframe only including rows where the region matches the "region" value and only includes the columns that are between the start and end date
 df1 = df.loc[(df["Region"] == region)].loc[:, startdate:enddate]
 #this line will use the concat function to add back in the "Rooms" column to the dataframe extract
 df1 = pd.concat([df["Rooms"], df1], axis=1, join='inner')
 for room_count in df1["Rooms"].unique():
  extract = df1.loc[(df1["Rooms"] == room_count)]
 #this line removes the "Rooms" column again as to not include it when determining the mean of all the values
 extract = extract.iloc[:, 1:]
 #plots a line of the average percentage increase for this property type in this region over time
 extract.mean().plot()
 plt.legend([room_count for room_count in df1["Rooms"].unique()], title="Rooms:")
 #titles the graph appropriatley and includes the values inputted by the user
 plt.title("Different sized properties in " + region + " from " + startdate + " to " + enddate)
 #displays the graph
 plt.show()
#displays a bar graph showing the difference between the overall increase in property value from different regions over a specified time period
def compare_overall_increase(startdate, enddate):
 #this array will hold the overall increase of property value for each region
 totals = []
 #will iterate through each region present in the dataframe
 for region in df["Region"].unique():
 #creates an extract of the dataframe only including rows where the region matches the "region" value and only includes the columns that are between the start and end date
  df1 = df.loc[(df["Region"] == region)].loc[:, startdate:enddate]
 #gets the sum of all percentages in the extract, round it to 2 decimal places and adds it to the totals array
 total_increase = round(df1.sum("columns").sum(), 2)
 totals.append(total_increase)
 #plots a bar graph with the region names on the x axis and the corrosponding totals as the y axis
 #this will show in a visually meaningful way, the difference between the overall increase in property value from different regions
 plt.bar([region for region in df["Region"].unique()], totals)
 #titles the graph appropriatley and includes the values inputted by the user
 plt.title("Overall increase in property value from " + startdate + " to " + enddate)
 #displays the graph
 plt.show()
#gives the user a list of all the regions and asks them to pick one, the input is validated and then returned
#this code was moved to be in a function so that its functionality can be used throughout the program rather than needing to add unecessary lines of code
def get_region():
 while True:
 #presents the user with an options menu of all the regions present in the dataframe
  print("Regions:")
  for i, region in enumerate(df["Region"].unique()):
   print(str(i+1) + ")", region)
  #allows the user to enter the region as a code from 1 to 8
  region_code = input("Please enter the name of the region you would like to check: ")
 #validates that the input is a number between 1 and 8
  if region_code.isnumeric() and 0 < int(region_code) < 9:
 #converts the code into the region and makes sure it is within the dataframe
   region = region_dict[region_code]
  if region in df.Region.values:
   return region
  else:
   print("Region not found")
 
#will ask the user for a start and end date, validate them and return the values
#this code was moved to be in a function so that its functionality can be used throughout the program rather than needing to add unecessary lines of code
def get_dates():
 while True:
  startdate = input("PLEASE ENTER A START DATE AS MONTH-YEAR e.g. JAN-20: ")
  startdate = startdate.capitalize()
 #determines if the entered date is valid by checking to see if it is within the dataframe
  if startdate not in df.columns:
   print("Error start date not found")
   
  enddate = input("PLEASE ENTER AN END DATE AS MONTH-YEAR e.g. JAN-20: ")
  enddate = enddate.capitalize()
 #determines if the entered date is valid by checking to see if it is within the dataframe
  if enddate not in df.columns:
     print("Error end date not found")
  else:
    return [startdate, enddate]
 
#main loop
x = mainmenu()
#will keep looping the menu until the user enter a value that isn't within the menu of options
while x in ["1", "2", "3", "4", "5"]:
 if x == "1":
  alldata()
 #asks the user for a region, startdate and enddate, makes sure they are valid and calls the region_check function using them as the parameters
 elif x == "2":
  region = get_region()
  startdate, enddate = get_dates()
  region_check(region, startdate, enddate)
 #asks the user for a region, startdate and enddate, makes sure they are valid and calls the property_types function using them as the parameters
 elif x == "3":
  region = get_region()
  startdate, enddate = get_dates()
  property_types(region, startdate, enddate)
 
 #asks the user for a region, startdate and enddate, makes sure they are valid and calls the property_sizes function using them as the parameters
 elif x == "4":
  region = get_region()
  startdate, enddate = get_dates()
  property_sizes(region, startdate, enddate)
 
 #asks the user for startdate and end date, makes sure they are valid and calls the compare_overall_increase function using them as the parameters
 elif x == "5":
  startdate, enddate = get_dates()
  compare_overall_increase(startdate, enddate)
 #calls the menu again to ask the user for another choice
 else:
     break
 x = mainmenu()

