from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
from random import randint
import pandas as pd
from os import path, remove
from pickle import dump, load

# Overriding print function for good view in console
def printD(msg):
    print(f"""  {msg}""")


# Change this to your own chromedriver path!
chromedriver_path = 'C:/webdrivers/chromedriver.exe'

printD(f"Chromedriver: {chromedriver_path}")
printD("Starting Chromedriver...")
webdriver = webdriver.Chrome(
    executable_path=chromedriver_path)
sleep(2)

webdriver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
sleep(3)

insta_username = "yourusername"
insta_password = 'yourpassword'
username = webdriver.find_element_by_name('username')
username.send_keys(insta_username)
password = webdriver.find_element_by_name('password')
password.send_keys(insta_password)
printD(f"Logining as {insta_username}")
button_login = webdriver.find_element_by_xpath(
    '//*[@id="loginForm"]/div/div[3]/button')
button_login.click()
sleep(5)
printD(f"Loged In as: {insta_username}")
webdriver.get('https://instagram.com')
sleep(2)
notnow = webdriver.find_element_by_css_selector(
    'body > div.RnEpo.Yx5HN > div > div > div > div.mt3GC > button.aOOlW.HoLwm')
notnow.click()  # comment these last 2 lines out, if you don't get a pop up asking about notifications

hashtag_list = ['spacex','nasa']

printD(f"Exloring tags: {hashtag_list}")
dataFileName = "userdata"
data = {'is_csvFile': False, 'currentFileName': ''}
csvFileName = ""

# Creating userdata file to save csv file status
if not path.isfile(dataFileName):
    printD("Data file not found")
    prev_user_list = []
    newFile = open(dataFileName, "wb")
    dump(data, newFile)
    newFile.close()
else:
    printD("Data file found")
    file = open(dataFileName, "rb")
    fileData = load(file)
    file.close
    if fileData['is_csvFile']:
        printD("CSV file found")
        csvFileName = fileData['currentFileName']
        # useful to build a user log
        printD(f"Getting previous followed user list from: {csvFileName}")
        prev_user_list = pd.read_csv(csvFileName, delimiter=',').iloc[:, 1:2]
        prev_user_list = list(prev_user_list['0'])
    else:
        printD("CSV File not found")
        prev_user_list = []

new_followed = []
tag = -1
followed = 0
likes = 0
comments = 0
printD("")
for hashtag in hashtag_list:
    tag += 1
    webdriver.get('https://www.instagram.com/explore/tags/' +
                  hashtag_list[tag] + '/')
    sleep(5)
    first_thumbnail = webdriver.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div')

    first_thumbnail.click()
    printD(f"Starting explore of #{hashtag_list[tag]}")
    sleep(randint(1, 2))
    try:
        for x in range(1, 10):
            username = webdriver.find_element_by_xpath(
                '/html/body/div[5]/div[2]/div/article/header/div[2]/div[1]/div[1]/span/a').text
            printD(f"User: {username}")
            if username not in prev_user_list:
                # If we already follow, do not unfollow
                if webdriver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').text == 'Follow':

                    webdriver.find_element_by_xpath(
                        '/html/body/div[5]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').click()

                    new_followed.append(username)
                    printD("    Followed the user")
                    followed += 1

                    # Liking the picture
                    button_like = webdriver.find_element_by_xpath(
                        '/html/body/div[5]/div[2]/div/article/div[3]/section[1]/span[1]/button/div/span')
                    printD("    Liked the post!")
                    button_like.click()
                    likes += 1
                    sleep(randint(18, 25))

                    # Comments and tracker
                    comm_prob = randint(1, 10)
                    printD('{}_{}: {}'.format(hashtag, x, comm_prob))
                    if comm_prob > 7:
                        comments += 1
                        webdriver.find_element_by_xpath(
                            '/html/body/div[5]/div[2]/div/article/div[3]/section[1]/span[2]').click()
                        comment_box = webdriver.find_element_by_xpath(
                            '/html/body/div[5]/div[2]/div/article/div[3]/section[3]/div/form/textarea')
                        if (comm_prob < 7):
                            comment_box.send_keys('Really cool!')
                            sleep(1)
                        elif (comm_prob > 6) and (comm_prob < 9):
                            comment_box.send_keys('Nice :)')
                            sleep(1)
                        elif comm_prob == 9:
                            comment_box.send_keys('Nice gallery!!')
                            sleep(1)
                        elif comm_prob == 10:
                            comment_box.send_keys('So cool! :)')
                            sleep(1)
                        # Enter to post comment
                        comment_box.send_keys(Keys.ENTER)
                        printD("    Commented on post")
                        print("""          
                            """)
                        sleep(randint(10, 20))

                # Next picture
                webdriver.find_element_by_link_text('Next').click()
                sleep(randint(10, 20))
            else:
                webdriver.find_element_by_link_text('Next').click()
                sleep(randint(10, 20))
    # some hashtag stops refreshing photos (it may happen sometimes), it continues to the next
    except:
        continue

if len(new_followed) == 0:
    printD("Did not created csv File as no accounts folllowed!")
else:
    for n in range(0, len(new_followed)):
        prev_user_list.append(new_followed[n])
    updated_user_df = pd.DataFrame(prev_user_list)
    gen_csvFileName = '{}_users_followed_list.csv'.format(
        strftime("%Y%m%d-%H%M%S"))
    updated_user_df.to_csv(gen_csvFileName)

    printD(f'New fllowers list created: {gen_csvFileName}')
    if csvFileName != "":
        remove(csvFileName)
        printD(f'Old followers list deleted: {csvFileName}')
    newFileData = data
    newFileData['is_csvFile'] = True
    newFileData['currentFileName'] = gen_csvFileName
    fileToBeUpdated = open(dataFileName, "wb")
    dump(newFileData, fileToBeUpdated)
    fileToBeUpdated.close()
    printD("Data file updated!")

printD('Liked {} photos.'.format(likes))
printD('Commented {} photos.'.format(comments))
printD('Followed {} new people.'.format(followed))

for i in range(5, -1, -1):
    printD(f'{i} seconds...')
    if i <= 0:
        webdriver.quit()
    sleep(1)
