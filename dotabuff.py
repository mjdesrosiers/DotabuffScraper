import urllib2
from BeautifulSoup import BeautifulSoup
from pprint import pprint as pp
import time
import json

HID = 0
PLAYS = 2
WR = 3
KDA = 4

CACHE_FILENAME = "cache.json"

MAX_FILE_AGE = 86400 # seconds - timeout of data is a day

url = "http://www.dotabuff.com/players/{pid}/heroes"

#@TODO move these into a config file
people = { 'mike': 136754293,
"woody": 30075956,
"stu": 78479931,
"jon": 65091923,
"matt": 119518678,
"brian": 107023417,
"andy": 84388592}

def get_heroes_list(name):
	soup = get_soup_from_url(generate_url_for(name))
	herosoup = soup.table.contents[1]
	heroes = {}
	for hero in herosoup:
		name = hero.contents[HID].img['title']
		matches = int(hero.contents[PLAYS].contents[0])
		wr = float(hero.contents[WR].contents[0][:-1]) / 100.0
		kda = float(hero.contents[KDA].contents[0])
		heroes[name] = {"matches": matches, "wr": wr, "kda": kda}
	return heroes

def get_soup_from_url(url):
	f = urllib2.urlopen(url, timeout=1)
	soup = BeautifulSoup(f.read())
	return soup	

def generate_url_for(person):
	return url.format(pid=people[person])

def cache_data(people):
	now = time.time()
	data = {}
	data['time'] = int(now)
	data['stats'] = people
	strdata = json.dumps(data)
	with open(CACHE_FILENAME, 'w') as f:
		f.write(strdata)

def load_cached_data():
	data = None
	with open(CACHE_FILENAME, 'r') as f:
		data = json.load(f)
	return data

def get_data():
	try:
		data = load_cached_data()
		now = time.time()
		age = now - data['time']
		if age < MAX_FILE_AGE:
			print("\tUsing cached data")
			return data['stats']
	except Exception, e:
		pass
	print("\tScraping new data")
	data = scrape_new_data()
	cache_data(data)
	return data

def scrape_new_data():
	data = dict()
	for person in people:
		heroes = get_heroes_list(person)
		data[person] = heroes
	return data

def find_person_best_at_most_heroes(data, threshold = 0.0, wrthresh = 0.0):
	heronames = []

	# collect all the active hero names
	for person in data:
		for hero in data[person]:
			if hero not in heronames:
				heronames.append(hero)

	bestatheros = dict()

	# find best at each hero
	for hero in heronames:
		# initialize to unknown
		bestatheros[hero] = ['unknown', -1.0]

		# iterate over each person
		for person in people:
			# if this person has played 
			if hero in data[person]:
				wr = data[person][hero]['wr']
				matches = data[person][hero]['matches']
				if wr > bestatheros[hero][1] and wr > 0:
					if matches > threshold and wr > wrthresh:
						bestatheros[hero] = [person, wr]
	number_of_best = dict()
	for person in people:
		number_of_best[person] = 0
	number_of_best['unknown'] = 0
	for hero in bestatheros:
		number_of_best[bestatheros[hero][0]] += 1
	best = 'unknown'
	number_of_best['unknown'] = 0
	for person in people:
		if number_of_best[person] > number_of_best[best]:
			best = person
	dupes = []
	dupes.append(best)
	for person in people:
		if person != best:
			if number_of_best[person] == number_of_best[best]:
				dupes.append(person)
	if len(dupes) == 1:
		return (best, number_of_best[best])
	else:
		return (dupes, number_of_best[best])

#@TODO Actually do analytics
if __name__ == "__main__":
	data = get_data()
	for i in range(1, 120):
		best = find_person_best_at_most_heroes(data, i, 0.5)
		if best is not None:
			print("at minimum of {} matches, person best at most heroes is {} with {}".format(i, best[0], best[1]))




