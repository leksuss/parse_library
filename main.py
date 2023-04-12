import os
from urllib.parse import urljoin, urlsplit, unquote

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

BOOKS_FOLDER = 'books'
IMAGES_FOLDER = 'images'


def download_txt(url, filename, folder):

    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()

    if response.content:
        filepath = os.path.join(folder, filename)
        with open(filepath, 'wb') as file:
            file.write(response.content)
        return filepath
    return None


def download_img(url, filename, folder):

    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()

    if response.content:
        filepath = os.path.join(folder, filename)
        with open(filepath, 'wb') as file:
            file.write(response.content)
        return filepath
    return None


def get_book(book_id, book_folder, image_folder):

    url = f'https://tululu.org/b{book_id}/'
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()

    if response.content:
        soup = BeautifulSoup(response.text, 'lxml')
        title = soup.find(id='content').find('h1').text.split('::')[0].strip()

        filename = f'{book_id}. {sanitize_filename(title)}.txt'
        txt_url = f'https://tululu.org/txt.php?id={book_id}'
        filepath = download_txt(txt_url, filename, book_folder)

        img_uri = soup.find(class_='bookimage').find('img')['src']
        img_url = urljoin('https://tululu.org', img_uri)
        filename = unquote(urlsplit(img_uri).path.split('/')[-1])
        imgpath = download_img(img_url, filename, image_folder)

        return filepath, imgpath
    return None


if __name__ == '__main__':
    os.makedirs(BOOKS_FOLDER, exist_ok=True)
    os.makedirs(IMAGES_FOLDER, exist_ok=True)

    for book_id in range(1, 2):
        get_book(book_id, BOOKS_FOLDER, IMAGES_FOLDER)
