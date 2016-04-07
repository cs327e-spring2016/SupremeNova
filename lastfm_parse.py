from urllib.request import urlopen
import json

# user inputs artist name
name = input("Input an artist name: ")

# replaces string spaces with %20 to fit API convention
name.replace('','%20')

# calls the last.fm API 
url = 'http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist=&api_key=809d15fdb258f92ffd60f361dcf84feb&format=json'
url = url[:66] + (name) + url[66:]
response = urlopen(url)

# convert bytes to string type and string type to dict
string = response.read().decode('utf-8')
json_obj = json.loads(string)

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
