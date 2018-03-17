# whos-in-town
A tool to make a google map of your facebook friends.

Most of us have more facebook friends than we know closely - wouldn't it be great to see who's living nearby some city you happen to be visiting? Facebook's graph search allows this to some extent, but is relatively poor at telling you who is nearby some city, or who used to live in a place and may have suggestions.

Plus, it's nice to have all your friends visually laid out on a map like this. Plus, with multiple place-markers per friend, you can feel like you have even more friends than you you really do!

Also a great tool for FB alumni pages, etc. But I digress.

###To Use:

Making the map consists of 4 steps.
- Getting a list of facebook urls associated with the people you're trying to map
- Finding all the places associated with each of those people, by visiting their pages (here, using Selenium)
- Geocoding all those places into lat/lng coordinates
- Putting those on a google map

##### Prerequisites:

You'll need a facebook account, and google geocoding API key. The easiest way to provide these to the program is to save them in a json of the following format, and then specify that file using the --secrets [FILENAME] option for whichever script you're running.

Example:
```
{
	"google_geocoding_api_key":  "AIlaNyCR38ZbbRsoioDETxaqtvpgiYGHfvEtYUI",
	"fb_password": "Kitty1993",
	"fb_login": "friendlyfreddie@gmail.com"
}
```

You'll also need the various python libs I import here. Most of those should be fairly straightforward to download with pip install.However, getting selenium (and in particular chromedriver) is sometimes fairly complicated.

On OSX, the general approach follows, but expect to google some errors:
- Selenium: run `sudo easy_install -U selenium; sudo easy_install -U requests`.

- chromedriver: go to the chromedriver website, download chromedriver, and then run something like `cp ~/Downloads/chromedriver /usr/local/bin/chromedriver; sudo chmod 755 /usr/local/bin/chromedriver` to put it in your path and set up permissions.

Also, if you don't want a weird number next to every name, make sure you have no facebook notifications when you start the script.

##### Running the code:

The first three steps (and part of the 4th) can be run together by running `python main.py`. The first three steps can also be run individually, with the respective scripts `get_friend_list.py`, `locate_friends.py`, and `get_geocodes.py`.

Note that data is stored between these steps in a data/ file - these are stored as JSON or text for (relatively) easy human readibility.

Script options:
 `--test` will only fetch info for the first 10 listed facebook URLs. It's recommended that you start with this option (especially if running main.py) to see if there are any errors in any step, because if you have over 1000 URLs to process (as is often the case), the entire process will take several hours.

 `--prefix` allows you to specify a prefix for the files stored in data/, so you can keep track of different runs, and not overwrite existing files.

 `--secrets` specifies a json file which contains your secret credentials, as described above.


Note that get_friend_list.py is a little janky, and depending on window size and the number of friends you have, you may have to help it scroll.

After running main.py or it's constituent scripts in order, you should be able to open map.html in a browser of your choice to view the map of your friends! Note that if you used a prefix, you'll need to modify the single reference to friend_places.js in map.html to contain the prefix you specified. You'll also have to make sure that those to files are in the same directory/folder (which won't initially be the case if your friend_places file is in the data/ directory).