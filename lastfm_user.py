from urllib.request import urlopen
import json
import pymysql

def main ():

	name = str(input('Input artist number for infomation (press ENTER to quit):'))

	while name is not '':
		name = str(input('Input artist number for infomation (press ENTER to quit):'))

main ()