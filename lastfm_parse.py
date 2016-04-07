from urllib.request import urlopen
import json


# Get the dataset
url = 'http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist=Passion%20Pit&api_key=809d15fdb258f92ffd60f361dcf84feb&format=json'
response = urlopen(url)

# Convert bytes to string type and string type to dict
string = response.read().decode('utf-8')
json_obj = json.loads(string)
artistList =[]
artistLast = json_obj['similarartists']['artist'][-1]['name']
artist_index = 0
while json_obj['similarartists']['artist'][artist_index]['name'] is not artistLast:
	artistList.append((json_obj['similarartists']['artist'][artist_index]['name']))
	artist_index += 1

artistList.append(artistLast)
print(artistList)
