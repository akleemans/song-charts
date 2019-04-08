from __future__ import division
import urllib2
import time

def download(url):
    f = urllib2.urlopen(url)
    data = f.read()
    f.close()
    time.sleep(0.2) # slow it down a tad
    return data

song_list = []
base_url = 'http://www.swisscharts.com/showcharttext.asp?week='
total_weeks = 2620 # April 2019

for week in range(1, total_weeks):
    url = base_url + str(week)
    page = download(url)
    # encoding seems to be latin1 (Windows) by default, convert it when saving
    page = page.decode('latin1').encode('utf-8')
    with open('raw/' + str(week) + '.html', 'w') as write_file:
        write_file.write(page)
    print 'Downloading...', round(week/total_weeks * 100.0, 2), '%'

