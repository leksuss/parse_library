import json
import  os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

import parse_tululu_category

TEMPLATE = 'template.html'
WEBSITE_DIR = 'website'
PAGES_SUBDIR = 'pages'
BOOKS_PER_PAGE = 20


def render_page(html_template, books, pages_dir, books_per_page, env):
    template = env.get_template(html_template)
    chunked_books = list(chunked(books, books_per_page))
    pages = range(1, len(chunked_books) + 1)

    for page_id, books_chunk in enumerate(chunked_books, 1):
        rendered_content = template.render({
            'books': list(chunked(books_chunk, 2)),
            'pages': pages,
            'current_page': page_id,
        })
        filename = os.path.join(pages_dir, f'index{page_id}.html')
        with open(filename, 'w', encoding="utf8") as file:
            file.write(rendered_content)


def main():
    pages_dir = os.path.join(WEBSITE_DIR, PAGES_SUBDIR)
    os.makedirs(pages_dir, exist_ok=True)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    books_filepath = os.path.join(
        WEBSITE_DIR, parse_tululu_category.BOOKS_FILENAME
    )
    with open(books_filepath, 'r') as f:
        books = json.load(f)

    run_render = lambda: render_page(
        TEMPLATE, books, pages_dir, BOOKS_PER_PAGE, env
    )

    run_render()
    server = Server()
    server.watch(TEMPLATE, run_render())
    server.serve(root=WEBSITE_DIR)

if __name__ == '__main__':
    main()
