from urllib.request import urlopen
import json
<<<<<<< HEAD
import pymysql
=======
#import urllib.parse
>>>>>>> 1b9d89fe83e64c92cdfc68295febea566ef2c25b

# Populates user table
def user():
	pass 

# Populates original band list table
def bandList():
	pass

# Populates similar band list table
def similarBands():
	pass

# Populates event list table 
def Event():
	pass

def artistparse():
	# user inputs artist name
	name = str(input('Input an artist name (press ENTER to quit): '))

	conn = pymysql.connect(host='127.0.0.1', user='root', passwd='2SANSALVA', db='mysql')
	cur = conn.cursor()

	####################
	w = open('testing.txt', 'w', encoding='utf-8')

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
			# COMMENT REMOVE WHILE loop if you URL encode
			i = 0
			while i < len(artistList):
				artistList[i] = artistList[i].replace(' ','%20')
				artistList[i] = artistList[i].replace('/','%252F')
				# insert 
				i += 1

			# Calling bandsintown url (bit = BandsinTown)
			# COMMENT
			# URL encode this to remove errors 
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
						print(item['formatted_location'])
						print(item['datetime'])
						print(item['formatted_datetime'])
						print(item['venue']['name'])
						print()
						# print(str(item['formatted_location'].encode('utf-8')))
						# print(str(item['formatted_datetime'].encode('utf-8')))
						# print(item['venue']['name'].encode('utf-8'))
						
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

	cur.close()
	conn.close()



def main():

	artistparse()

main()

