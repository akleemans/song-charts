from __future__ import division
import csv
import json

entries = []

print 'Reading compiled entries...'
with open('all_entries.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
        week = int(row[0])
        week_date = row[1]
        year = int(row[2])
        position = int(row[3])
        interpret = row[4]
        title = row[5]
        entries.append((week, week_date, year, position, interpret, title))

print 'Read', len(entries), 'entries, aggregating toplist...'
aggregated = {}
year_map = {}
for song in entries:
    key = song[4] + ' - ' + song[5]
    position = song[3]
    score = 0.95 ** (position - 1) * 100
    if key in aggregated:
        aggregated[key] += score
    else:
        aggregated[key] = score
    
    if key not in year_map: year_map[key] = song[2]

print 'Aggregated', len(aggregated), 'songs, writing to CSV...'
toplist = []
pos = 1
for key, value in sorted(aggregated.iteritems(), key=lambda (k,v): (v,k), reverse=True):
    # year of first appearance
    year = year_map[key]
    toplist.append((pos, key, round(value, 3), year))
    pos += 1
    
with open('alltime_charts.csv', 'wb') as write_file:
    csvwriter = csv.writer(write_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(['position','artist_title','score','year'])
    for song in toplist:
        csvwriter.writerow(song)
        

# prepare json
json_array = []
for song in toplist:
    s = {"pos": song[0], "title": song[1], "value": song[2], "year": song[3]}
    json_array.append(s)  
  
json_data = json.dumps(json_array)

with open('alltime_charts.json', 'w') as write_file:
    write_file.write(json.dumps(toplist)) #json_data)

print 'Category 1: all-time charts:'
for song in toplist[:20]:
    print '#', song[1], '(' + str(song[3]) + ')', '-', song[2], 'points'

### TODO distribution of points - grafic & songs int total / with more than 1 / 100 / 1000 points
bins = {} 
for song in toplist:
    value = int(song[2] / 100.0)
    if value in bins: bins[value] += 1
    else: bins[value] = 1
    
print 'Bins:', bins


print '\n\n================\n\n'
print 'Category 2: most weeks in #1'

year_list = {}
for song in entries:
    key = song[4] + ' - ' + song[5]
    position = song[3]
    if position == 1:
        if key in year_list: year_list[key] += 1
        else: year_list[key] = 1

i = 1
for key, value in sorted(year_list.iteritems(), key=lambda (k,v): (v,k), reverse=True)[:20]:
    print '#', key, '(' + str(value) + ' weeks)'
    i += 1

print '\n\n================\n\n'
print 'Category 3: most weeks in #100'

year_list = {}
for song in entries:
    key = song[4] + ' - ' + song[5]
    if key in year_list: year_list[key] += 1
    else: year_list[key] = 1

i = 1
for key, value in sorted(year_list.iteritems(), key=lambda (k,v): (v,k), reverse=True)[:20]:
    print '#', key, '(' + str(value) + ' weeks)'
    i += 1

print '\n\n================\n\n'
print 'Category 4: charts per year'
per_year = 3
for year in range(1968, 2020):
    print '\nYear', year
    i = 1
    for song in toplist:
        if song[3] == year:
            print '#', song[1]
            i += 1
        if i > per_year:
            break

print '\n\n================\n\n'
print 'Category 5: charts per artist'

artists = {}
count = 0
for song in toplist:
    key = song[1].split(' - ')[0]
    value = song[2]
    if key in artists:
        artists[key] += value
    else:
        artists[key] = value
        count += 1

print 'Total artists:', count
print
print 'Most succesful artists:'
i = 1
for key, value in sorted(artists.iteritems(), key=lambda (k,v): (v,k), reverse=True)[:50]:
    print '#', key, '(' + str(int(value)) + ' points)'
    i += 1

