import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_html(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    return response.text


def get_last_page():
    url = 'https://tululu.org/l55/'
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    last_page = soup.select('.center .npage')[-1].text
    return int(last_page)


def get_books_url(start_page, end_page):
    books_url = []
    for page in range(start_page, end_page):
        page_url = f'https://tululu.org/l55/{page}'
        page_html = get_html(page_url)
        soup = BeautifulSoup(page_html, 'lxml')
        books_card = soup.select('.d_book')
        for book_card in books_card:
            book_url = urljoin(page_url, book_card.select_one('a').get('href'))
            books_url.append(book_url)
    return books_url


def get_book_response(book_num):
    url = f'https://tululu.org/txt.php?id={book_num}'
    response = requests.get(url, verify=False)
    response.raise_for_status()
    return response, url


def get_genres(soup):
    title_genre, name_genres = soup.select('.d_book')[1].text.split(sep=':')
    genres = name_genres.strip().replace('.', '').split(', ')
    return genres
