from get_friends import *
from get_geocodes import *

# HTML from an entire "friends" page -> a list of friend urls
process_fb_friends_html_page("../fb_friend_list_page.html", "some_friend_urls.txt", 30)

# list of friend urls -> a json file of friend names and locations
process_all_urls("../some_friend_urls.txt", "some_friend_locations.json")

# json file of friend names and locations -> that plus lat & lng
add_geocodes_to_all_friends("some_friend_locations.json", "all_new_friend_locations.js")