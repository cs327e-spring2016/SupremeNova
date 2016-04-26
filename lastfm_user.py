from urllib.request import urlopen
import json
import pymysql

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
			break

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
	eventList = cur.fetchone()

	if eventList == None:
		print ("No events found for this band/artist")
	# print(cur.fetchone())
	else:
		while eventList != None:

			details = cur.fetchone()
			# print(details)


			eventDate = details[1]

			if (eventDate == None):
				print ("nothing")
			else:
				try:
					if (details[1] == None):
						print ("No date listed")
					else:
						print (eventDate.strftime('%m/%d/%Y'))

					if (details[2] == None):
						print ("No time listed")
					else:
						print (str(details[2]))

					if (details[3]== None):
						print ("No venue listed")
					else:
						print ("venue: "+ details[3])

					if (details[4] == None and details[5] == None):
						print ("No location listed")
					else:
						print ("Location: " + details[4] + ", " + details[5])
					print ()
				except:
					print("some error")
					print()
				# continue
			eventList = cur.fetchone()


	
	# print ("show artist function")


def showEvent(cur, conn):
	pass
	

def main ():

	conn = pymysql.connect(host='127.0.0.1', user='root', passwd='2SANSALVA', db='mysql')
	cur = conn.cursor()
	cur.execute("USE supremenova")

	# anything(cur,conn)
	print("#######################################################################")
	print("Select from the following options or press ENTER to quit")
	print()
	print("1: Make your own query")
	print("2: Choose events from list of artist")
	print()

	start = str(input("Select option number or press ENTER to quit:"))

	while ((start != "") and (start != "1") and (start != "2")):
		print()
		print ("Wrong input: Try again.")
		start = str(input("Select option number or press ENTER to quit:"))

	if (start == ""):
		pass
	else: 
		if (start == "1"):
			anything(cur,conn)
		elif(start == "2"):
			showArtist(cur,conn)






main ()