import urllib2
from BeautifulSoup import BeautifulSoup
from pprint import pprint as pp
HID = 0
PLAYS = 2
WR = 3
KDA = 4

url = "http://www.dotabuff.com/players/{pid}/heroes"
people = { 'mike': 136754293,
"woody": 30075956,
"stu": 78479931,
"jon": 65091923,
"matt": 119518678,
"brian": 107023417,
"andy": 84388592}

def get_heroes_list(name):
	url = generate_url_for(name)
	soup = get_soup_for(url)
	herosoup = soup.table.contents[1]
	heroes = {}
	for hero in herosoup:
		name = hero.contents[HID].img['title']
		matches = int(hero.contents[PLAYS].contents[0])
		wr = float(hero.contents[WR].contents[0][:-1])/100.0
		kda = float(hero.contents[KDA].contents[0])
		heroes[name] = {"matches": matches, "wr": wr, "kda": kda}
	return heroes

def get_soup_for(url):
	f = urllib2.urlopen(url, timeout=1)
	soup = BeautifulSoup(f.read())
	return soup	

def generate_url_for(person):
	return url.format(pid=people[person])

if __name__ == "__main__":
	for person in people:
		heroes = get_heroes_list(person)
		morethan5playscnt = len([h for h in heroes if heroes[h]['matches'] > 5])
		print("{}: {}".format(person, morethan5playscnt)) 	