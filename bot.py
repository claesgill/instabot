from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import csv

class InstaBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = webdriver.Firefox()

    def login(self):
        b = self.browser
        b.get("https://www.instagram.com/accounts/login/?source=auth_switcher")
        sleep(3)
        email = b.find_element_by_name("username")
        pw    = b.find_element_by_name("password")
        email.clear()
        pw.clear()
        email.send_keys(self.username)
        pw.send_keys(self.password)
        pw.send_keys(Keys.RETURN)
        sleep(3)

        print("Logged in with {}".format(self.username))

        # Hit enter/return key for removing pop-up
        actions = ActionChains(b) 
        actions.send_keys(Keys.TAB * 2)
        actions.perform()
        actions.send_keys(Keys.RETURN)
        actions.perform()
        sleep(1)

        print("Remove pop-up")

    def like(self, search):
        b = self.browser
        b.get("https://www.instagram.com/explore/tags/" + search + "/")
        print("Searching for '{}'".format(search))

        # Scrolling through site
        # b.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        photos = b.find_elements_by_partial_link_text("")

        p = []
        for photo in photos:
            p.append(photo.get_attribute("href"))

        fail_count = 0
        duplicates = 0
        log = read_from_csv()
        for i in range(len(p)):
            if "/p/" in p[i] and p[i] not in log:
                print("Accessing: {}/{} - FAILS: {} - DUPS: {}".format(i, len(p), fail_count, duplicates), end="\r")
                b.get(p[i])
                try:
                    b.find_element_by_class_name("dCJp8.afkep._0mzm-").click()
                    write_to_csv(p[i])
                    sleep(10)
                except Exception as ex:
                    print("Something went wrong...")
                    fail_count += 1
                    sleep(60)
            else:
                duplicates += 1

    def follow():
        # TODO ...
        pass

def write_to_csv(link):
    with open("log.csv", "a") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([link])

def read_from_csv():
    with open("log.csv", "r") as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        list_of_links = []
        for line in reader:
            list_of_links.append(line[0])
    return list_of_links

if __name__ == "__main__":
    tags = ["sunrise", "sunset", "ocean", "travelling"]

    username = "ola@nordmann.no"
    password = "1234567890"

    bot = InstaBot(username, password)
    bot.login()
    while(True):
        for tag in tags:
            bot.like(tag)
        print("Starting new search!")