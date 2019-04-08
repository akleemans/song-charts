from __future__ import division
import csv

entries = []
total_weeks = 2620

for week in range(1, total_weeks):
    with open('raw/' + str(week) + '.html', 'r') as read_file:
        page = read_file.read()
    page = page.decode('utf-8').encode('utf8')
    page = page.split('<h1>Schweizer Hitparade - Textversion</h1>')[1].split('</td></tr></table>')[0]
    week_date = page.split('<h2>')[1].split('</h2>')[0]
    year = week_date.split('.')[-1]
    raw_songs = page.split('<b>Singles</b><br>')[1].split('<br>')
    
    new_entries = []
    for song in raw_songs:
        song = song.strip()
        if song == '': break
        position = int(song.split('.')[0])
        interpret = song.split(')')[1].split(' - ')[0].strip()
        title = '('.join(' - '.join(song.split(' - ')[1:]).split('(')[:-2]).strip()
        new_entries.append((week, week_date, year, position, interpret, title))
    print 'Week', week, ', collected', len(new_entries), 'new songs'
    entries.extend(new_entries)

#  (-) The Hollies - He Ain't Heavy - He's My Brother (1. Woche) (Hansa/-)<br>

print 'Collected', len(entries), 'entries, saving'

with open('all_entries.csv', 'wb') as write_file:
    csvwriter = csv.writer(write_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for song in entries:
        csvwriter.writerow(song)

        
