import requests
from bs4 import BeautifulSoup
import time
import random
import smtplib, ssl
import sys
import traceback

starttime = time.time()
def runtime():
    uptime = time.time() - starttime
    days, notdays = divmod(uptime, 86400)
    hours, nothours = divmod(notdays, 3600)
    minutes, seconds = divmod(nothours, 60)
    print("Total Uptime: {:0>2}:{:0>2}:{:0>2}:{:0>2}".format(int(days),int(hours),int(minutes),int(seconds)))
    return(uptime)

def safetime():
    Rtime = float(random.randint(60,90)) + float(random.random())
    testtime = 15
    return(Rtime)

def livetimer(waittime):
    DecTime = float(waittime) - int(waittime)
    time.sleep(DecTime)
    for remaining in range(int(waittime), 0, -1):
        sys.stdout.write("\r")
        days, notdays = divmod(remaining, 86400)
        hours, nothours = divmod(notdays, 3600)
        minutes, seconds = divmod(nothours, 60)
        sys.stdout.write("Timer: {:0>2}:{:0>2}:{:0>2}:{:0>2} ".format(int(days),int(hours),int(minutes),int(seconds)))
        sys.stdout.flush()
        time.sleep(1)
    days, notdays = divmod(int(waittime), 86400)
    hours, nothours = divmod(notdays, 3600)
    minutes, seconds = divmod(nothours, 60)
    sys.stdout.write("\rslept {:0>2}:{:0>2}:{:0>2}:{:0>2} ".format(int(days),int(hours),int(minutes),int(seconds)) + '(' + str(round(waittime,1)) + 's)'"\n")

def saferequest(url):
    time1 = safetime() 
    livetimer(time1)
    get = requests.get(url)
    if 'safe_get_counter' not in str(globals()):
        global safe_get_counter
        safe_get_counter = 1
    else:
        safe_get_counter += 1
    print("Request " + str(safe_get_counter) + " complete")
    return(get)

with open('D:\Documents\Email_Credentials\SenderEmail.txt', 'r', encoding="utf-8") as cred1: 
    sender = str(cred1.read())
cred1.close()
with open('D:\Documents\Email_Credentials\RecieverEmail.txt', 'r', encoding="utf-8") as cred2: 
    reciever = str(cred2.read())
cred2.close()
with open('D:\Documents\Email_Credentials\Password.txt', 'r', encoding="utf-8") as cred3: 
    password = str(cred3.read())
cred3.close()

def EmailAlert_Blocked():
    port = 0
    smpt_server = 'smtp.gmail.com'
    sender_email = sender
    receiver_email = reciever
    password = password
    message = '''\
Subject: Your Scrape has been blocked

Try to see if it's a reCaptcha or a full block'''

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smpt_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

def EmailAlert_Finished():
    port = 0
    smpt_server = 'smtp.gmail.com'
    sender_email = sender
    receiver_email = reciever
    password = password
    message = '''\
Subject: Your Scrape has completed

It's finished running, now just make sure the file is okay'''

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smpt_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

def EmailAlert_StartedNewLetter(letter):
    port = 0
    smpt_server = 'smtp.gmail.com'
    sender_email = sender
    receiver_email = reciever
    password = password
    message = 'Subject: Scrape of ' + str(letter) + ' has started\n\nYour scrape of azlyrics has started looking for artists whos names start with the letter ' + str(letter)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smpt_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

def EmailAlert_Crashed():
    port = 0
    smpt_server = 'smtp.gmail.com'
    sender_email = sender
    receiver_email = reciever
    password = password
    message = '''\
Subject: Your Script Has Crashed

There has been a critical error and the try/except block was triggered'''

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smpt_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

az = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "19"]
abc = ["a", "b", "c"]
example = ['s']
yesbank = ["yeah", "yea", "ye", "y", "yee", "yeh", "yes", "yesh", "yush", "yup", "yep", "affirmative", "yes please", "sure", "ok", "okay", "o.k."]
nobank = ["nah", "na", "no", "nope", "n", "no thank you", "no thanks", "negative", "noo", "nooo", "nononono", "nothx"]

