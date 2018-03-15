from lib import *

def get_friend_list(url_filename):
	driver = setup_selenium()
	webpage = raw_input("Enter URL of friends page:")
	html = get_infinity_scroll_page_with_selenium(driver, webpage)
	process_fb_friends_html_page(html, url_filename)

if __name__ == "__main__":
	prefix = get_prefix()
	if prefix:
		url_filename = "data/" + prefix + "_friend_urls.txt"
	else:
		url_filename = "data/friend_urls.txt"
	get_friend_list(url_filename)