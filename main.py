import pandas as pd
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
import requests
from urllib.parse import urljoin

url = "https://www.imdb.com/chart/top/"
base = "https://www.imdb.com/"

r = requests.get(url)
soup = bs(r.text, 'html.parser')

movies = soup.find('tbody', class_='lister-list').find_all('tr')
results = []
for movie in tqdm(movies):
    title = movie.find('td', class_='titleColumn').find('a').text
    year = movie.find('td', class_='titleColumn').find('span').text[1:-1]
    poster_link = movie.find('td', class_='posterColumn').find('a').find('img')['src']
    movie_link = movie.find('td', class_='titleColumn').find('a')['href']
    movie_link = urljoin(base, movie_link)
    result = {
        'title': title,
        'year': year,
        'poster': poster_link,
        'movie': movie_link
    }
    results.append(result)

df = pd.DataFrame(results)

df.to_csv('best_movies.csv', index=False)
