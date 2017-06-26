import re, mmap, requests, json

from util import *

def process_fb_friends_html_page(friend_html_filename, url_filename, limit = None):
  with open(friend_html_filename, 'r+') as f:
    data = mmap.mmap(f.fileno(), 0)
    friend_urls = re.findall('https://www\.facebook\.com/.*?location=friends_tab', data)
    friend_urls = list(set([f + "\n" for f in friend_urls if len(f) < 100]))
    if limit:
      friend_urls = friend_urls[:limit]
    print("Total URLs Found:")
    print(len(friend_urls))
    with open(url_filename, 'w+') as new_list_file:
      for fu in friend_urls:
        new_list_file.write(fu)


def process_friend_url(url):
  try:
    print "fetching url " + url
    result_dictionary = process_friend_html(requests.get(url).text)
    result_dictionary["url"] = url
    print result_dictionary
    return result_dictionary
  except (UnicodeEncodeError):
    print "!! Unicode Error for " + url
    return {"url": url, "success": False, "error": "Unicode"}

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
