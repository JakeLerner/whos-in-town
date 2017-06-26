from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from get_friends import *
from util import *

import os, re, mmap, requests, json

def first_regex_or_false(regex, searched_string):
  namereg = re.findall(regex, searched_string)
  return namereg[0].encode('utf-8', 'replace') if namereg else ""

def setup_selenium():
	# Set up Driver
	chromedriver = "/Users/jrlerner/Downloads/chromedriver"
	os.environ["webdriver.chrome.driver"] = chromedriver
	driver = webdriver.Chrome(chromedriver)

	# Login to Facebook
	fb_password = read_secrets("../secrets.json")["fb_password"]
	fb_login = read_secrets("../secrets.json")["fb_login"]

	driver.get("http://www.facebook.com")
	name_elem = driver.find_element_by_id("email")
	name_elem.clear()
	name_elem.send_keys(fb_login)
	password = driver.find_element_by_id("pass")
	password.send_keys(fb_password)
	password.send_keys(Keys.RETURN)
	return driver

def get_page_with_selenium(driver, url):
	driver.get(url)
	return driver.page_source

def process_about_page(html):
	entry = {}
	entry["name"] = first_regex_or_false("pageTitle\">(.*?)<", html)
	entry["places"] = find_places(html)
	entry["locality"] = entry["places"][0] if entry["places"] else ""
	entry["success"] = entry["name"] and entry["locality"]
	return entry


def find_places(req):
	word_list = ["[Ll]ives ", "[Ww]orks ", "[Ss]tudies ", "[Ss]tudied ", "[Ww]orked ", "[Ww]ent to ", " at", "[Ff]rom "]
	return filter(bool, [first_regex_or_false(word + ".*?<.*?>(.*?)<", req) for word in word_list])


# def fill_in_the_blanks(json_file, new_output_file):
# 	with open(json_file) as in_file:
# 		friends = json.load(in_file)
# 	filled_in_friends =[add_geocode_to_friend_json(friend) for friend in friends if friend["success"]]
# 	geocoded_friends_json = json.dumps(geocoded_friends)
# 	with open(new_output_file, 'w+') as file_out:
# 		file_out.write("var friend_data = " + geocoded_friends_json + ";")
# 	print "done"
# def process_urls_selenium(url_file, output_file)


# with open(url_file, 'r+') as file_in:
# 	for item in file_in:
# 		about_url = item.split("?")[0] + "/about"
# 		req_html = get_page_with_selenium(driver, about_url)
# 		result = process_about_page(req_html)
# 		print result

def process_friend_url_selenium(url, verbose = 0):
	about_url = url.split("?")[0] + "/about"
	req_html = get_page_with_selenium(driver, about_url)
	result = process_about_page(req_html)
	result["url"] = url
	if verbose and result["success"]:
		print "Success for " + result["name"] + ": " + result["success"]

	if verbose and not result["success"]:
		print "Failed for " + url

	if verbose > 1:
		print result

	return result

def process_all_urls_selenium(urls_file, json_result_file, limit = None, offset = None):
	global driver
	if not 'driver' in globals():
		driver = setup_selenium()
	with open(urls_file, 'r+') as file_in:
		file_in = [url for url in file_in][offset:limit]
	 	name_address_list = [process_friend_url_selenium(url, 0) for url in file_in]
	print str(len(name_address_list)) + " friends processed, " + str(len([k for k in name_address_list if k["success"]])) + " successful."

	name_address_json = json.dumps(name_address_list)
	with open(json_result_file, 'w+') as file_out:
	 	file_out.write(name_address_json)

# all_failed_urls_from_json("all_friend_locations.json", "failed_friend_urls.txt")
# process_all_urls("failed_friend_urls.txt", "some_failed_friend_locations.json", 20)
# print "SECOND BATCH"
# process_all_urls("failed_friend_urls.txt", "some_more_failed_friend_locations.json", 40, 20)
# append_json_files("some_failed_friend_locations.json", "some_more_failed_friend_locations.json", "failed_friend_locations.json")
# with open("failed_friend_locations.json") as test:
# 	print len([i for i in json.load(test)])



#driver = setup_selenium()
#process_friend_url_selenium("https://www.facebook.com/ralucam?lst", 2)