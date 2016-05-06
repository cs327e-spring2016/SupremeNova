from urllib.request import urlopen
import json
import pymysql
import sys
import time

#Description: This code is what the user will use to query through the database

# Lets user use their own query 
def anything (cur, conn):

	notKeep = True
	while notKeep: 
		try:
			print()
			x = str(input("Press ENTER to quit OR input an SQL query:"))
			if (x == ''):
				break
			else:
				cur.execute(x)

				show = cur.fetchone()
				print (show)

				while (show != None):
					print(cur.fetchone())
					show = cur.fetchone()

				notKeep = False

		except:
			print ("Error: try again")


#Shows a list of artist in the database
def helpShow(cur, conn):
	print("#########################################")
	print("List of bands on database")
	cur.execute("SELECT bandName FROM bandList")
	x = cur.fetchone()
	count = 1
	while x != None:
		print (str(count)+ ":  " + x[0])
		count += 1
		x = cur.fetchone()

	print()


# User picks band from list to display events for the artist selected
def showArtist(cur, conn):

	print()
	name = str(input("Select band name or press ENTER to quit: "))

	cur.execute("SELECT bandName FROM bandList WHERE bandName = %s", (name))
	favBand = cur.fetchone()
	count = 0

	while ((favBand == None) and (type(name) != 'str')):

		if (name == ''):
			sys.exit()

		else:
			print ("band not in database. Try again.")
			print()

			if (name == "help"):
				helpShow(cur,conn)

			if (count > 3):
				print ("Need help?")
				print ("enter 'help' for a list of bands")
			name = str(input("Select band name or press ENTER to quit: "))
			cur.execute("SELECT bandName FROM bandList WHERE bandName = %s", (name))
			favBand = cur.fetchone()

			count += 1 



	print()
	print("#######################################################################")
	print("Band selected: " + favBand[0])
	print()

	#################
	cur.execute("SELECT bandName, date, time, venue, city, state FROM event WHERE bandName = %s", (favBand))
	eventInfo = cur.fetchone()
	counter = 0 

	if ((eventInfo == None) and counter == 0):
		print ("No events found for this artist")

	while (eventInfo != None):
		eventDate = eventInfo[1].strftime('%m/%d/%Y')
		eventTime = eventInfo[2]
		eventVenue = eventInfo[3]
		eventCity = eventInfo[4]
		eventState = eventInfo[5]

		try: 
			print (eventDate)
		except:
			print ("ERROR PRINTING DATE")

		try:
			print (eventTime)
		except:
			print ("ERROR PRINTING TIME")

		try:
			print (eventVenue)
		except:
			print ("ERROR PRINTING VENUE")

		try:
			print (eventCity + "," + eventState)
			print ()

		except:
			print ("ERROR PRINTING LOCATION")
			print ()

		eventInfo = cur.fetchone()
		counter += 1

	if (counter == 0):
		pass 
	else:
		print (str(counter) + " events found")


#User picks events based on city and state
def showEvent(cur, conn):

	print()

	check = False 

	while not check:
		city = str(input("Select CITY or press ENTER to quit: "))

		if (city == ""):
			sys.exit()

		state = str(input("Select STATE (ex. TX): "))

		if (len(state) == 2):
			check = True 
			break

		print("Incorrect input: Try again")
		print()

	print()
	print("#######################################################################")
	print("City selected: " + city +"," + state)
	print()

	#################
	cur.execute("SELECT bandName, date, time, venue, city, state FROM event WHERE city = %s AND state = %s", (city, state))
	eventInfo = cur.fetchone()
	counter = 0 

	if ((eventInfo == None) and counter == 0):
		print ("No events found.")

	while (eventInfo != None):
		eventName = eventInfo[0]
		eventDate = eventInfo[1].strftime('%m/%d/%Y')
		eventTime = eventInfo[2]
		eventVenue = eventInfo[3]
		eventCity = eventInfo[4]
		eventState = eventInfo[5]

		try:
			print(eventName)
		except:
			print("ERROR PRINTING NAME")

		try: 
			print (eventDate)
		except:
			print ("ERROR PRINTING DATE")

		try:
			print (eventTime)
		except:
			print ("ERROR PRINTING TIME")

		try:
			print (eventVenue)
		except:
			print ("ERROR PRINTING VENUE")

		try:
			print (eventCity + "," + eventState)
			print ()

		except:
			print ("ERROR PRINTING LOCATION")
			print ()

		eventInfo = cur.fetchone()
		counter += 1

	if (counter == 0):
		pass 
	else:
		print (str(counter) + " events found")


