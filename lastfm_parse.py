from urllib.request import urlopen
import json
import pymysql
from urllib.parse import quote
from urllib.parse import unquote
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
		print(bandName + ": added to bandList")

	# If band is already in bandlist, do NOT add the band (prevents duplicates)
	else:
		print (bandName + ": Not added to bandList, already exists")



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
	# bandList(bandName, genre, cur, conn)



# Populates event list table 
def event(oriBand, state, city, date, time, venue, cur, conn):
	#primary key is eventID
	#foreign key is bandID

	#Get the band ID
	cur.execute("SELECT bandID FROM bandList WHERE bandName = %s", (oriBand))
	x = cur.fetchone()
	originalBand = x[0]

	#Get the band name
	cur.execute("SELECT bandName FROM bandList WHERE bandName = %s", (oriBand))
	y = cur.fetchone()
	originalBandName = y[0]

	#check to see if event is already in event table
	cur.execute("SELECT * FROM event WHERE bandName = %s AND city = %s AND state = %s AND venue = %s AND date = %s", (oriBand, city, state, venue, date))
	keep = cur.fetchone()

	#If event is not already in table
	if (keep == None):

		cur.execute("INSERT INTO event (state, city, date, time, venue, bandID, bandName) VALUES (%s,%s,%s,%s,%s,%s,%s)", (state, city, date, time, venue, originalBand, originalBandName))
		print (oriBand + ": event added to event")

	#If event already in table
	else:
		print (oriBand + ": event was not added, already in event table.")


	cur.connection.commit()
	

#def artistparse(conn, cur):
def artistparse(cur, conn):


	# user inputs artist name
	name = str(input('Input an artist name (press ENTER to quit): '))


	# Continues loop until the user types quit
	while name is not '':
		
		# replaces string spaces with %20 to fit API convention
		name = quote(name)

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


		# calls the last.fm genre API 
		lastfm_genre = 'http://ws.audioscrobbler.com/2.0/?method=artist.gettoptags&artist=&api_key=809d15fdb258f92ffd60f361dcf84feb&format=json'
		lastfm_genre = lastfm_genre[:66] + (name) + lastfm_genre[66:]
		resp_genre = urlopen(lastfm_genre)

		# converts bytes to string type and string type to dict
		lfm_genre = resp_genre.read().decode('utf-8')
		lfm_genre_json = json.loads(lfm_genre)

		
		# for function bandList for the original band
		if len(lfm_genre_json) != 0:
			bandList(str(unquote(name)), str(lfm_genre_json['toptags']['tag'][0]['name']), cur, conn)
		else:
			bandList(str(unquote(name)), 'None', cur, conn)
		

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
			while i < len(artistList):
				artistList[i] = quote(str(artistList[i]))
				#artistList[i] = artistList[i].replace(' ','%20')
				#artistList[i] = artistList[i].replace('/','%252F')
				#artistList[i] = artistList[i].replace('','u')
				#print(artistList[i])

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
				print(str(unquote(band)))
				
				
				# calls the last.fm GENRE API 
				lastfm_genre = 'http://ws.audioscrobbler.com/2.0/?method=artist.gettoptags&artist=&api_key=809d15fdb258f92ffd60f361dcf84feb&format=json'
				lastfm_genre = lastfm_genre[:66] + str(band) + lastfm_genre[66:]
				resp_genre = urlopen(lastfm_genre)

				# converts bytes to string type and string type to dict
				lfm_genre = resp_genre.read().decode('utf-8')
				lfm_genre_json = json.loads(lfm_genre)


				# for function bandList for the original band
				if len(lfm_genre_json) != 0:
					#print(str(lfm_genre_json['toptags']['tag'][0]['name']))
					bandList(str(unquote(band)), str(lfm_genre_json['toptags']['tag'][0]['name']), cur, conn)
					similarBands(str(unquote(name)), str(unquote(band)), str(lfm_genre_json['toptags']['tag'][0]['name']), cur, conn)
				else:
					bandList(str(unquote(band)), 'None', cur, conn)
					similarBands(str(unquote(name)), str(unquote(band)), 'None', cur, conn)
					print("found nothing")
				
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
						# print (city)

						#print state
						state = formatedLocation[-2:]
						# print (state)

						#print venue
						# print(item['venue']['name'])
						venue = item['venue']['name']

						#print date and time
						datetime = item['datetime']
						date = datetime[0:10]
						time = datetime[11:]
						# print(date)
						# print(time)
						# print()
						event(str(unquote(band)), state, city, date, time, venue, cur, conn)
						# event(str(unquote(band)), str(state), str(city), str(date), str(time), str(item['venue']['name']), cur, conn)

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
	conn = pymysql.connect(host='127.0.0.1', user='root', passwd='2SANSALVA', db='mysql')
	
	# conn = pymysql.connect(host='127.0.0.1', user='root', passwd='erniestuff', db='mysql')

	#Create a cursor
	cur = conn.cursor()
	cur.execute("USE supremenova")
	

	#Populate the database based on user input
	artistparse(cur, conn)
	

	#Close connection
	cur.close()
	conn.close()


main()

