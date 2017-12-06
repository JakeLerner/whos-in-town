from get_friends import *
from get_geocodes import *
from get_friends_selenium import *
from shutil import copyfile
from os import remove
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--input_html", help="Complete HTML file of your 'friends' page or a list of group members.")
parser.add_argument("--prefix", help="Complete HTML file of your 'friends' page or a list of group members.")
parser.add_argument("--secrets", help="Path of file containing fb credentials and API keys")
parser.add_argument("--public", help="Don't log in as a facebook user; only scrape public profile info",
                    action="store_true")
parser.add_argument("--test", help="Only run the code on the first 20 names",
                    action="store_true")
args = parser.parse_args()

prefix = args.prefix or ""

FRIEND_URL_FILE = prefix + "friend_urls.txt"
FRIEND_JSON_FILE = prefix + "friend_locations.json"
FRIEND_JS_FILE = "friend_locations.js"

if args.secrets:
	copyfile(args.secrets, "secrets.json")

# HTML from an entire "friends" page -> a list of friend urls
if args.test:
	process_fb_friends_html_page(args.input_html, FRIEND_URL_FILE, 20)
	section_length = 5
else:
	process_fb_friends_html_page(args.input_html, FRIEND_URL_FILE)
	section_length = 50

# list of friend urls -> a json file of friend names and locations

if args.public:
	incremental_process(process_all_urls, FRIEND_URL_FILE, FRIEND_JSON_FILE, section_length)
else:
	incremental_process(process_all_urls_selenium, FRIEND_URL_FILE, FRIEND_JSON_FILE, section_length)

# json file of friend names and locations -> that plus lat & lng
add_geocodes_to_all_friends(FRIEND_JSON_FILE, FRIEND_JS_FILE)

print "Friend Finding is Complete! you should be able to find your friend map at 'map.html'!!"

remove("secrets.json")