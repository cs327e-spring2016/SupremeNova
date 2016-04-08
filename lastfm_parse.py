from urllib.request import urlopen
import json

# user inputs artist name
name = str(input('Input an artist name (press ENTER to quit): '))



# Continues loop until the user types quit
while name is not '':
	# replaces string spaces with %20 to fit API convention
	name = name.replace(' ','%20')

	# there is some type of error with when someone types a string '. H'
	if ("." and "H") in name:
		name = name.replace('.','')

	# calls the last.fm API 
	url = 'http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist=&api_key=809d15fdb258f92ffd60f361dcf84feb&format=json'
	url = url[:66] + (name) + url[66:]
	response = urlopen(url)
	
	# convert bytes to string type and string type to dict
	string = response.read().decode('utf-8')
	json_obj = json.loads(string)

	# error checking
	#print((json_obj['similarartists']['artist']))

	# to check if no artist is empty 
	if ("error" not in string) and (len(json_obj['similarartists']['artist']) != 0):

		# creates artist list, last artist, and artist index
		artistList =[]
		artistLast = json_obj['similarartists']['artist'][-1]['name']
		artist_index = 0

		# iterates through the list and uses the last artist to prevent going out of index
		while json_obj['similarartists']['artist'][artist_index]['name'] is not artistLast:
			artistList.append((json_obj['similarartists']['artist'][artist_index]['name']))
			artist_index += 1

		# adds the last artist parsing through list
		artistList.append(artistLast)
		print(artistList)
		print()

	# when no artist is found 
	else:
		print()
		print("Similar Artists Not Found")
		print()

	# user inputs artist name
	name = input('Input an artist name (press ENTER to quit): ')

