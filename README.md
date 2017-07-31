# whos-in-town
A tool to make a google map of your facebook friends

To Use:


1. Go to your facebook friends page. Scroll down all the way so all friends are visible. Copy the html of that page, and save it as a `filename`. Call it whatever you want, but here we'll assue you've saved it as 'friends_page.html', so it's located at `~/Downloads/friends_page.html`

2. Save a google maps API token, (and, if desired, fb credentials) into a secret file. (let's say '~/Documents/secrets.json')

3. Run `python main.py --input_html ~/Downloads/friends_page.html --secrets ~/Documents/secrets.json --test`

3.1 you might be missing modules. On OSX, the easy solution is running `sudo easy_install -U selenium; sudo easy_install -U requests`. If that doesn't work, google the errors.

3.2 you probably will need to install chromedriver. to do this, go to the chromedriver website, download chromedriver, and then run something like `cp ~/Downloads/chromedriver /usr/local/bin/chromedriver; sudo chmod 755 /usr/local/bin/chromedriver` to put it in your path and set up permissions.

3.3 most things that could go wrong will throw errors, but you can check everything worked by looking at the map.html page in the current directory.

4. Once test mode works, run the same command but without the --test flag to process all your friends and generate a complete map.

4. Open [directory]/whos-in-town/map.html in a browser of your choice