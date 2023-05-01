import json
import logging
import os
import requests
import time
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

import downloader

SITE_URL = 'https://tululu.org'
PAGES_TO_DOWNLOAD = 4
FANTASTIC_SECTION_URI = 'l55'
BOOK_JSON_FLE = 'books.json'

logger = logging.getLogger(__file__)


def get_page_content(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_book_urls_in_page(soup, site_url):
    book_cards = soup.find(id='content').find_all('table')
    book_urls = []
    for book_card in book_cards:
        tds = book_card.find_all('td')
        link = tds[1].find('a')['href']
        book_urls.append(urljoin(site_url, link))
    return book_urls


def main():
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            '%(asctime)s %(message)s'))
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    os.makedirs(downloader.BOOKS_FOLDER, exist_ok=True)
    os.makedirs(downloader.IMAGES_FOLDER, exist_ok=True)

    books = []
    for page_id in range(1, PAGES_TO_DOWNLOAD + 1):
        page_url = '/'.join((SITE_URL, FANTASTIC_SECTION_URI, str(page_id)))
        soup = get_page_content(page_url)
        book_urls = get_book_urls_in_page(soup, SITE_URL)
        for book_url in book_urls:
            book_id =  urlparse(book_url).path.split('/')[1][1:]
            book = None
            while not book:
                try:
                    book = downloader.download_book(
                        book_id,
                        downloader.BOOKS_FOLDER,
                        downloader.IMAGES_FOLDER
                    )

                except downloader.BookPageError:
                    logger.warning(
                        f'[Книга не скачана]: книги #{book_id} на tululu нет'
                    )
                    break
                except downloader.DownloadBookError:
                    logger.warning(
                        f'[Книга не скачана]: книгу №{book_id} скачать нельзя'
                    )
                    break
                except (requests.ConnectionError, requests.ReadTimeout):
                    logger.warning(
                        f'''Не подключиться, \
                            повтор через {downloader.RETRY_TIMEOUT} сек'''
                    )
                    time.sleep(downloader.RETRY_TIMEOUT)
            else:
                logger.info(
                    f'[Книга скачана]: {book["title"]}, автор: {book["author"]}'
                )
                books.append(book)

    with open(BOOK_JSON_FLE, 'w') as f:
        json.dump(books, f, ensure_ascii=False)


if __name__ == '__main__':
    main()
