from urllib.request import urlopen
import json
import pymysql


def anything (cur, conn):

	notKeep = True
	while notKeep: 
		try: 
			x = str(input("Enter an SQL query:"))
			cur.execute(x)
			print(cur.fetchone())
			notKeep = False

		except:
			print ("not a number")

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

	anything(cur,conn)

	# showArtist(cur,conn)


	# name = str(input('Input artist number for infomation (press ENTER to quit):'))

	# while name is not '':
	# 	name = str(input('Input artist number for infomation (press ENTER to quit):'))

main ()