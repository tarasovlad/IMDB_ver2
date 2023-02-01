import requests as requests
from bs4 import BeautifulSoup
import psycopg2

movie_id = []
movie_name_year= []
imdb_data = []

url = 'https://www.imdb.com/search/title/?title_type=feature,tv_movie,documentary,short,tv_special&release_date=2022-01-01,2022-12-31&num_votes=100,&sort=num_votes,asc&count=20&start=1&ref_=adv_nxt'
response = requests.get(url)
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
soup = BeautifulSoup(response.content, 'html.parser')


movie_data = soup.findAll('div', attrs={'class': 'lister-item mode-advanced'})

for store in movie_data:
    movie_id_raw = str(store.h3.a)
    s = [i[2:] for i in movie_id_raw.split('/') if i.startswith('tt')]
    movie_id.append(*s)

def create_connecthoin(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except 'OperationalError' as e:
        print(f"The error '{e}' occurred")
    return connection

connection = create_connecthoin

def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except 'OperationalError' as e:
        print(f"The error '{e}' occurred")

for i in movie_id:
    imdb_data.append((i, ' ', ' ', ' '))

imdb_data_records = ", ".join(["%s"] * len(imdb_data))

insert_query = (
        f"INSERT INTO raw_data.imdb_data(id_imdb, release_year, movie_name_original, movie_name_us) VALUES {imdb_data_records}"
    )

connection.autocommit = True
cursor = connection.cursor()
cursor.execute(insert_query, imdb_data)

