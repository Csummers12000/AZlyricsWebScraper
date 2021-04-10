import pandas as pd

#this section is only here because i accidentally forgot to replace commas with semicolens in the songtitle field while scraping
#the error in the code is already fixed, but I didnt catch it until after the 30 hour scrape had completed
'''
with open('summersc_project1_allSongs_urls.csv', 'r', encoding="utf-8") as inputfile:
    with open('CLEANED_summersc_project1_allSongs_urls.csv', 'w', encoding="utf-8") as genfile:
            None
    genfile.close()
    for line in inputfile:
        if ', ' in line:
            line = line.replace(', ', '; ')
        if ',0' in line:
            line = line.replace('0,0', '0;0')
        if 'A,B,C,D' in line:
            line = line.replace('A,B,C,D', 'A;B;C;D')
        if '0,33' in line:
            line = line.replace('0,33', '0;33')
        if '1,0' in line:
            line = line.replace('1,0', '1;0')
        if '1,2,3' in line:
            line = line.replace('1,2,3', '1;2;3')
        if '84,000' in line:
            line = line.replace('84,000', '84;000')
        if '0,7' in line:
            line = line.replace('0,7', '0;7')
        if '1,2' in line:
            line = line.replace('1,2', '1;2')
        if '3,4' in line:
            line = line.replace('3,4', '3;4')
        if '4,0' in line:
            line = line.replace('4,0', '4;0')
        if '愛,태우다' in line:
            line = line.replace('愛,태우다', '愛;태우다')
        with open('CLEANED_summersc_project1_allSongs_urls.csv', 'a+', encoding="utf-8") as outputfile:
            outputfile.write(line)
        outputfile.close()
inputfile.close()
'''


csv = pd.read_csv('CLEANED_summersc_project1_allSongs_urls.csv', quotechar='"')
csv.columns = ['Artist_Name', 'Album_Year', 'Song_Name', 'URL']
df = pd.DataFrame(csv)
print(len(df.index))
print(df)
input('stop')

remove_list = []
years_unique = []
for index, row in df.iterrows():
    try:
        year = int(str(row['Album_Year'])[-5:-1])
        if year == 104:
            remove_list.append(index)
            #row['Album_Year'] = str(row['Album_Year'])[:-7]
        elif year not in years_unique:
            years_unique.append(year)
    except:
        remove_list.append(index)
    if row['URL'][0:3] != '../':
        remove_list.append(index)

df = df.drop(remove_list)


def label_Year(row):
    return(int(str(row['Album_Year'])[-5:-1]))
def fix_album(row):
    return(str(row['Album_Year'])[:-7])
def label_Before1970(row):
    if int(row['Year']) < 1970:
        return True
    else:
        return False

df['Year'] = df.apply(lambda row: label_Year(row), axis=1)
#df['Album_Year'] = df.apply(lambda row: fix_album(row), axis=1)
#df.rename(columns={'Album_Year':'Album'}, inplace=True)
df['Before1970'] = df.apply(lambda row: label_Before1970(row), axis=1)


keeplist = []
pre1970 = df.Before1970[df.Before1970.eq(True)].sample(frac = 0.1).index
for item in pre1970:
    keeplist.append(item)

for intyear in years_unique:
    if intyear < 1970:
        None
    else:
        post1970 = df.Year[df.Year.eq(intyear)].sample(n = 80).index
        for item in post1970:
            keeplist.append(item)

print(len(keeplist))

droplist = []
for index, row in df.iterrows():
    if index not in keeplist:
        droplist.append(index)

df = df.drop(droplist)

dfcsv = df

del dfcsv['Year']
del dfcsv['Before1970']

dfcsv.to_csv('summersc_project1_sampledSongs_urls.csv', index=False, quotechar='"')


