from __future__ import print_function
import argparse
from utils import get_last_page, get_books_urls, get_html, get_book_response, eprint
from book import get_book
from os import chdir
from pathlib import Path
import json
import requests
from time import sleep
import logging
import sys

logger = logging.getLogger()


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Программа скачивает коллекцию книг фантастического жанра'
    )
    parser.add_argument('--start_page', type=int, help='с какой страницы скачать', default=1)
    parser.add_argument('--end_page', type=int, help='до какой страницы скачать, не включая её',
                        default=get_last_page() + 1)
    parser.add_argument('--dest_folder', help='путь к каталогу с результатами парсинга: картинкам, книгам, JSON')
    parser.add_argument('--skip_imgs', help='не скачивать картинки', action="store_true")
    parser.add_argument('--skip_txt', help='не скачивать txt', action="store_true")
    parser.add_argument('--json_path', help='указать свой путь к *.json файлу с результатами')
    args = parser.parse_args()
    return args


def main():
    logging.basicConfig(level='INFO', format='%(filename)s - %(asctime)s - %(levelname)s - %(message)s')
    args = parse_arguments()
    start_page = args.start_page
    end_page = args.end_page
    books_urls = get_books_urls(start_page, end_page)
    books = []
    if args.dest_folder:
        Path(args.dest_folder).mkdir(parents=True, exist_ok=True)
        chdir(args.dest_folder)
    attempt = 1
    for book_url in books_urls:
        try:
            book_num = book_url.split('b')[-1]
            response = get_book_response(book_num)
            book_html = get_html(book_url)
            book = get_book(book_url, book_html, response, args.skip_txt, args.skip_imgs)
            books.append(book)
        except requests.HTTPError:
            logger.info('requests.HTTPError')
        except ConnectionError as error:
            if attempt > 3:
                logger.info(error)
                eprint('Max reconnection attempts exceeded')
                sys.exit()
            logger.info(error)
            eprint(f'Attempt to reconnect {attempt}/3 after 30 seconds')
            attempt += 1
            sleep(30)
    if args.json_path:
        Path(args.json_path).mkdir(parents=True, exist_ok=True)
        chdir(args.json_path)
    with open(f'books.json', 'w', encoding='utf8') as file:
        json.dump(books, file, ensure_ascii=False)


if __name__ == '__main__':
    main()
