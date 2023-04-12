import argparse
import os
from urllib.parse import urljoin, urlsplit, unquote

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

BOOKS_FOLDER = 'books'
IMAGES_FOLDER = 'images'


def read_args():
    parser = argparse.ArgumentParser(
        description='''
            Download books from tululu.org e-library
        '''
    )
    parser.add_argument(
        '--start_id',
        default=1,
        type=int,
        help='''
            From which book id to download
        '''
    )
    parser.add_argument(
        '--end_id',
        default=10,
        type=int,
        help='''
            Up to which book id to download
        '''
    )
    args = parser.parse_args()
    return args


def download_txt(url, filename, folder):
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()

    if response.content:
        filepath = os.path.join(folder, filename)
        with open(filepath, 'wb') as file:
            file.write(response.content)
        return filepath
    return None


def download_img(url, folder):
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()

    if response.content:
        filename = unquote(urlsplit(url).path.split('/')[-1])
        filepath = os.path.join(folder, filename)
        with open(filepath, 'wb') as file:
            file.write(response.content)
        return filepath
    return None


def parse_book_page(soup):
    title, author = soup.find(id='content').find('h1').text.split('::')

    genre = soup.find('span', class_='d_book').find('a').text.strip()

    cover_uri = soup.find(class_='bookimage').find('img')['src']
    cover_url = urljoin('https://tululu.org', cover_uri)

    comments = []
    raw_comments = soup.find_all(class_='texts')
    for raw_comment in raw_comments:
        comment = raw_comment.find(class_='black').text.strip()
        comments.append(comment)

    return {
        'title': title.strip(),
        'author': author.strip(),
        'genre': genre,
        'cover_url': cover_url,
        'comments': comments,
    }


def download_book(book_id, book_folder, image_folder):
    url = f'https://tululu.org/b{book_id}/'
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()

    if response.content:
        soup = BeautifulSoup(response.text, 'lxml')
        book = parse_book_page(soup)

        filename = f"{book_id}. {sanitize_filename(book['title'])}.txt"
        txt_url = f'https://tululu.org/txt.php?id={book_id}'
        filepath = download_txt(txt_url, filename, book_folder)
        if filepath:
            download_img(book['cover_url'], image_folder)
            return book['title'], book['author']
    return None, None


def main():
    args = read_args()

    os.makedirs(BOOKS_FOLDER, exist_ok=True)
    os.makedirs(IMAGES_FOLDER, exist_ok=True)

    for book_id in range(args.start_id, args.end_id + 1):
        title, author = download_book(book_id, BOOKS_FOLDER, IMAGES_FOLDER)
        if title:
            print('Название:', title)
            print('Автор:', author, end='\n\n')


if __name__ == '__main__':
    main()
