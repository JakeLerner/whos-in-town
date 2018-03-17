from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os, re, mmap, requests, json, argparse, getpass, pip, time, random, codecs, sys

# Utility functions:
def first_regex_or_false(regex, searched_string):
	namereg = re.findall(regex, searched_string)
	return namereg[0].encode('utf-8', 'replace') if namereg else ""

def quick_sleep():
	time.sleep(random.randint(0, 2) + random.uniform(0, 1))

def get_prefix():
	parser = argparse.ArgumentParser()
	parser.add_argument("--prefix", help="String to prepend to generated filenames")
	args, unknown = parser.parse_known_args()
	prefix = args.prefix or raw_input("Enter prefix (or just hit enter for no prefix:")
	return prefix and prefix + '_'

def get_geocoding_credentials():
	parser = argparse.ArgumentParser()
	parser.add_argument("--secrets", help="If you want to enter your credentials separately.")
	args, unknown = parser.parse_known_args()
	if args.secrets:
		with open(args.secrets) as secrets_file:
			return json.load(secrets_file)
	else:
		api_token = getpass.getpass("Please enter your google geocoding API key:")
	return {"google_geocoding_api_key": api_token}

def get_fb_credentials():
	parser = argparse.ArgumentParser()
	parser.add_argument("--secrets", help="If you want to enter your credentials separately.")
	args, unknown = parser.parse_known_args()
	if args.secrets:
		with open(args.secrets) as secrets_file:
			secrets_json = json.load(secrets_file)
			fb_login = secrets_json["fb_login"]
			fb_password = secrets_json["fb_password"]
	else:
		fb_login = raw_input("Please enter your facebook username:") # input for python 3.x
		fb_password = getpass.getpass("Please enter your facebook password:")
	return {"fb_login": fb_login, "fb_password": fb_password}

# Sets up an automated browser in which to load facebook pages.
def setup_selenium():
	# Setup driver
	driver = webdriver.Chrome()
	# Get credentials
	fb_credentials = get_fb_credentials()
	fb_login = fb_credentials["fb_login"]
	fb_password = fb_credentials["fb_password"]
	# Log in to facebook
	driver.get("http://www.facebook.com")
	name_elem = driver.find_element_by_id("email")
	name_elem.clear()
	name_elem.send_keys(fb_login)
	password = driver.find_element_by_id("pass")
	password.send_keys(fb_password)
	password.send_keys(Keys.RETURN)
	# Return driver to caller
	return driver

def get_page_with_selenium(driver, url):
	driver.get(url)
	return driver.page_source

def get_infinity_scroll_page_with_selenium(driver, url, target_file = None):
	SCROLL_PAUSE_TIME = 5
	driver.get(url)
	last_height = driver.execute_script("return document.body.scrollHeight")
	while True:
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(SCROLL_PAUSE_TIME)
		new_height = driver.execute_script("return document.body.scrollHeight")
		if new_height == last_height:
			break
		last_height = new_height
	return driver.page_source

def process_fb_friends_html_page(data, url_filename, limit = None):
	friend_urls = re.findall('https://www.facebook.com/[a-z.0-9]+?\?', data)
	friend_urls = list(set([f + "location=friends_tab\n" for f in friend_urls if len(f) < 100]))
	if limit:
		friend_urls = friend_urls[:limit]
	print("Total URLs Found:")
	print(len(friend_urls))
	with open(url_filename, 'w+') as new_list_file:
		for fu in friend_urls:
			new_list_file.write(fu)
