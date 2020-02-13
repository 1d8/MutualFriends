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
	global request
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
	#try:
	if sys.argv[2] == '-i' or sys.argv[2] == '--images':
		for k, v in relatedusers.items():
			f.write(k + ' ' + v)
			f.write('\n')
			f.write('   ')
	else:
		for k, v in relatedusers.items():
			f.write(k + ' ')
			f.write('\n')
			f.write('  ')
	#if the -i flag isn't there, it causes an Indexerror, in this case go here
	#except IndexError:
	#	for k, v in relatedusers.items():
	#		f.write(k)
	#		f.write('\n')
	#		f.write('   ')
	f.close()


def dlimgofrelatedusers():
	os.system('mkdir imgs-of-related-to-' + sys.argv[1] + ' > /dev/null 2>&1')
	os.chdir('imgs-of-related-to-' + sys.argv[1])
	print('Downloading profile pics of following list...')
	i = 0
	for k, v in relatedusers.items():
		i = str(i)
		os.system('curl ' + "'" + v + "'" + ' -o img' + i + '.jpg > /dev/null 2>&1')
		i = int(i)
		i+=1


def dlimgsoftarget():
	os.system('mkdir imgs-of-' + sys.argv[1] + '> /dev/null 2>&1')
	os.chdir('imgs-of-' + sys.argv[1])
	url = "http://insee.me/u/" + sys.argv[1]
	request = get(url, headers=headers)
	soup = BeautifulSoup(request.text, 'html.parser')
	mainmedia = soup.find_all('a', class_='media main-media')
	print('Downloading images posted by target')
	x = 0
	for image in mainmedia:
		image = image.div
		image = image['data-src']
		x = str(x)
		os.system('curl ' + "'" + image + "'" + ' -o img' + x + '.jpg > /dev/null 2>&1')
		x = int(x)
		x += 1
	print('Images downloaded to', 'imgs-of-' + sys.argv[1])
	

#execute first ->
try:
	if sys.argv[1] == '--help' or sys.argv[1] == '-h':
		print('''
				Coded by 1d8
				github.com/1d8
			NOTE: Only 1 flag can be passed at a time
		Usage: Python3 [script-name-here] [username here] [flag]
		Flags:
			-h or --help- Displays this message
			-i or --images - Displays user images
			-n or --normal - Scrapes only usernames
			-dr or --download-related - Downloads profile pics of users target follows
			-dt or --download-target - Downloads first 10 images posted by target
		''')
	elif sys.argv[2] == '-dr' or sys.argv[2] == '--download-related':
		scrape()
		dlimgofrelatedusers()
	elif sys.argv[2] == '-i' or sys.argv[2] == '--images':
		scrape()
		dbfile()
	elif sys.argv[2] == '-dt' or sys.argv[2] == '--download-related':
		dlimgsoftarget()
	elif sys.argv[2] == '-n' or sys.argv[2] == '--normal':
		scrape()
		dbfile()
except IndexError:
	print('''
				Coded by 1d8
				github.com/1d8
			NOTE: Only 1 flag can be passed at a time
		Usage: Python3 [script-name-here] [username here] [flag]
		Flags:
			-h or --help- Displays this message
			-i or --images - Displays user images
			-n or --normal - Scrapes only usernames
			-dr or --download-related - Downloads profile pics of users target follows
			-dt or --download-target - Downloads first 10 images posted by target
		''')
	sys.exit()
