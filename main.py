import os
import requests


FOLDER_NAME = 'books'

os.makedirs(FOLDER_NAME, exist_ok=True)

for book_id in range(1, 11):
    url = f'https://tululu.org/txt.php?id={book_id}'
    response = requests.get(url)
    response.raise_for_status()

    filename = f'{book_id}.txt'
    filepath = os.path.join(FOLDER_NAME, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)
