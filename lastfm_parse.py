from urllib.request import urlopen
import json
import pymysql

# <<<<<<< HEAD
# =======
# #import urllib.parse
# >>>>>>> 1b9d89fe83e64c92cdfc68295febea566ef2c25b

# Populates user table
def user():
	pass 


# Populates original band list table
def bandList(bandName, genre, cur, conn):

	cur.execute("SELECT bandID FROM bandList WHERE bandName = %s", (bandName))

	x = cur.fetchone()

	# If band not in bandlist, add the band
	if (x == None):
		cur.execute("INSERT INTO bandList (bandName, genre) VALUES (%s,%s)", (bandName,genre))
		cur.connection.commit()
		print(bandName + ":added")

	# If band is already in bandlist, do NOT add the band (prevents duplicates)
	else:
		print (bandName + ":Not added, already exists")



# Populates similar band list table
def similarBands(oriBand, bandName, genre, cur, conn):

	# Get the original band ID to this similar band
	cur.execute("SELECT bandID FROM bandList WHERE bandName = %s", (oriBand))
	x = cur.fetchone()
	originalBand = x[0]

	# Get the original band name to this similar band 
	cur.execute("SELECT bandName FROM bandList WHERE bandName = %s", (oriBand))
	y = cur.fetchone()
	originalBandName = y[0]

	# add the similar band to the similar band table
	cur.execute("INSERT INTO similarBand (bandName, genre, similarBandID, similarBandName) VALUES (%s,%s,%s,%s)", (bandName, genre, originalBand, originalBandName))

	cur.connection.commit()

	# Add the similar band to bandlist, all bands will be listed in bandlist
	bandList(bandName, genre, cur, conn)



# Populates event list table 
def event(oriBand, state, city, date, time, venue, cur, conn):
	#primary key is eventID
	#foreign key is bandID

	cur.execute("SELECT bandID FROM bandList WHERE bandName = %s", (oriBand))
	x = cur.fetchone()
	originalBand = x[0]

	cur.execute("SELECT bandName FROM bandList WHERE bandName = %s", (oriBand))
	y = cur.fetchone()
	originalBandName = y[0]



	### Create a boolean to make sure events are only added one based on the date, time, venue, bandName
	cur.execute("INSERT INTO event (state, city, date, time, venue, bandID, bandName) VALUES (%s,%s,%s,%s,%s,%s,%s)", (state, city, date, time, venue, originalBand, originalBandName))


	cur.connection.commit()
	# print("event")
	# print(cur.fetchone())
	# print("done event")
	# print()
	

def artistparse(conn, cur):

	# cur.execute("DESCRIBE event")
	# print ("before")
	# print(cur.fetchone())
	# print("after")


	# user inputs artist name
	name = str(input('Input an artist name (press ENTER to quit): '))

	# conn = pymysql.connect(host='127.0.0.1', user='root', passwd='2SANSALVA', db='mysql')
	# cur = conn.cursor()

	####################
	# w = open('testing.txt', 'w', encoding='utf-8')

	# Continues loop until the user types quit
	while name is not '':
		
		# replaces string spaces with %20 to fit API convention
		name = name.replace(' ','%20')

		# there is some type of error with when someone types a string '. H'
		if ('.' and 'H') in name:
			name = name.replace('.','')
				
		# calls the last.fm API 
		lastfm_url = 'http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist=&api_key=809d15fdb258f92ffd60f361dcf84feb&format=json'
		lastfm_url = lastfm_url[:66] + (name) + lastfm_url[66:]
		response = urlopen(lastfm_url)
		
		# convert bytes to string type and string type to dict
		lfm_string = response.read().decode('utf-8')
		lfm_json_obj = json.loads(lfm_string)

		# error checking
		#print((json_obj['similarartists']['artist']))

		# to check if no artist is empty 
		if ('error' not in lfm_string) and (len(lfm_json_obj['similarartists']['artist']) != 0):

			# creates artist list, last artist, and artist index
			artistList =[]
			artistLast = lfm_json_obj['similarartists']['artist'][-1]['name']
			artist_index = 0

			# iterates through the list and uses the last artist to prevent going out of index
			while lfm_json_obj['similarartists']['artist'][artist_index]['name'] is not artistLast:
				artistList.append((lfm_json_obj['similarartists']['artist'][artist_index]['name']))
				artist_index += 1

			# adds the last artist parsing through list
			artistList.append(artistLast)
			print(artistList)
			print()

			# Scraping the Bandsintown API
			i = 0
			#chrs = set('àáâãäåæ',)
			while i < len(artistList):
				artistList[i] = artistList[i].replace(' ','%20')
				artistList[i] = artistList[i].replace('/','%252F')
				#artistList[i] = artistList[i].replace('','u')
				# insert 
				i += 1

			# Calling bandsintown url (bit = BandsinTown)
			for band in artistList:
				bit_url = 'http://api.bandsintown.com/artists//events.json?api_version=2.0&app_id=BandAdvocate'
				bit_url = bit_url[:35] + str(band) + bit_url[35:]
				response2 = urlopen(bit_url)

				# convert bytes to string type and string type to dict
				bit_string = response2.read().decode('utf-8')
				bit_json_obj = json.loads(bit_string)

				# Parses through all of the artists venues, formatted location, formatted datetime
				print(band)
				if len(bit_json_obj) != 0:
					for item in bit_json_obj :
						print()

						#print city
						formatedLocation = item['formatted_location']
						city = ''
						i = 0
						while (formatedLocation[i] != ',' ):
							city += formatedLocation[i]
							i += 1
						print (city)

						#print state
						state = formatedLocation[-2:]
						print (state)

						#print venue
						print(item['venue']['name'])

						#print date and time
						datetime = item['datetime']
						date = datetime[0:10]
						time = datetime[11:]
						print(date)
						print(time)
						print()

						# print(str(type(item['formatted_location'].encode('utf-8'))))
						# print(type(item['formatted_datetime'].encode('utf-8')))
						# print(item['venue']['name'].encode('utf-8'))
						# print()
						
				else:
					print('There are no events for this artist')
					print()
			


		# when no artist is found 
		else:
			print()
			print('Similar Artists Not Found')
			print()

		# user inputs artist name
		name = input('Input an artist name (press ENTER to quit): ')


def main():

	#establish a connection with Herbert's mysql (only work's with Herbert)
	#ERNIE: if you want to test using your own computer you will need to create a connection
		#Make sure to also create the same database name (supremenova)
		#Make sure to create the same tables with the same entities (sent picture on facebook)
	conn = pymysql.connect(host='127.0.0.1', user='root', passwd='2SANSALVA', db='mysql')
	# conn = pymysql.connect(host='127.0.0.1', user='root', passwd='erniestuff', db='mysql')

	#Create a cursor
	cur = conn.cursor()
	cur.execute("USE supremenova")

	# artistparse(conn, cur)

	# bandList('band2','rock', cur, conn)
	# similarBands('band2', 'bandawesome', 'folk', cur, conn)
	# bandList('bandawesome', 'folk', cur, conn)
	# event('bandawesome', 'TX', 'Austin', '2017-08-10', '15:30:00', 'Emos', cur, conn)
	# cur.execute("SELECT bandID FROM bandList WHERE bandName = 'passion pit' ")
	# print("here is fetchone")
	# x = cur.fetchone()
	# if (x == None):
	# 	print ("worked")


	#Close connection
	cur.close()
	conn.close()


main()

