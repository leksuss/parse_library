import argparse
import json
import logging
import os
import requests
import time
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

import downloader
from exceptions import BookPageError, DownloadBookError, CategoryPageError

SITE_URL = 'https://tululu.org'
FANTASTIC_CATEGORY_URI = 'l55'
BOOKS_FILENAME = 'books.json'

logger = logging.getLogger(__file__)


def read_args():
    parser = argparse.ArgumentParser(
        description='''
            Download books from from fantastic category tululu.org e-library 
        '''
    )
    parser.add_argument(
        '--start_page',
        default=1,
        type=int,
        nargs='?',
        help='From which page id to download'
    )
    parser.add_argument(
        '--end_page',
        default=10**6,
        type=int,
        nargs='?',
        help='Up to which page id to download'
    )
    parser.add_argument(
        '--dest_folder',
        default='.',
        type=str,
        nargs='?',
        help='Path to save parsed books'
    )
    parser.add_argument(
        '--json_path',
        default=None,
        nargs='?',
        help='Path to save meta information about book'
    )
    parser.add_argument(
        '--skip_imgs',
        action='store_true',
        help='Skip download book cover image'
    )
    parser.add_argument(
        '--skip_txt',
        action='store_true',
        help='Skip download text of book'
    )

    args = parser.parse_args()
    return args


def get_page_content(page_url):
    response = requests.get(page_url)
    response.raise_for_status()
    downloader.check_for_redirect(response, CategoryPageError)

    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_book_urls_in_page(soup, site_url):
    book_cards = soup.select('#content table')
    book_urls = []
    for book_card in book_cards:
        link = book_card.select_one('td+td a')['href']
        book_urls.append(urljoin(site_url, link))
    return book_urls

def main():
    args = read_args()

    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            '%(asctime)s %(message)s'))
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    books_folder_path = None
    if not args.skip_txt:
        books_folder_path = os.path.join(
            args.dest_folder, downloader.BOOKS_FOLDER
        )
        os.makedirs(books_folder_path, exist_ok=True)

    images_folder_path = None
    if not args.skip_imgs:
        images_folder_path = os.path.join(
            args.dest_folder, downloader.IMAGES_FOLDER
        )
        os.makedirs(images_folder_path, exist_ok=True)

    json_filepath = args.dest_folder
    json_filename = BOOKS_FILENAME
    if args.json_path:
        json_filepath, json_filename = os.path.split(args.json_path)
        if json_filepath:
            os.makedirs(json_filepath, exist_ok=True)

    books = []
    for page_id in range(args.start_page, args.end_page):
        page_url = '/'.join((SITE_URL, FANTASTIC_CATEGORY_URI, str(page_id)))
        try:
            soup = get_page_content(page_url)
        except CategoryPageError:
            logger.warning(
                f'Страницы {page_id} нет, заканчиваем работу'
            )
            break
        logger.info(
            f'Открываем страницу № {page_id}'
        )
        book_urls = get_book_urls_in_page(soup, SITE_URL)
        for book_url in book_urls:
            book_id =  urlparse(book_url).path.split('/')[1][1:]
            book = None
            while not book:
                try:
                    book = downloader.download_book(
                        book_id,
                        books_folder_path,
                        images_folder_path,
                    )
                except BookPageError:
                    logger.warning(
                        f'[Книга не скачана]: книги #{book_id} на tululu нет'
                    )
                    break
                except DownloadBookError:
                    logger.warning(
                        f'[Книга не скачана]: книгу №{book_id} скачать нельзя'
                    )
                    break
                except (requests.ConnectionError, requests.ReadTimeout):
                    logger.warning(
                        f'Не подключиться, \
                            повтор через {downloader.RETRY_TIMEOUT} сек'
                    )
                    time.sleep(downloader.RETRY_TIMEOUT)
            else:
                logger.info(
                    f'[Книга скачана]: {book["title"]}, автор: {book["author"]}'
                )
                books.append(book)

    json_filepath = os.path.join(json_filepath, json_filename)
    with open(json_filepath, 'w') as f:
        json.dump(books, f, ensure_ascii=False)


if __name__ == '__main__':
    main()
