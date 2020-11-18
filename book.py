
from utils import get_genres
from bs4 import BeautifulSoup
from download_files import download_txt, download_image


def get_book_data(html):
    soup = BeautifulSoup(html, 'lxml')
    title, author = soup.select_one('h1').text.split(sep='::')
    img_url = soup.select_one('.bookimage img')['src']
    comments = [texts_comments.select_one('.black').text for texts_comments in soup.select('.texts')]
    genres = get_genres(soup)
    return title.strip(), author.strip(), comments, genres, img_url


def get_book(book_url, book_html, response, skip_txt, skip_imgs):
    title, author, comments, genres, img_url = get_book_data(book_html)
    book = {
        'title': title,
        'author': author,
        'image_src': None,
        'book_path': None,
        'comments': comments,
        'genres': genres
    }
    if not skip_txt:
        book_path = download_txt(response, title)
        book['book_path'] = book_path
    if not skip_imgs:
        image_src = download_image(book_url, img_url)
        book['image_src'] = image_src
    return book
