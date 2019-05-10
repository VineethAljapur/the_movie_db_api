import http.client
import json
import time
import sys
import collections

base_url = 'api.themoviedb.org'
api_key = sys.argv[1]
url = ''.join(['/3/discover/movie?with_genres=18&sort_by=popularity.desc&primary_release_year=2004&api_key=', api_key])

conn = http.client.HTTPSConnection(base_url)

# To get top 350 movies in Drama
results = []
hits = 0
while not hits or r1.status == 200:
	hits += 1
	if hits > 18: break
	time.sleep(0.25)
	conn.request("GET", url + '&page=' + str(hits))
	r1 = conn.getresponse()
	data = json.loads(r1.read())
	for hit in data['results']:
		results.append(hit)
results = results[:350]
with open('./movie_ID_name.csv', 'w') as f:
    for hit in results:
        f.write(str(hit['id']) + ',' + hit['title'] + '\n')
# print (len(results))

# To get the similar movies to them
conn = http.client.HTTPSConnection(base_url)
similar = []
for movie in results:
    time.sleep(0.25)
    conn.request("GET", '/3/movie/'+ str(movie['id']) + '/similar?&api_key=' + api_key)
    r1 = conn.getresponse()
    data = json.loads(r1.read())
    count = 0
    for hit in data['results']:
        count += 1
        if count > 5: break
        similar.append((movie['id'], hit['id']))
temp = dict()
sorted_similar = sorted(similar)
deduplicated = {}
for item in sorted_similar:
    if item not in temp and item[::-1] not in temp:
        deduplicated[item] = ''
    temp[item] = ''
final_similar = []
for item in similar:
    if item in deduplicated:
        final_similar.append(item)
with open('./movie_ID_sim_movie_ID.csv', 'w') as f:
    for pair in final_similar:
        f.write(str(pair[0]) + ',' + str(pair[1]) + '\n')