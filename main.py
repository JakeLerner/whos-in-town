from get_friends import *
from get_geocodes import *
from get_friends_selenium import *

# HTML from an entire "friends" page -> a list of friend urls
#process_fb_friends_html_page("../fb_friend_list_page.html", "some_friend_urls.txt", 30)

# list of friend urls -> a json file of friend names and locations
#process_all_urls("../all_friend_urls.txt", "all_friend_locations.json")

# json file of friend names and locations -> that plus lat & lng
#add_geocodes_to_all_friends("some_friend_locations.json", "some_new_friend_locations.js")


#incremental_process(process_all_urls_selenium, "failed_friend_urls.txt", "failed_friend_location.json", 50)
# print "Finding out"
# print file_len( "failed_friend_location.json"

append_json_files("failed_friend_location.json", "all_friend_locations.json", "more_friend_locations.json")

add_geocodes_to_all_friends("more_friend_locations.json", "including_failed_friend_locations.js")