#User picks event by date 
def showDate (cur, conn):
	print()

	check = False 

	while not check:
		date = str(input("Select date (MM/DD/YYYY) or press ENTER to quit: "))

		if (date == ""):
			sys.exit()

		month = int(date[0:2])
		day = int(date[3:5])
		year = int(date[6:10])
		

		if ((len(date) == 10) and (date[2] == "/") and (date[5] == "/") and (month < 13) and (day < 32) and (year > 2015)):
			check = True 
			break

		print("Incorrect input: Try again")
		print()

	print()
	print("#######################################################################")
	print("Date selected: " + date)
	print()

	year = date[6:10]
	month = date[0:2]
	day = date[3:5]

	newDate = year+"-"+month+"-"+day

	################
	cur.execute("SELECT bandName, date, time, venue, city, state FROM event WHERE date = %s", (newDate))
	eventInfo = cur.fetchone()
	counter = 0 

	if ((eventInfo == None) and counter == 0):
		print ("No events found.")

	while (eventInfo != None):
		eventName = eventInfo[0]
		eventDate = eventInfo[1].strftime('%m/%d/%Y')
		eventTime = eventInfo[2]
		eventVenue = eventInfo[3]
		eventCity = eventInfo[4]
		eventState = eventInfo[5]

		try:
			print(eventName)
		except:
			print("ERROR PRINTING NAME")

		try: 
			print (eventDate)
		except:
			print ("ERROR PRINTING DATE")

		try:
			print (eventTime)
		except:
			print ("ERROR PRINTING TIME")

		try:
			print (eventVenue)
		except:
			print ("ERROR PRINTING VENUE")

		try:
			print (eventCity + "," + eventState)
			print ()

		except:
			print ("ERROR PRINTING LOCATION")
			print ()

		eventInfo = cur.fetchone()
		counter += 1

	if (counter == 0):
		pass 
	else:
		print (str(counter) + " events found")

	
#Interacts with the user to select what to do first 
def main ():

	conn = pymysql.connect(host='127.0.0.1', user='root', passwd='2SANSALVA', db='mysql')
	cur = conn.cursor()
	cur.execute("USE supremenova")



	print("#######################################################################")
	print("Select from the following options or press ENTER to quit")
	print()
	print("1: Choose events by city")
	print("2: Choose events by artist")
	print("3: Choose events by date")
	print()

	start = str(input("Select option number or press ENTER to quit:"))

	while ((start != "") and (start != "1") and (start != "2") and (start != "3")):
		print()
		print ("Wrong input: Try again.")
		start = str(input("Select option number or press ENTER to quit:"))

	while (True):
		if (start == ""):
			sys.exit()
		elif (start == "1"):
			showEvent(cur,conn)
		elif(start == "2"):
			showArtist(cur,conn)
		elif(start == "3"):
			showDate(cur,conn)

		time.sleep(3)
		print("#######################################################################")
		print("Select from the following options or press ENTER to quit")
		print()
		print("1: Choose events by city")
		print("2: Choose events by artist")
		print("3: Choose events by date")
		print()

		start = str(input("Select option number or press ENTER to quit:"))

		while ((start != "") and (start != "1") and (start != "2") and (start != "3")):
			print()
			print ("Wrong input: Try again.")
			start = str(input("Select option number or press ENTER to quit:"))


main ()