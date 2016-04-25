from urllib.request import urlopen
import json
import pymysql


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

	

def showArtist(cur, conn):

	cur.execute("SELECT bandName FROM bandList")
	x = cur.fetchone()
	count = 1
	while x != None:
		print (str(count)+ ":" + x[0])
		count += 1
		x = cur.fetchone()

	print()
	number = int(input("Select bandID: "))
	while ((number > count) and (type(number) != 'int')):
		print ("bandID of range")
		number = int(input("Select bandID:"))

	cur.execute("SELECT bandName FROM bandList WHERE bandID = %s", (str(number)))
	favBand = cur.fetchone()
	print()
	print("#######################################################################")
	print("Band selected is " + favBand[0])
	print()

	##########
	cur.execute("SELECT bandName, date, time, venue, city, state FROM event WHERE bandID = %s", (str(number)))
	eventList = cur.fetchone()

	if eventList == None:
		print ("No events for this band")
	# print(cur.fetchone())
	else:
		while eventList != None:

			details = cur.fetchone()

			eventDate = details[1]
			try:
				print (eventDate.strftime('%m/%d/%Y'))
				print (str(details[2]))
				print ("venue: "+ details[3])
				print ("Location: " + details[4] + ", " + details[5])
				print ()
			except:
				print("some error")
				print()
				continue
			eventList = cur.fetchone()


	
	# print ("show artist function")


def showEvent(cur, conn):
	pass
	

def main ():

	conn = pymysql.connect(host='127.0.0.1', user='root', passwd='2SANSALVA', db='mysql')
	cur = conn.cursor()
	cur.execute("USE supremenova")

	# anything(cur,conn)
	print("#########################################################")
	print("Select from the following options or press ENTER to quit")
	print()
	print("1: Make your own query")
	print("2: Choose events from list of artist")
	print()

	start = str(input("Select option numer or press ENTER to quit:"))

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