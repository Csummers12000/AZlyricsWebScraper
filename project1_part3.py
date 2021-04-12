import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random
import smtplib, ssl
import traceback
import sys
import pickle

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

def EmailAlert_Crashed_ver_2(errName, errTB):
    port = 0
    smpt_server = 'smtp.gmail.com'
    sender_email = sender
    receiver_email = reciever
    password = password
    header = 'Error: ' + str(errName)
    body = str(errTB)
    message = 'Subject: {}\n\n{}'.format(header, body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smpt_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)



csv = pd.read_csv('summersc_project1_sampledSongs_urls.csv', quotechar='"')
csv.columns = ['Artist_Name', 'Album_Year', 'Song_Name', 'URL']
df = pd.DataFrame(csv)

try:
    with open('summersc_project1_lyrics.csv', 'r', encoding="utf-8") as lyricscsv:
        None
    lyricscsv.close()
    print('Partial Lyrics CSV detected')
    lyricsfound = True
except:
    with open('summersc_project1_lyrics.csv', 'w', encoding="utf-8") as lyricscsv:
        lyricscsv.write('Artist_Name' + ',' + 'Album_Year' + ',' + 'Song_Name' + ',' + 'URL' + ',' + 'Lyrics' + '\n')
    lyricscsv.close()
    print('Partial Lyrics CSV not detected - Lyricscsv initialized')
    lyricsfound = False
time.sleep(0.1)

#listcontents[index of last url used, runtime in seconds, number of requests]
checkpoint = [-1, 0, 0]
try:
    with open('checkpoint', 'rb') as picklejar:
        checkpoint = pickle.load(picklejar)
    picklejar.close()
    print('Pickle Jar loaded')
    picklejarfound = True
except:
    with open('checkpoint', 'wb') as picklejar:
        pickle.dump(checkpoint, picklejar)
    picklejar.close()
    print('Pickle Jar not detected - New Pickle Jar createad')
    picklejarfound = False
time.sleep(0.1)

lastindex = int(checkpoint[0])
starttime = starttime - checkpoint[1]
safe_get_counter = checkpoint[2]
print('Loading data...')
time.sleep(0.1)
print('  last index scraped: ' + str(lastindex))
days2, notdays2 = divmod(float(checkpoint[1]), 86400)
hours2, nothours2 = divmod(notdays2, 3600)
minutes2, seconds2 = divmod(nothours2, 60)
print("  Time added: {:0>2}:{:0>2}:{:0>2}:{:0>2} ".format(int(days2),int(hours2),int(minutes2),int(seconds2)))
print('  Requests added: ' + str(safe_get_counter))
time.sleep(0.1)

if picklejarfound != lyricsfound:
    input("Error: File Mismatch")

def fullurl(row):
    return 'https://www.azlyrics.com' + str(row['URL'][2:])
df['URL'] = df.apply(lambda row: fullurl(row), axis=1)

testurl = 'https://www.azlyrics.com/lyrics/siames/mrfear.html'
try:
    for index, row in df.iterrows():
        if index > lastindex:
            print('Getting data for row ' + str(int(index + 1)) + ' (index ' + str(index) + ')')
            time.sleep(0.1)
            print('  Song: ' + str(row['Song_Name']))
            time.sleep(0.1)
            print('  Album: ' + str(row['Album_Year']))
            time.sleep(0.1)
            print('  Artist: ' + str(row['Artist_Name']))
            time.sleep(0.1)
            print('  URL: ' + str(row['URL']))
            time.sleep(0.1)
            page = saferequest(row['URL'])
            #page = saferequest(testurl)
            bs = BeautifulSoup(page.content, "html.parser")
            noattrs = bs.findAll('div', attrs={'class': None,'id': None})

            if len(noattrs) != 1:
                print('\nError: divs != 1\nCheck azlyrics for a block before troubleshooting')
                print(row)
                print(noattrs)
                homemadeTB = 'Row:\n' + str(row) + '\n\nAttributes:\n ' + str(noattrs) + '\n\nIndex:\n' + str(index) + '\n\nRequests:\n' + str(safe_get_counter)
                EmailAlert_Crashed_ver_2('unexpected attribute length', homemadeTB)
                input('Continue?')
                print('Continuing in:')
                livetimer(15)
            else:
                #lyricslist.append(noattrs[0].text.replace(',', ';'))
                nocommas = noattrs[0].text.replace(',', ';')
                nobreaks = nocommas.replace('\r', '|r|')
                nonewline = nobreaks.replace('\n', '|n|')
                with open('summersc_project1_lyrics.csv', 'a', encoding="utf-8") as lyricscsv:
                    lyricscsv.write(str(row['Artist_Name']) + ',' + str(row['Album_Year']) + ',' + str(row['Song_Name']) + ',' + str(row['URL']) + ',' + str(nonewline) + '\n')
                lyricscsv.close()
                checkpoint[0] = index
                checkpoint[1] = runtime()
                checkpoint[2] = safe_get_counter
                with open('checkpoint', 'wb') as picklejar:
                    pickle.dump(checkpoint, picklejar)
                picklejar.close()
                print('CSV and Pickle Jar updated\n')
                time.sleep(0.1)
    EmailAlert_Finished()
except KeyboardInterrupt:
    print('\n\nKeyboardInterrupt')
except Exception as e:
    errorName = e
    errorTraceback = traceback.format_exc()
    print(errorTraceback)
    EmailAlert_Crashed_ver_2(errorName, errorTraceback)

