import requests
from bs4 import BeautifulSoup
import time
import random

starttime = time.time()
def runtime():
    uptime = time.time() - starttime
    days, notdays = divmod(uptime, 86400)
    hours, nothours = divmod(notdays, 3600)
    minutes, seconds = divmod(nothours, 60)
    print("Total Uptime: {:0>2}:{:0>2}:{:0>2}:{:0>2}".format(int(days),int(hours),int(minutes),int(seconds)))
    return(uptime)

def safetime():
    Rtime = float(random.randint(30,45)) + float(random.random())
    testtime = 15
    return(Rtime)

def saferequest(url):
    time1 = safetime() 
    print("Waiting " + str(round(time1,1)) + "s")
    time.sleep(time1 / 2)
    print("getting url...")
    time.sleep(time1 / 2)
    get = requests.get(url)
    if 'safe_get_counter' not in str(globals()):
        global safe_get_counter
        safe_get_counter = 1
    else:
        safe_get_counter += 1
    print("Request " + str(safe_get_counter) + " complete")
    return(get)

az = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "19"]

#put any letters you want to check in this list
checkletters = ['s']

with open('s_artists.txt', 'w', encoding="utf-8") as output_file1:
    output_file1.write("Artist Name,URL\n")
output_file1.close()

for letter in checkletters:
    current_letter = str(letter)
    time.sleep(0.1)
    print('Writing data for ' + current_letter + '...')
    url = "https://www.azlyrics.com/" + current_letter + ".html"
    page = saferequest(url)
    bs = BeautifulSoup(page.content, "html.parser")
    what_are_these = bs.find_all(class_="col-sm-6 text-center artist-col")
    half_links = []
    letter_artists = []
    for col in what_are_these:
        a_tags3 = col.find_all("a")
        for item in a_tags3:
            half_links.append(item.get('href'))
            letter_artists.append(item.text)
    letter_urls = ["https://www.azlyrics.com/" + addition for addition in half_links]

ziplist = list(zip(letter_artists, letter_urls))
for item in ziplist:
    line = str(item[0] + ',' + str(item[1]) + '\n')
    #change the filename to reflect what letter you chose
    with open('s_artists.txt', 'a+', encoding="utf-8") as output_file3: 
        output_file3.write(line)
    output_file3.close()