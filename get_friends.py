import re, mmap, requests, json

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

def is_good_result(friend_dictionary):
  # Using a full-fledged function not a lambda 'cuz I expect to expand this in the future
  return friend_dictionary and friend_dictionary["name"] != "ttstamp"

def process_friend_url(url):
  try:
    print "fetching url " + url
    result_dictionary = process_friend_html(requests.get(url).text)
    print result_dictionary
    print is_good_result(result_dictionary)
    return result_dictionary
  except (UnicodeEncodeError):
    print "!! Unicode Error for " + url
    return {}

def process_friend_html(req):
  entry = {}
  namereg = re.findall("name\":\"(.*?)\"", req)
  entry["name"] = str(namereg[0]) if namereg else "Unknown"
  addr = re.findall("addressLocality\":\"(.*?)\"", req)
  entry["locality"] = str(addr[0]) if addr else "Unknown"
  section = re.findall("pagelet_eduwork(.*?)pagelet_all_favorites", req)
  places = re.findall("href=\"https://www.facebook.com/.*?>(.*?)<", section[0]) if section else "None"
  entry["places"] = [str(place) for place in places if place]
  return entry

def process_all_urls(urls_file, json_result_file):
  with open(urls_file, 'r+') as file_in:
    name_address_list = [process_friend_url(url) for url in file_in]
  print str(len(name_address_list)) + " friends processed"

  name_address_list = filter(is_good_result, name_address_list)
  print str(len(name_address_list)) + " Valid Jsons Formed"

  name_address_json = json.dumps(name_address_list)
  with open(json_result_file, 'w+') as file_out:
    file_out.write(name_address_json)
