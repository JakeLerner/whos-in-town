import os, re, mmap, requests, json, argparse, getpass
from lib import *

def process_about_page(html):
	entry = {}
	entry["name"] = first_regex_or_false("pageTitle\">(.*?)<", html)
	verbose_places = find_places(html)
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
		if result["success"]:
			print "Success - " + result["name"] + ": " + str(result["places"])
		else:
			print "Failed for " + url
		if sleepy:
			quick_sleep()
		return result
	except KeyboardInterrupt:
		raise
	except Exception as e:
		print e
		return { "success": False, "error": e.message }

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

# Above functions can be called from main.py, but also allow this step to be run alone:
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--prefix", help="List of URLs of friends to locate")
	parser.add_argument("--secrets", help="Path of file containing fb credentials and API keys")
	parser.add_argument("--test", help="Only run the code on the first 20 names", action="store_true")
	args = parser.parse_args()

	prefix = args.prefix and args.prefix + '_'

	data_directory = os.path.dirname(os.path.realpath(__file__)) + "/data/"

	try:
			os.stat(data_directory)
	except:
			os.mkdir(data_directory)

	URL_FILE = data_directory + prefix + "friend_urls.txt"
	JSON_RESULT_FILE = data_directory + prefix + "friend_places.json"

	process_all_urls_selenium(URL_FILE, JSON_RESULT_FILE, limit = 10 if args.test else None)
