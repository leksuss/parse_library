import os
import requests


FOLDER_NAME = 'books'


def download_book(book_id):
    url = f'https://tululu.org/txt.php?id={book_id}'
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()

    if response.content:
        filename = f'{book_id}.txt'
        filepath = os.path.join(FOLDER_NAME, filename)
        with open(filepath, 'wb') as file:
            file.write(response.content)
    else:
        return


if __name__ == '__main__':
    os.makedirs(FOLDER_NAME, exist_ok=True)

    for book_id in range(1, 11):
        download_book(book_id)
