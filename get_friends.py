import re, mmap, requests, json

from util import *

def process_friend_url(url):
  try:
    stripped_url = url.rstrip()
    # url = url + "HLKJLKJ"
    #url = url.split("?")[0]
    print "fetching url " + stripped_url
    result_dictionary = process_friend_html(requests.get(stripped_url).text)
    result_dictionary["url"] = stripped_url
    print result_dictionary
    return result_dictionary
  except (UnicodeEncodeError):
    print "!! Unicode Error for " + stripped_url
    return {"url": stripped_url, "success": False, "error": "Unicode"}

def process_friend_html(req):
  entry = {}
  entry["name"] = first_regex_or_false("name\":\"(.*?)\"", req)
  entry["locality"] = first_regex_or_false("addressLocality\":\"(.*?)\"", req)
  section = first_regex_or_false("pagelet_eduwork(.*?)pagelet_all_favorites", req)
  if section:
    entry["places"] = [str(place) for place in re.findall("href=\"https://www.facebook.com/.*?>(.*?)<", section) if place]
    entry["locality"] = entry["locality"] or entry["places"][0]
  entry["success"] = entry["name"] and entry["locality"]
  return entry

def process_all_urls(urls_file, json_result_file):
  with open(urls_file, 'r+') as file_in:
    name_address_list = [process_friend_url(url) for url in file_in]
  print str(len(name_address_list)) + " friends processed, " + str(len([k for k in name_address_list if k["success"]])) + " successful."

  name_address_json = json.dumps(name_address_list)
  with open(json_result_file, 'w+') as file_out:
    file_out.write(name_address_json)
