from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from get_friends import *
from util import *

import os, re, mmap, requests, json

def setup_selenium():
	# Set up Driver
	driver = webdriver.Chrome()

	# Login to Facebook
	fb_password = read_secrets()["fb_password"]
	fb_login = read_secrets()["fb_login"]

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
	verbose_places = find_places(html)
	print "Verbose Places:"
	print verbose_places
	entry["verbose_places"] = verbose_places
	entry["places"] = [item["name"] for item in verbose_places]
	entry["locality"] = entry["places"][0] if entry["places"] else ""
	entry["success"] = entry["name"] and entry["locality"]
	return entry

def find_places(req):
	word_list = ["[Ll]ive[sd] ", "[Ww]orks ", "[Ww]orked ", "[Ss]tudie[sd] ", "[Ww]ent to ", "[\w]* at", "[Ff]rom "] # could be "[\w*] at"
	places =  filter(bool, [re.findall("(" + word + ".*?)<.*?>(.*?)<", req) for word in word_list])
	result = {}
	for place in [p[0] for p in places]:
		print "place in find places is"
		print place
		name = place[1]
		if len(name) > 3:
			reason = place[0]
			if name in result.keys():
				result[name]["reasons"].append(reason)
			else:
				result[name] = {"name" : name, "reasons": [reason]}
	return result.values()


def process_friend_url_selenium(url, verbose = 0, sleepy = True):
	try:
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
		if sleepy:
			quick_sleep()
		return result
	except KeyboardInterrupt:
	    raise
	except Exception as e:
	    return {"success": False, "error": e.message}


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
