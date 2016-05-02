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
			print (eventTime)
			print (eventVenue)
			print (eventCity + "," + eventState)
			print ()

		except:
			print ("Error printing")
			print ()

		eventInfo = cur.fetchone()
		count += 1


def showEvent(cur, conn):
	pass
	

def main ():

	conn = pymysql.connect(host='127.0.0.1', user='root', passwd='2SANSALVA', db='mysql')
	cur = conn.cursor()
	cur.execute("USE supremenova")



	print("#######################################################################")
	print("Select from the following options or press ENTER to quit")
	print()
	print("1: Make your own query")
	print("2: Choose events from list of artist")
	print("3: Something that ernie implements")
	print()

	start = str(input("Select option number or press ENTER to quit:"))

	while ((start != "") and (start != "1") and (start != "2") and (start != "3")):
		print()
		print ("Wrong input: Try again.")
		start = str(input("Select option number or press ENTER to quit:"))

	# if (start == ""):
	# 	sys.exit()
	# else: 
	# 	if (start == "1"):
	# 		anything(cur,conn)
	# 	elif(start == "2"):
	# 		showArtist(cur,conn)

	while (True):
		if (start == ""):
			sys.exit()
		elif (start == "1"):
			anything(cur,conn)
		elif(start == "2"):
			showArtist(cur,conn)
		elif(start == "3"):
			print ("not added yet")

		time.sleep(3)
		print("#######################################################################")
		print("Select from the following options or press ENTER to quit")
		print()
		print("1: Make your own query")
		print("2: Choose events from list of artist")
		print("3: Something that ernie implements")
		print()

		start = str(input("Select option number or press ENTER to quit:"))

		while ((start != "") and (start != "1") and (start != "2") and (start != "3")):
			print()
			print ("Wrong input: Try again.")
			start = str(input("Select option number or press ENTER to quit:"))







main ()