import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from sys import stderr


def eprint(*args, **kwargs):
    print(*args, file=stderr, **kwargs)


def check_response(response):
    if response.is_redirect:
        raise requests.HTTPError
    return


def get_html(url):
    response = requests.get(url, verify=False, allow_redirects=False)
    check_response(response)
    response.raise_for_status()
    return response.text


def get_last_page():
    url = 'https://tululu.org/l55/'
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    last_page = soup.select_one('.center .npage:last-of-type').text
    return int(last_page)


def get_books_urls(start_page, end_page):
    books_urls = []
    for page in range(start_page, end_page):
        page_url = f'https://tululu.org/l55/{page}'
        page_html = get_html(page_url)
        soup = BeautifulSoup(page_html, 'lxml')
        books_cards = soup.select('.d_book')
        for book_card in books_cards:
            book_url = urljoin(page_url, book_card.select_one('a').get('href'))
            books_urls.append(book_url)
    return books_urls


def get_book_response(book_num):
    url = f'https://tululu.org/txt.php?id={book_num}'
    response = requests.get(url, verify=False, allow_redirects=False)
    check_response(response)
    response.raise_for_status()
    return response


def get_genres(soup):
    genre_title, genres_name = soup.select('.d_book')[1].text.split(sep=':')
    genres = genres_name.strip().replace('.', '').split(', ')
    return genres
