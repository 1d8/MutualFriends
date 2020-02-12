from bs4 import BeautifulSoup
from requests import get
import re
import os
import json
import sys
headers = ({'User-Agent':
			'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
			
def scrape():
	global relatedusers
	global imglinks
	relatedusers = {}
	imglinks  = []
	url = 'http://insee.me/u/' + sys.argv[1] + '/following'
	request = get(url, headers=headers)
	soup = BeautifulSoup(request.text, 'html.parser')
	card = soup.find_all('div', class_='card')
	for i in card:
		user = i
		user = user.text
		user = user.replace('\n', '')
		relatedusers[user] = ''

	urlpattern = re.compile(r'([A-Za-z]+://)([-\w]+(?:\.\w[-\w]*)+)(:\d+)?(/[^.!,?"<>\[\]{}\s\x7F-\xFF]*(?:[.!,?]+[^.!,?"<>\[\]{}\s\x7F-\xFF]+)*)?', re.IGNORECASE)
	for i in card:
		imgusers = soup.find_all('img', alt=True)
		lstimgs = imgusers[2:]
		lstimgs.pop()
	for j in lstimgs:
		j = str(j)
		#this is for finding img links to profile imgs
		for match in re.findall(urlpattern, j):
			match = ''.join(map(str, match))
			match2 = str(match)
			match2 = ''.join(match2)
			match2 = match2.replace('amp;', '')
			imglinks.append(match2)
	for x in relatedusers:
		relatedusers[x] = imglinks[0]
		imglinks.pop(0)

def dbfile():
	f = open('dbfile.txt', 'a+')
	f.write('--------------------------------------------------')
	f.write('\n\n\n')
	f.write(sys.argv[1] + ' ' + 'Follows:')
	f.write('\n')
	f.write('   ')
	#this checks if the -i flag exists to ensure that the user wants images
	try:
		if sys.argv[2] == '-i':
			for k, v in relatedusers.items():
				f.write(k + ' ' + v)
				f.write('\n')
				f.write('   ')
	#if the -i flag isn't there, it causes an Indexerror, in this case go here
	except IndexError:
		for k, v in relatedusers.items():
			f.write(k)
			f.write('\n')
			f.write('   ')
	f.close()

try:
	if sys.argv[1] == '-help' or sys.argv[1] == '-h':
		print('''Usage: Python3 [script-name-here] [username here] [flags]
		Flags:
			-h - Displays this message
			-i - Displays user images
		
		Coded by 1d8
		github.com/1d8
		I love criticism.''')
	else:
		scrape()
		dbfile()
except IndexError:
	print('''Usage: Python3 [script-name-here] [username here] [flags]
		Flags:
			-h - Displays this message
			-i - Displays user images''')
	sys.exit()
