import bs4 as bs4
import requests as requests
from bs4 import BeautifulSoup
import asyncio

movie_id = []
movie_name_year= []
USA_movie_name = []
Original_movie_name = []

url = 'https://www.imdb.com/search/title/?title_type=feature,tv_movie,documentary,short,tv_special&release_date=2022-01-01,2022-12-31&num_votes=100,&sort=num_votes,asc&count=20&start=1&ref_=adv_nxt'
response = requests.get(url)
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
soup = BeautifulSoup(response.content, 'html.parser')


movie_data = soup.findAll('div', attrs={'class': 'lister-item mode-advanced'})

for store in movie_data:
    movie_id_raw = str(store.h3.a)
    s = [i[2:] for i in movie_id_raw.split('/') if i.startswith('tt')]
    movie_id.append(*s)

print(movie_id)

def movie_Orig(movie_id):
    for digital_id in movie_id:
        link = f'https://www.imdb.com/title/tt{digital_id}/releaseinfo'
        response_page = requests.get(link, headers=headers)
        soup_page = BeautifulSoup(response_page.content, 'html.parser')
        AKA_name = soup_page.find('table', class_='ipl-zebra-list akas-table-test-only')
        try:
            Original_movie_name.append(AKA_name.find('td', class_= 'aka-item__title').text)
        except:
            Original_movie_name.append('')
    return Original_movie_name

print(movie_Orig(movie_id))