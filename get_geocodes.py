import re, mmap, requests, json
from util import *

def get_google_geocode(location, key):
	print "Grabbing google geocode for " + location
	try:
		request_url = "https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}".format(location, key)
		result_json = json.loads(requests.get(request_url).text)
		return result_json["results"][0] if result_json["status"] == "OK" else None
	except (UnicodeEncodeError):
		return None

def add_geocode_to_friend_json(friend, key):
	primary_location = friend["locality"]
	primary_geocode_json = get_google_geocode(primary_location, key)
	if primary_geocode_json:
		primary_geocode_lat_lng = primary_geocode_json["geometry"]["location"]
		primary_geocode_county = [c["long_name"] for c in primary_geocode_json["address_components"] if "administrative_area_level_2" in c["types"]]
		primary_geocode_state = [c["long_name"] for c in primary_geocode_json["address_components"] if "administrative_area_level_1" in c["types"]]
		print primary_geocode_state
		print primary_geocode_county
		print primary_geocode_lat_lng
		friend["locality_geocode"] = primary_geocode_lat_lng
	else:
		print "Failed to geocode"
		friend["locality_geocode"] = {"lat": 0.00, "lng": 0.00}
	return friend

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
	google_key = read_secrets()["google_geocoding_api_key"]
	with open(json_file) as in_file:
		friends = json.load(in_file)
	geocoded_friends =[add_geocodes_to_verbose_places(friend, google_key) for friend in friends]
	#geocoded_friends =[add_geocode_to_friend_json(friend, google_key) for friend in friends if friend["success"]]
	geocoded_friends_json = json.dumps(geocoded_friends)

	with open(new_output_file, 'w+') as file_out:
		file_out.write("var friend_data = " + geocoded_friends_json + ";")
	print "done"
