from get_friend_list import *
from locate_friends import *
from get_geocodes import *

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--prefix", help="Complete HTML file of your 'friends' page or a list of group members.")
parser.add_argument("--secrets", help="Path of file containing fb credentials and API keys")
parser.add_argument("--test", help="Only run the code on the first 20 names", action="store_true")
args = parser.parse_args()

prefix = args.prefix and args.prefix + '_'
data_directory = os.path.dirname(os.path.realpath(__file__)) + "/data/"
try:
    os.stat(data_directory)
except:
    os.mkdir(data_directory)  

friend_url_list = data_directory + prefix + "friend_urls.txt"
friend_places_json = data_directory + prefix + "friend_places.json"
geocoded_friends_js= data_directory + prefix + "friend_places.js"

# Generate facebook urls from a specified friend list page.
get_friend_list(URL_FILE)

# Get "places" associated with friends from their respective "about" pages.
process_all_urls_selenium(friend_url_list, friend_places_json, limit = 10 if args.test else None)


# Geocode friend locations, and format as javascript.
add_geocodes_to_all_friends(friend_places_json, geocoded_friends_js)