decision = False
while decision == False:
    answer = input('Is this your first time running this code?\n')
    if answer.lower() in yesbank:
        RUsure = input('Are you sure?  This will delete any previous file outputs.\n')
        if RUsure.lower() in yesbank:
            print('Reformatting output file in 10s')
            livetimer(10)
            with open('summersc_project1_allSongs_urls.csv', 'w', encoding="utf-8") as output_file1:
                output_file1.write("Artist Name,Album (Year),Song Name,URL\n")
            output_file1.close()
            decision = True
        elif RUsure in nobank:
            print("Alright, I'll ask again:")
        else:
            print("Error: unrecognized input\nReturning to start...")
    elif answer.lower() in nobank:
        print("Type the name of the artist you'd like to start on, or type 'ABORT' if you'd like to try again")
        print("(Be sure to use correct capitalization and replace all commas with semicolons)")
        starting_artist = str(input('Artist: '))
        if starting_artist == 'ABORT':
            print('Pickup aborted, returning to start...')
        else:
            lastruntime = float(input('How long in seconds was the last program running for?\n'))
            safe_get_counter = int(input('How many requests had been made?\n'))
            print('Pickup location set!')
            starttime = starttime - lastruntime
            decision = True
    else:
        print("Error: unrecognized input\nReturning to start...")

try:
    for letter in example:
        current_letter = str(letter)
        time.sleep(0.1)
        print('Writing data for ' + current_letter + '...')
        EmailAlert_StartedNewLetter(current_letter)
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
                letter_artists.append(item.text.replace(',',';'))
        letter_urls = ["https://www.azlyrics.com/" + addition for addition in half_links]

        all_urls = []
        all_albums = []
        all_songs = []
        all_artists = []
        while str(letter_artists[0]) != str(starting_artist):
            letter_artists.pop(0)
            letter_urls.pop(0)
        print('starting with ' + str(letter_artists[0]) + '\nNext 10 artists:')
        print('starting URL: ' + str(letter_urls[0]))
        print(str(letter_artists[1]) + '\n' + str(letter_artists[2]) + '\n' + str(letter_artists[3]))
        print(str(letter_artists[4]) + '\n' + str(letter_artists[5]) + '\n' + str(letter_artists[6]))
        print(str(letter_artists[7]) + '\n' + str(letter_artists[8]) + '\n' + str(letter_artists[9]) + '\n' + str(letter_artists[10]))
        input('Continue?')
        ziplist = list(zip(letter_artists, letter_urls))
        for item in ziplist:
            class_present = False
            while class_present == False:
                current_artist = item[0].replace(',',';')
                current_url = item[1]
                time.sleep(0.1)
                page = saferequest(current_url)
                bs = BeautifulSoup(page.content, "html.parser")
                divs = bs.find_all("div")
                for div in divs:
                    if div.has_attr("class"):
                        if div.attrs["class"][0] == "album":
                            class_present = True
                        elif div.attrs["class"][0] == "listalbum-item":
                            class_present = True
                if class_present == False:
                    print("Error 404: Data not found\nPausing script...\nThere's probably a reCaptcha, Please wait a moment and visit https://azlyrics.com")
                    EmailAlert_Blocked()
                    input("Hit ENTER when it is safe to continue")
                    input("You have hit ENTER are you sure it is safe? (ENTER)")
                    input("Last chance to check, are you REALLy sure? (ENTER)")

            current_album2 = ''
            time.sleep(0.1)
            print("Artist: " + str(current_artist) + '\nURL: ' + str(current_url) + '\nStatus: ' + str(page.status_code))
            for div in divs:
                if div.has_attr("class"):
                    if div.attrs["class"][0] == "album":
                        current_album2 = div.text.replace(',',';')
                    elif div.attrs["class"][0] == "listalbum-item":
                        all_urls.append(div.a.get('href'))
                        all_albums.append(current_album2)
                        all_songs.append(div.text.replace(',',';'))
                        all_artists.append(current_artist)
                        with open('summersc_project1_allSongs_urls.csv', 'a+', encoding="utf-8") as output_file2: 
                            output_file2.write(str(current_artist) + ',' + str(current_album2) + ',' + str(div.text.replace(',',';')) + ',' + str(div.a.get('href')) + '\n')
                        output_file2.close()
            time.sleep(0.1)
            print("Data for " + str(current_artist) + " written to file")
            time.sleep(0.1)
            runtime()
            print("  ")
        time.sleep(0.1)
        print('Completed data for ' + current_letter)
        print("  ")
    EmailAlert_Finished()
except: 
    EmailAlert_Crashed()
    traceback.print_exc()