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
				# print(cur.description())
				# print(cur.fetchone())
				show = cur.fetchone()
				print (show)

				while (show != None):
					print(cur.fetchone())
					show = cur.fetchone()

				notKeep = False

		except:
			print ("Error: try again")

	# print (x

def showArtist(cur, conn):

	cur.execute("SELECT bandName FROM bandList")
	x = cur.fetchone()
	count = 1
	while x is not None:
		print (str(count)+ ":" + x[0])
		count += 1
		x = cur.fetchone()


	
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
	print("2: Choose band from list")
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
			pass






main ()