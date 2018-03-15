import re, mmap, requests, json
from lib import *

def get_google_geocode(location, key):
	print "Grabbing google geocode for " + location
	try:
		request_url = "https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}".format(location, key)
		result_json = json.loads(requests.get(request_url).text)
		return result_json["results"][0] if result_json["status"] == "OK" else None
	except (UnicodeEncodeError):
		return None

def add_geocodes_to_verbose_places(friend, key, tolerance = 10):
	geocoded_places = []
	try:
		for place in friend["verbose_places"]:
			print "place is "
			print place
			geocode = get_google_geocode(place["name"], key)
			lat_lng = geocode["geometry"]["location"] if geocode else {"lat": 0.00, "lng": 0.00}
			n = place
			n["lat_lng"] = lat_lng
			geocoded_places.append(n)
			print "N is "
			print n
			# TODO: if place is within TOLERANCE of any other place, just add this name and reason to that place
	except KeyboardInterrupt:
	    raise
	except Exception as e:
	    print "ERROR!! Not adding places." 
	    print e.message
	    geocoded_places = [{"name" : "Default place", "reasons": ["caused an error when running the code at"], "lat_lng": {"lat": 0.00, "lng": 0.00}}]
	print "Geocoded places:"
	print geocoded_places
	friend["geocoded_places"] = geocoded_places
	return friend


def add_geocodes_to_all_friends(json_file, new_output_file):
	google_key = get_geocoding_credentials()["google_geocoding_api_key"]
	with open(json_file) as in_file:
		friends = json.load(in_file)
	geocoded_friends =[add_geocodes_to_verbose_places(friend, google_key) for friend in friends]
	geocoded_friends_json = json.dumps(geocoded_friends)

	with open(new_output_file, 'w+') as file_out:
		file_out.write("var friend_data = " + geocoded_friends_json + ";")
	print "done"

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--prefix", help="List of URLs of friends to locate")
	parser.add_argument("--secrets", help="Path of file containing fb credentials and API keys")
	parser.add_argument("--test", help="Only run the code on the first 20 names",
	                    action="store_true")
	args = parser.parse_args()
	prefix = args.prefix and args.prefix + '_'
	data_directory = os.path.dirname(os.path.realpath(__file__)) + "/data/"
	friend_json = data_directory + prefix + "friend_places.json"
	geocoded_friends_js = data_directory + prefix + "friend_places.js"
	add_geocodes_to_all_friends(friend_json, geocoded_friends_js)
