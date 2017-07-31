import re, mmap, requests, json, os

def read_secrets():
	with open("secrets.json") as secrets_file:
		secrets_json = json.load(secrets_file)
		return secrets_json

def first_regex_or_false(regex, searched_string):
  namereg = re.findall(regex, searched_string)
  return namereg[0].encode('utf-8', 'replace') if namereg else ""

def all_failed_urls_from_json(json_file, url_output_file):
	with open(json_file) as in_file:
		friends = json.load(in_file)
		urls = [f["url"] for f in friends if not f["success"]]
	print("Total URLs Found:")
	print(len(urls))
	with open(url_output_file, 'w+') as new_list_file:
	  for fu in urls:
		new_list_file.write(fu)

def append_json_files(json_file_1, json_file_2, new_json_file):
	with open(json_file_1) as first_file:
		first = json.load(first_file)
		with open(json_file_2) as second_file:
			second = json.load(second_file)
			result = first + second
	with open(new_json_file, 'w+') as file_out:
		file_out.write(json.dumps(result))

def append_files(file_1, file_2, output_file):
	with open(file_1) as first_file:
		with open(json_file_2) as second_file:
			with open(output_file, 'w+') as file_out:
				file_out.write(first_file.read())
				file_out.write(second_file.read())

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

def flush_array_to_file(arr, filename):

	with open(filename, 'w+') as file_out:
		if "json" in filename:
			arr_json = json.dumps(arr)
			file_out.write(arr_json)
		else:
			for a in arr:
				file_out.write(a)

def file_len(filename):
	with open(filename) as test:
		if "json" in filename:
			return len(json.load(test))
		else:
			return len([x for x in test])

def incremental_process(function, input_file, output_file, increment):
	# In case something goes wrong, we want to break up our big url file
	# into little URL files, process them in turn, and concatenate all the resultant
	# json lists.

	#function should take as input an input filename and an output filename
	with open(input_file, 'r+') as file_in:
		increments = int(file_len(input_file) / increment) + 1
		print "File length was " + str(file_len(input_file)) + ", increment length is " + str(increment) + ", so there are " + str(increments) + " increments."
		#sublists = [file_in[i * increment : (i + 1) * increment] for i in range(increments)]
		flush_array_to_file([], output_file)
		input_arr = [l for l in file_in]
		for i in range(increments):
			tmp_in = "tmp_" + input_file
			tmp_out = "tmp_" + output_file
			sublist = input_arr[i * increment : (i + 1) * increment]
			flush_array_to_file(sublist, tmp_in)
			function(tmp_in, tmp_out)
			if "json" in output_file:
				append_json_files(output_file, tmp_out, output_file)
			else:
				append_files(output_file, tmp_out, output_file)
			os.remove(tmp_in)
			os.remove(tmp_out)
			print "FINISHED ITERATION " + str(i)
			print "OUTPUT FILE " + output_file + " NOW HAS " + str(file_len(output_file)) + " ENTRIES."




