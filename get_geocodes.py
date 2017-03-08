import re, mmap, requests, json

def read_secrets(secrets_filename):
	with open(secrets_filename) as secrets_file:
	    secrets_json = json.load(secrets_file)
	    return secrets_json

def get_google_geocode(key, location):
	print "Grabbing google geocode for " + location
	request_url = "https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}".format(location, key)
	result_json = json.loads(requests.get(request_url).text)
	return result_json["results"][0] if result_json["status"] == "OK" else None

def add_geocode_to_friend_json(friend):
	google_key = read_secrets("../secrets.json")["google_geocoding_api_key"]
	primary_location = friend["locality"]
	primary_geocode_json = get_google_geocode(google_key, primary_location)
	if primary_geocode_json:
		primary_geocode_lat_lng = primary_geocode_json["geometry"]["location"]
		primary_geocode_county = [c["long_name"] for c in primary_geocode_json["address_components"] if "administrative_area_level_2" in c["types"]]
		primary_geocode_state = [c["long_name"] for c in primary_geocode_json["address_components"] if "administrative_area_level_1" in c["types"]]
		print primary_geocode_state
		print primary_geocode_county
		print primary_geocode_lat_lng
		friend["locality_geocode"] = primary_geocode_lat_lng
	else:
		friend["locality_geocode"] = {"lat": 0.00, "lng": 0.00}
	return friend


def add_geocodes_to_all_friends(json_file, new_output_file):
	with open(json_file) as in_file:
		friends = json.load(in_file)
	geocoded_friends =[add_geocode_to_friend_json(friend) for friend in friends]
	geocoded_friends_json = json.dumps(geocoded_friends)
	with open(new_output_file, 'w+') as file_out:
		file_out.write("var friend_data = " + geocoded_friends_json + ";")
	print "done"
