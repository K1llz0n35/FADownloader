import configparser
import urllib
import requests, wget, ast, re, time
from bs4 import BeautifulSoup
import json
import os

# When referencing keywords, 1st page can be called with q=tag but following pages must be retrieved using NextPage: Next
# TODO function grabs tag, searched on furaffinity.net/@keywords%20{tag} (remove brackets)
# call function to grab posts and thumbnails from page
# first page is q=@Keywords {tag} following pages are q=@Keywords {tag}&page={int} where int is page number
# page number is 0 indexed, 1 = pg 2, 2 = pg 3, etc.

# setup config file
config = configparser.ConfigParser()
config.read('config.ini')
# set download path from config
downloadpath = config['configs']['download_path']
# set cookies from config
cookies = {
    'a': str(config['configs']['cookie_a']),
    'b': str(config['configs']['cookie_b'])
}
# define whether to include scrap with gallery download
scrap = config['configs']['scrap']


def save_entries_to_files(filepath):
    # Open the JSON file for reading
    with open(filepath, 'r', encoding="utf8") as file:
        data = json.load(file)

    # Loop through each entry in the JSON data
    for entry in data:
        # Get the id value
        file_id = entry['id']
        print(file_id)
        jsonout = '{"tags": ['
        jsonout = jsonout + f'"title: {entry["title"]}"'
        jsonout = jsonout + f',"creator: {entry["username"]}"'
        if entry['tags']:
            taglist = entry['tags'].split(',')
            for tag in taglist:
                jsonout = jsonout + f',"{tag}"'
        jsonout = jsonout + f'],"urls": ["{entry["url"]}"]}}'
        # Define a new file path for saving the entry
        new_file_path = os.path.join('C:\\Temp\\sidecars', f'{file_id}.json')

        # Save the entry to the new file
        with open(new_file_path, 'w') as new_file:
            json.dump(ast.literal_eval(jsonout), new_file, indent=4)


def datafromsearch(tag, pg):
    r = requests.get(
        f'https://www.furaffinity.net/search/?q={tag}&page={pg}&perpage=42&order-by=date&order-direction=desc&range=all&rating-general=on&rating-mature=on&rating-adult=on&type-art=on&type-flash=on&type-photo=&type-music=&type-story=&type-poetry=&mode=extended',
        cookies=cookies)
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find('section', id='gallery-search-results')
    l = s.find_all('a')
    if l:
        count = 0
        links = []
        for link in l:
            if re.search('/view/', link.get('href')):
                if count % 2 == 0 or count == 0:
                    links.append(link.get('href'))
                count = count + 1
        print(links)
        time.sleep(1)
        return links


def datafrompage(slug):
    global imglink
    url = f'https://www.furaffinity.net{slug}'
    r = requests.get(url, cookies=cookies)
    time.sleep(1)
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find('div', class_='favorite-nav')
    image = s.find_all('a')
    for link in image:
        if link.text == 'Download':
            imglink = link.get('href')
            break
    suffix = imglink.split('.')[-1]
    filename = slug.split('/')[-2]
    download('https:' + imglink, filename + "." + suffix)
    print(filename + ' downloaded')
    data = {}
    s = soup.find('div', class_='submission-title')
    title = s.find_all('p')
    data['title'] = title[0].text
    s = soup.find('div', class_='submission-id-sub-container')
    artist = s.find_all('strong')
    data['creator'] = artist[0].text
    s = soup.find('section', class_='tags-row')
    print('grabbing tags')
    data['tags'] = []
    if s == None:
        pass
    else:
        tags = s.find_all('a')
        if tags.__len__() > 0:
            for tag in tags:
                data['tags'].append(tag.text)
    print('tags retrieved')
    data['id'] = filename
    dicttojson(data)


def dicttojson(dict):
    if 'id' in dict:
        print(dict['id'] + ' processing start')
        file_name = dict.pop('id')
        with open(f'{downloadpath}{file_name}.json', 'w') as json_file:
            json.dump(dict, json_file, indent=4)
        print('Finished Processing')


def datafromgallery(query, pg):
    r = requests.get('https://www.furaffinity.net/gallery/' + query + '/' + str(pg), cookies=cookies)
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find('section', id='gallery-gallery')
    l = s.find_all('a')
    if l:
        count = 0
        links = []
        for link in l:
            if re.search('/view/', link.get('href')):
                if count % 2 == 0 or count == 0:
                    links.append(link.get('href'))
                count = count + 1
        print(links)
        time.sleep(1)
        return links


def datafromscrap(query, pg):
    r = requests.get('https://www.furaffinity.net/scrap/' + query + '/' + str(pg), cookies=cookies)
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find('section', id='gallery-gallery')
    l = s.find_all('a')
    if l:
        count = 0
        links = []
        for link in l:
            if re.search('/view/', link.get('href')):
                if count % 2 == 0 or count == 0:
                    links.append(link.get('href'))
                count = count + 1
        print(links)
        time.sleep(1)
        return links


def datafromfavorites(query):
    running = True
    a = []
    q = 'favorites/' + query + '/'
    while running:
        url = 'https://www.furaffinity.net/' + q
        r = requests.get(url, cookies=cookies)
        time.sleep(1)
        soup = BeautifulSoup(r.content, 'html.parser')
        s = soup.find('div', class_='gallery-navigation')
        buttons = s.find_all('div')
        link = buttons[2]
        b = link.find('form', method='get')
        try:
            q = b.get('action')
        except:
            running = False
        s = soup.find('section', id='gallery-favorites')
        l = s.find_all('a')
        if l:
            count = 0
            for link in l:
                if re.search('/view/', link.get('href')):
                    if count % 2 == 0 or count == 0:
                        a.append(link.get('href'))
                    count = count + 1
    return a


def download(url, title):
    wget.download(url, downloadpath + title)


def downloader(query, type):
    running = True
    count = 1
    if type == 'tag':
        links = []
        while running:
            if count < 1:
                oldlinks = []
            else:
                oldlinks = links
            safe_query = urllib.parse.quote(query)
            links = datafromsearch(safe_query, count)
            if links == None or oldlinks == links:
                running = False
            if running:
                for link in links:
                    datafrompage(link)
            count = count + 1
    elif type == 'gallery':
        running = True
        while running:
            links = datafromgallery(query, count)
            if scrap:
                links.append(datafromscrap(query, count))
            if links == None:
                running = False
            if running:
                for link in links:
                    print(count, link.count(link))
                    datafrompage(link)
            count = count + 1
    elif type == 'favorites':
        links = datafromfavorites(query)
        for link in links:
            print(links.index(link))
            datafrompage(link)


def listfromfile(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return lines


def downloadfromlist(cookies):
    tags = listfromfile('tags.txt')
    artists = listfromfile('gallery.txt')
    favorites = listfromfile('favorites.txt')
    if tags.__len__() + artists.__len__() + favorites.__len__() == 0 or cookies.get(
            'a') == 'Cookie A Value Here' or cookies.get('b') == 'Cookie B Value Here' or downloadpath == 'C:\\Path\\To\\Downloads':
        raise Exception("Please read the ReadMe File before Running!!!")
    for tag in tags:
        downloader(tag, 'tag')
    for artist in artists:
        downloader(artist, 'gallery')
    for favorite in favorites:
        downloader(favorite, 'favorites')

downloadfromlist(cookies)