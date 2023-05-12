import json
import  os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

import parse_tululu_category

TEMPLATE = 'template.html'
PAGE_NAME = 'index'
DIR_NAME = 'pages'


def render_page(html_template, page_name, books, dir_name, env):
    template = env.get_template(html_template)
    chunked_books = list(chunked(books, 20))
    pages = range(1, len(chunked_books) + 1)
    for page_id, books_chunk in enumerate(chunked_books, 1):
        rendered_content = template.render({
            'books': chunked(books_chunk, 2),
            'pages': pages,
            'current_page': page_id,
        })
        filename = os.path.join(dir_name, f'{page_name}{page_id}.html')
        with open(filename, 'w', encoding="utf8") as file:
            file.write(rendered_content)


def main():
    os.makedirs(DIR_NAME, exist_ok=True)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    with open(parse_tululu_category.BOOKS_FILENAME, 'r') as f:
        books = json.load(f)

    render_page(TEMPLATE, PAGE_NAME, books, DIR_NAME, env)
    server = Server()
    server.watch(
        TEMPLATE, 
        lambda: render_page(
            TEMPLATE, PAGE_NAME, {'books': books}, DIR_NAME, env
        )
    )
    server.serve(root='.')

if __name__ == '__main__':
    main()
