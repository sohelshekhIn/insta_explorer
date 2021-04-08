# Instagram Explorer
Get interaction on your post and suggested more by Instagram, just by interacting with 
other users with same interest and location!
Fully automated on selenium and chrome, just enter username and password and you are all done
If you think you are getting unnecessary followers, Instagram Unfollower is also uploaded on my Github
😛
Log of every followed account is saved in form of CSV file.
## Installation
>Required Libraries: Selenium & Pandas

>This project runs on Chrome Driver (recommended), or you may use any other Web Browser
If you don't have chromedriver follow this [blog](http://jonathansoma.com/lede/foundations-2018/classes/selenium/selenium-windows-install/)

Download the files in your prefer method (Downloading ZIP or through the url)
```
pip install -r requirements.txt
```

##### Before runing the main.py file, make sure you change the following things in the code

Chromedriver Path: Line 15
Instagram Username and Password: Line 26 & 27
Hastags you want to interect: Line 44
Number of people you want to follow per tag (default 10): Line 80
.
.
##### Now you can run the main.py file
.
```
py main.py
```
After runnning the above commands, a chrome window will appear and will start its work

## License

MIT
**Free Software, Hell Yeah!**
