import os

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

FOLDER_NAME = 'books'


def get_book(book_id, folder):

    url = f'https://tululu.org/b{book_id}/'
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()

    if response.content:
        soup = BeautifulSoup(response.text, 'lxml')
        title = soup.find(id='content').find('h1').text.split('::')[0].strip()
        filename = f'{book_id}. {sanitize_filename(title)}.txt'
        url = f'https://tululu.org/txt.php?id={book_id}'
        return download_txt(url, filename, folder)
    return None


def download_txt(url, filename, folder='books/'):

    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()

    if response.content:
        filepath = os.path.join(folder, filename)
        with open(filepath, 'wb') as file:
            file.write(response.content)
        return filepath
    return None


if __name__ == '__main__':
    os.makedirs(FOLDER_NAME, exist_ok=True)

    for book_id in range(1, 11):
        get_book(book_id, FOLDER_NAME)
