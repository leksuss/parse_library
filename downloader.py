import argparse
import logging
import os
import time
from urllib.parse import urljoin, urlsplit, unquote

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

from error_handlers import BookPageError, DownloadBookError

BOOKS_FOLDER = 'books'
IMAGES_FOLDER = 'images'
RETRY_TIMEOUT = 5  # in seconds

logger = logging.getLogger(__file__)


def read_args():
    parser = argparse.ArgumentParser(
        description='''
            Download books from tululu.org e-library
        '''
    )
    parser.add_argument(
        'start_id',
        default=1,
        type=int,
        nargs='?',
        help='''
            From which book id to download
        '''
    )
    parser.add_argument(
        'end_id',
        default=10,
        type=int,
        nargs='?',
        help='''
            Up to which book id to download
        '''
    )
    args = parser.parse_args()
    return args


def check_for_redirect(response, exception_type=None):
    if response.url == 'https://tululu.org/':
         raise exception_type


def download_txt(book_id, book_title, folder):

    filename = f'{book_id}. {sanitize_filename(book_title)}.txt'
    url = 'https://tululu.org/txt.php'
    params = {
        'id': book_id,
    }

    response = requests.get(url, params=params, timeout=5)
    response.raise_for_status()
    check_for_redirect(response, DownloadBookError)

    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


def download_img(url, folder):
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    check_for_redirect(response)

    filename = unquote(urlsplit(url).path.split('/')[-1])
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


def parse_book_page(book_url, soup):
    title, author = soup.select_one('#content h1').text.split('::')

    genres_links = soup.select('span.d_book a')
    genres = [genre.text.strip() for genre in genres_links]

    img_uri = soup.select_one('.bookimage img')['src']
    img_url = urljoin(book_url, img_uri)

    raw_comments = soup.select('.texts .black')
    comments = [raw_comment.text.strip() for raw_comment in raw_comments]

    return {
        'title': title.strip(),
        'author': author.strip(),
        'genres': genres,
        'img_url': img_url,
        'comments': comments,
    }


def download_book(book_id, book_folder, image_folder):
    book_url = f'https://tululu.org/b{book_id}/'

    response = requests.get(book_url, timeout=5)
    response.raise_for_status()
    check_for_redirect(response, BookPageError)

    soup = BeautifulSoup(response.text, 'lxml')
    book = parse_book_page(book_url, soup)

    book['book_path'] = download_txt(book_id, book['title'], book_folder)
    book['img_src'] = download_img(book['img_url'], image_folder)
    del book['img_url']

    return book


def main():
    args = read_args()

    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            '%(asctime)s %(message)s'))
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    os.makedirs(BOOKS_FOLDER, exist_ok=True)
    os.makedirs(IMAGES_FOLDER, exist_ok=True)

    for book_id in range(args.start_id, args.end_id + 1):
        book = None
        while not book:
            try:
                book = download_book(
                    book_id,
                    BOOKS_FOLDER,
                    IMAGES_FOLDER
                )
            except BookPageError:
                logger.warning(
                    f'[Книга не скачана]: книги #{book_id} в библиотеке нет'
                )
                break
            except DownloadBookError:
                logger.warning(
                    f'[Книга не скачана]: книгу №{book_id} скачать нельзя'
                )
                break
            except (requests.ConnectionError, requests.ReadTimeout):
                logger.warning(
                    f'Не могу подключиться, повтор через {RETRY_TIMEOUT} сек'
                )
                time.sleep(RETRY_TIMEOUT)
        else:
            logger.info(
                f'[Книга скачана]: {book["title"]}, автор: {book["author"]}'
            )

if __name__ == '__main__':
    main()
